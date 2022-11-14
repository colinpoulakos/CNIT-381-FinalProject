### teams Bot ###
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response

### Created Skills
import netmiko_skills as netmiko
import restconf_skills as restconf
import my_utilities as utils
from mygenieskill import VPNMonitor


### System Utilities
from requests_toolbelt.multipart.encoder import MultipartEncoder
import ansible_runner as ar
import requests
import threading
import time
import os


#Variables for background monitoring
stop_flag = False
th = None

# RESTCONF Setup
port = '443'
headers = {'Content-Type': 'application/yang-data+json',
           'Accept': 'application/yang-data+json'}

#Ansible and routers file setup. This builds the ansible inventory file and returns data to the routers variable
#for other skills to use
routers = utils.build_ansible_inv()

# Bot Details
bot_email = 'YOUR BOT EMAIL HERE'
teams_token = 'YOUR BOT TOKEN HERE'
bot_url = "YOUR WEBHOOK HERE"
bot_app_name = 'Network Automation Chat Bot'

# Create a Bot Object
#   Note: debug mode prints out more details about processing to terminal
bot = TeamsBot(
    bot_app_name,
    teams_bot_token=teams_token,
    teams_bot_url=bot_url,
    teams_bot_email=bot_email,
    debug=False,
    webhook_resource_event=[
        {"resource": "messages", "event": "created"},
        {"resource": "attachmentActions", "event": "created"},],
)

# Create a function to respond to messages that lack any specific command
# The greeting will be friendly and suggest how folks can get started.
def greeting(incoming_msg):
    # Loopkup details about sender
    sender = bot.teams.people.get(incoming_msg.personId)

    # Create a Response object and craft a reply in Markdown.
    response = Response()
    response.markdown = "Hello {}, I can help you mange your network .  ".format(
        sender.firstName
    )
    response.markdown += "\n\nSee what I can do by asking for **/help**."
    return response

#Show the interfaces on a device that are configured with DHCP
def show_dhcp(incoming_msg):
    response = Response()
    #Read the message and parse out each element. Input nneds to be comma delineated to extract device name
    message = [word.strip() for word in incoming_msg.text.split(",")]
    device = message[1]

    #Use netmiko to access device and get information
    ints_list = (netmiko.show_dhcp_ints(routers[device]['ip'], routers[device]['user'], 
        routers[device]['password'], routers[device]['secret'])).split("\n")

    #Build response based on if there are any DHCP interfaces or not
    if len(ints_list) == 0:
        response.markdown = "No DHCP interfaces configured."
    else:
        for interface in ints_list:
            response.markdown = "DHCP Interfaces: \n"
            this_int = interface.split()
            response.markdown += "{}: {}".format(this_int[0], this_int[1])

    return response

#Find the number of packets received and transmitted on each interface of devices
def sys_packets(incoming_msg):
    response = Response()
    #Read the message and parse out each element. Input nneds to be comma delineated to extract device name
    message = [word.strip() for word in incoming_msg.text.split(",")]
    device = message[1]

    #Build URL and uset RESTCONF to gather data
    url_base = "https://{h}/restconf".format(h=routers[device]['ip'])
    packets = restconf.get_int_packets(url_base, headers, routers[device]['user'], routers[device]['password'])

    #Build response using returned data
    response.markdown = "Packets received and transmitted on each interface of {}:\n\n".format(device)
    for interface in packets:
        response.markdown += "{} | RX: {} | TX: {} \n\n".format(interface['name'], 
            interface['statistics']['in-unicast-pkts'], interface['statistics']['out-unicast-pkts'])
   
    return response

#Show which netowrks OSPF is configured to route for on a device
def ospf_conf(incoming_msg):
    response = Response()
    #Read the message and parse out each element. Input nneds to be comma delineated to extract device name
    message = [word.strip() for word in incoming_msg.text.split(",")]
    device = message[1]

    #Build URL and use RESTCONF to gather data
    url_base = "https://{h}/restconf".format(h=routers[device]['ip'])
    ospf = restconf.get_ospf(url_base, headers, routers[device]['user'], routers[device]['password'])

    #Build response from gatherd data
    if type(ospf) == str:
        response.markdown = ospf
    else:
        response.markdown = "#### OSPF Process ID: {} \n##### Networks:\n".format(ospf['ospf']['process-id'][0]['id'])

        for network in ospf['ospf']['process-id'][0]['network']:
            response.markdown += "- IP: {}\n - Wildcard: {}\n - Area: {}\n".format(network['ip'], 
                network['wildcard'], network['area'])
            response.markdown += "---\n"
   
    return response

#Use Ansible to gather the running configs from the devices and return them as a file
def get_backups(incoming_msg):
    response = Response()
    #Find room id for furute API calls
    room_id = incoming_msg.roomId
    #Delete old files
    files = os.listdir("ansible-data/backups/")
    for item in files:
        os.remove(("./ansible-data/backups/"+item))
    
    #get confugrations using Ansible
    r = ar.run(private_data_dir='./', playbook='backup_cisco_router_playbook.yaml')

    #Format and return a file for each device. 
    response.markdown = "Here are your configurations.\n"
    files = os.listdir("ansible-data/backups/")

    #Format and return each file
    for item in files:
        #Remove unneccessary information from beginning of file
        with open("ansible-data/backups/{}".format(item), 'r') as fin:
            data = fin.read().splitlines(True)
        with open("ansible-data/backups/{}".format(item), 'w') as fout:
            fout.writelines(data[15:])

        #Post the file to the message room using the api
        filepath = "./ansible-data/backups/" + item
        m = MultipartEncoder({'roomId': room_id,
                      'files': (filepath, open(filepath, 'rb'))})
        r = requests.post('https://webexapis.com/v1/messages', data=m,
                  headers={'Authorization': 'Bearer {}'.format(teams_token),
                  'Content-Type': m.content_type})
    return response

#Use Netmiko to confugre a loopback interface on a device
def conf_loopback(incoming_msg):
    response = Response()

    #Read the message and parse out each element. Message must be comma delineated to extrat each element
    message = [word.strip() for word in incoming_msg.text.split(",")]
    device = message[1]
    int_id = message[2]
    ip = message[3]
    mask = message[4]

    #Configure the loopback if the device exists. Return an error message if configuration fails
    if device in routers:
        try:
            out = netmiko.add_loopback(routers[device]['ip'], routers[device]['user'], routers[device]['password'], 
                routers[device]['secret'], int_id, ip, mask)
            response.markdown = "Loopback created. \n\n Current loopbacks.\n"
            response.markdown += out
        except:
            response.markdown = "An error occured when adding the interface."     
    else:
        response.markdown = "Not created. Device not found."

    return response

#List the hostnames of the devices the bot can manage
def list_hostnames(incoming_msg):
    response = Response()
    response.markdown = "Available hostnames:\n"
    for name in routers:
        response.markdown += "- {}\n".format(name)

    return response

#Start background process that will monitor the address of the VPN address on the brnach router
def start_monitor(incoming_msg):
    response = Response()
    response.markdown = "Monitoring on VPN interface started.\n\n"
    global th
    th = threading.Thread(target=monitor_VPN, args=(incoming_msg,))
    th.start()
    print("Thread starts")
       
    return response

#Actuall monitoring function
def monitor_VPN(incoming_msg):
    response = Response()
    room_id = incoming_msg.roomId

    #Create monitor object and connect to the device
    monitor = VPNMonitor()
    connect = monitor.build_connection('testbed.yaml')
    #Check the current IP of the VPN interface
    current_ip = monitor.check_IP()

    #Lopp will continously monitor the interface and will trigger actions if IP address changes. 
    #Loop will stop when stop_monitor function is called
    global stop_flag
    while stop_flag == False:
        new_ip = monitor.check_IP()
        #If the IP address changes, post a message and attempt to change the configuration on the HQ router
        #to bring the VPN back up.
        if new_ip != current_ip:
            print("VPN address at branch location as changed.")
            utils.create_message(room_id, "IP Address on branch VPN interface has changed from {} to {}.\n\n Please wait while I update the HQ router config...".format(current_ip,new_ip), teams_token)
            try:
                change_vpn = netmiko.fix_VPN_Config(routers['hq']['ip'], routers['hq']['user'], routers['hq']['password'], routers['hq']['secret'], current_ip, new_ip)
                if '!' in change_vpn:
                   utils.create_message(room_id, "HQ VPN Update SUCCESS. \n\n Connection test PASSED.", teams_token)
                else:
                    utils.create_message(room_id, "HQ VPN Update SUCCESS. \n\n Connection test FAILED.", teams_token)
            except:
                utils.create_message(room_id, "HQ VPN Update FAILED", teams_token)
            current_ip = new_ip
        else:
            print("no changes in ip on vpn")
        #Wait 5 seconds between checking the IP address
        time.sleep(5)
    
    #Reset flag for next monitoring session
    stop_flag = False
    return response

#Stops background prrocees of the monitor
def stop_monitor(incoming_msg):
    response = Response()
    response.markdown = "Stopped monitoring Branch VPN interface"
    global stop_flag
    stop_flag = True
    global th
    th.join()

    return response


# Set the bot greeting.
bot.set_greeting(greeting)

# Add Bot's Commmands
bot.add_command("show dhcp", "Show interfaces configured with DHCP (netmiko)", show_dhcp)
bot.add_command("show packet stats", "Display packets received and transmitted on each interface (restconf)", sys_packets)
bot.add_command("backup routers", "Get files of running configurations for all devices (ansible)", get_backups)
bot.add_command("show ospf", "Show the OSPF configuration (restconf)", ospf_conf)
bot.add_command("add loopback", "Add a loopback interface. use the following syntax, commas included: (netmiko)\n add loopback, hostname, int number, ip address, subnet mask", conf_loopback)
bot.add_command("List hostnames", "List the hostnames that I can manage.", list_hostnames)
bot.add_command("Start monitor", "Monitor the IP of the branch VPN interface (Genie & Netmiko)", start_monitor)
bot.add_command("Stop monitor", "Stop monitoring the VPN interface", stop_monitor)

# Every bot includes a default "/echo" command.  You can remove it, or any
bot.remove_command("/echo")

if __name__ == "__main__":
    # Run Bot
    bot.run(host="0.0.0.0", port=5000)

