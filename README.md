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
  - The /help command does this
- list hostnames
  - the list command does this

### Netmiko Commands
these commands use netmiko which is a python extentsion
- add loopback
  - add loopback does this
- show dhcp
  - show dhcp does this

### Ansible Commands
- backup routers

### RESTCONF Commands
- show ospf
- show packet stats

### GenieCommands
- start monitor - netmiko
  - stop monitor

