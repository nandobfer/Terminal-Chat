import requests
import json
from config import host
from termcolor import colored


def connect(username):
    print("Connecting to server")
    url = f'http://{host}/connect/'
    send_data = {
        'user': username
    }
    response = requests.post(url, data=send_data)
    try:
        users = eval(response.text)
        print(colored("Connected.", "green"))
        print(colored("Users: "+users, "yellow"))
        return True
    except:
        print(response.text)
        return False


def disconnect(username):
    url = f'http://{host}/disconnect/'
    send_data = {
        'user': username
    }
    response = requests.post(url, data=send_data)
    print(colored(response.text, "yellow"))
