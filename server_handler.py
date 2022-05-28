import requests
import json
from config import host
from termcolor import colored


def connect(username, url=f'http://{host}/connect/'):
    print("Connecting to server")

    send_data = {
        'user': username
    }
    response = requests.post(url, data=send_data)
    try:
        users = eval(response.text)
        print(colored("Connected.", "green"))
        print(colored("Users: "+str(users), "yellow"))
        return True
    except:
        print(response.text)
        if response.text == 'user already connected':
            option = input('wanna override? [y/n] ')
            if option.lower() == 'y':
                connect(username, url=f'http://{host}/force_connect/')
                return True
            else:
                return False


def disconnect(username):
    url = f'http://{host}/disconnect/'
    send_data = {
        'user': username
    }
    response = requests.post(url, data=send_data)
    print(colored(response.text, "yellow"))
