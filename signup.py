import requests
import config


def getInputs():
    user = input('username: ')
    password = input('password: ')
    return {user: password}


def signup():
    url = f'http://{config.host}/signup/'

    print('Signing a new user up\n')
    user = {'signup': getInputs()}
    response = requests.post(url, data=str(user))
    print(response.text)


signup()
