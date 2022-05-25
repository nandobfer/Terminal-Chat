import requests
import json
from config import host


def getUsers():
    url = f'http://{host}/database.json'
    print("Connecting to database's server")
    try:
        data = json.loads(requests.get(url).text)
        print('Connected.')
        return data
    except:
        print("Couldn't connect to server")


def connect(username):
    url = f'http://{host}/connect/'
    send_data = {
        'user': username
    }
    response = requests.post(url, data=send_data)
    try:
        users = eval(response.text)
        print(users)
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
    print(response.text)
