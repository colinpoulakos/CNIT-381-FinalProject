import requests
import json

#Use RESTCONF to get the transmit and recieve statistics from each interface
def get_int_packets(url_base,headers,username,password):
    #Define the url, which specifies which items to get
    url = url_base + "/data/ietf-interfaces:interfaces-state/interface"

    # execute the GET statement
    response = requests.get(url,
                            auth=(username, password),
                            headers=headers,
                            verify=False
                            )

    # return the json as text
    return response.json()["ietf-interfaces:interface"]


#Use RESTCONF to get the OSPF confiugration
def get_ospf(url_base,headers,username,password):
    #Define the url, which specifies which items to get
    url = url_base + "/data/Cisco-IOS-XE-native:native/router/router-ospf"

    #Execute GET statement
    response = requests.get(url,
                            auth=(username, password),
                            headers=headers,
                            verify=False
                            )

    # return the json as text
    try:
        return response.json()["Cisco-IOS-XE-ospf:router-ospf"]
    except:
        return "OSPF is not configured"