# CNIT-381-FinalProject
By Colin Poulakos and Nicolas Langenfeld 

## Project Overview

This goal of this project is to create a networking assistant chat bot that uses a variety of tool including Netmiko, Ansible, RESTCONF, and Genie in order to edit, view, and monitor routers on a network. 

### Prerequisites 
- Have a linux based Virtual Machine
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

