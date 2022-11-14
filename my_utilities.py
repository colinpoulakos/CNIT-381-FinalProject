#import routers
from yaml import safe_load
from jinja2 import Environment, FileSystemLoader
import json
import requests

#Using the input.yml file build an ansible inventory file using a Jinja template and return the data
def build_ansible_inv():
    with open("input.yml", "r") as handle:
        data = safe_load(handle)

    j2_env = Environment(loader=FileSystemLoader("."), autoescape=True)
    template = j2_env.get_template("build_inventory.j2")
    new_config = template.render(data=data)
    f = open("inventory", "w")
    f.write(new_config)
    f.close

    return data


#Send a message to a WebEx Teams room
def create_message(rid, msgtxt, token):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + token,
    }

    url = "https://api.ciscospark.com/v1/messages"
    data = {"roomId": rid, "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()



