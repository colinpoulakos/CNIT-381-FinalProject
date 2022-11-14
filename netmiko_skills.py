from netmiko import ConnectHandler

#Use netmiko to connect the the device using the inforamtion passed in from the function and execute a
#command to show the interfaces that are configured with DHCP
def show_dhcp_ints(host, user, password, secret):
    #Define connection
    conn_info = {'device_type': 'cisco_ios', 'host': host, 'username': user,
    'password': password,'port': 22, 'secret': secret, 'verbose': True}

    #Create connection
    connection = ConnectHandler(**conn_info)
    connection.enable()

    #Send command and return output
    output = connection.send_command('show ip int br | in DHCP')
    connection.disconnect()
    return output

#Connect the the device using Netmiko and add a loopback interface
def add_loopback(host, user, password, secret, int_id, ip, mask):
    #Define connection
    conn_info = {'device_type': 'cisco_ios', 'host': host, 'username': user,
    'password': password,'port': 22, 'secret': secret, 'verbose': True}

    #Create command set using passed in arguments
    interface = 'int lo {}'.format(int_id)
    ip_add = 'ip address {} {}'.format(ip, mask)
    print(ip_add)
    commands = [interface, ip_add, 'exit']
    
    #Connect to device and execute command set
    connection = ConnectHandler(**conn_info)
    connection.enable()
    connection.config_mode()
    connection.send_config_set(commands)

    #Verify the creation by returning all loopback interfaces
    output = connection.send_command('show ip int br | in Loopback')
    connection.exit_config_mode()

    connection.disconnect()
    return output

#Use netmiko to connect to the HQ router to fix the VPN configuration
def fix_VPN_Config(host, user, password, secret, old_peer, new_peer):
    #Define connection
    conn_info = {'device_type': 'cisco_ios', 'host': host, 'username': user,
    'password': password,'port': 22, 'secret': secret, 'verbose': True}

    #Build command set
    commands = ["no crypto isakmp key cisco address {}".format(old_peer), "crypto isakmp key cisco address {}".format(new_peer), 
        "crypto map Crypt 10 ipsec-isakmp","no set peer {}".format(old_peer),"set peer {}".format(new_peer),'exit']
    
    #Connect to device and execute command set
    connection = ConnectHandler(**conn_info)
    connection.enable()
    connection.config_mode()
    connection.send_config_set(commands)
    connection.exit_config_mode()

    #Test the new configuration
    output = connection.send_command('ping 2.2.2.2 source 1.1.1.1')

    connection.disconnect()
    return output
