# CNIT-381-FinalProject
By Colin Poulakos and Nicolas Langenfeld 

## Project Overview

This goal of this project is to create a networking assistant chat bot that uses a variety of tool including Netmiko, Ansible, RESTCONF, and Genie in order to edit, view, and monitor routers on a network. 

### Prerequisites 
- Have a linux machine
- Python 3.8
- Webex account
- Have the following untilites installed
```
pip3 install ansible-runner
pip3 install webexteamssdk 
pip3 install webexteamsbot 
pip3 install genie
sudo snap install ngrok 
```

## How to Set up a Chat Bot

1. Download all files
2. update input.yml with information for networking devices
3. launch Web hook
4. update roBOTo.py with your teams bot information <br><img width="308" alt="image" src="https://user-images.githubusercontent.com/117847136/201723318-1af10368-dbc9-4844-9fbe-9f0524048bae.png">
5. run roBOTo.py

## Chat Bot Functions Overview
### General Commands
these commands use built in chat bot functions
- /help
  - The /help command lists all of the available commands in a chat bot and a description of what they do. <br> <img width="500" src="https://user-images.githubusercontent.com/65036456/202234792-8b4be954-8a3b-482f-804d-4a4bb4e78f51.png" />

- list hostnames
  - The list hostnames command list all of the hostnames for the devices you put in the input.yml file 

### Netmiko Commands
These commands all use netmiko which is a python extentsion that enables for simplifies the proccess of creating SSH connections for programming networking devices
- add loopback
  - The add loopback command creates a new loopback on a networking device and assigns it an unused IP address
- show dhcp
  - The show dhcp command returns the output of the show dhcp command being ran on a networking device

### Ansible Commands
- backup routers
  - The backup routers command returns .txt files for all networking devices listed in input.yml, containing their current running configuration <br> <img width="400" src="https://user-images.githubusercontent.com/65036456/202235608-2c6f191b-83db-4aff-91fc-ac7270e4a2ca.png" />


### RESTCONF Commands
- show ospf
  - The show ospf command returns the output of the show ospf command being ran on a networking device
- show packet stats
  - The show packet stats command returns the output of the show stats command being ran on a networking device

### GenieCommands
- start monitor - netmiko
  - stop monitor

