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
