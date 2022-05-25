import RequirementsHandler
import getpass
import pysher
import os
import json
from termcolor import colored
from dotenv import load_dotenv
from pusher import Pusher
from database_handler import getUsers, connect, disconnect
load_dotenv(dotenv_path='.env')

users = getUsers()
user = ''


class terminalChat():
    pusher = None
    channel = None
    chatroom = None
    clientPusher = None
    user = None
    chatrooms = ["supersecreto"]

    def __init__(self, users) -> None:
        self.users = users

    def main(self):
        ''' The entry point of the application'''
        self.login()
        self.selectChatroom()
        while True:
            self.getInput()

    def login(self):
        ''' This function handles login'''
        global user
        self.user = input('username: ')
        if connect(self.user):
            user = self.user
            return True
        else:
            self.login()

        # username = input("Enter your username: ")
        # if username in self.users:
        #     password = getpass.getpass("Password:")
        #     if self.users[username] == password:
        #         self.user = username
        #     else:
        #         print(colored("Password is incorrect", "red"))
        #         self.login()
        # else:
        #     print(colored("Username is incorrect", "red"))
        #     self.login()

    def selectChatroom(self):
        ''' This function is used to select which chatroom will connect to '''
        chatroom = self.chatrooms[0]
        if chatroom in self.chatrooms:
            self.chatroom = chatroom
            self.initPusher()
        else:
            print(colored("No such chatroom in our list", "red"))
            self.selectChatroom()

    def initPusher(self):
        ''' This function initializes both the Http server Pusher as well as the clientPusher'''
        self.pusher = Pusher(app_id=os.getenv('PUSHER_APP_ID', None), key=os.getenv(
            'PUSHER_APP_KEY', None), secret=os.getenv('PUSHER_APP_SECRET', None), cluster=os.getenv('PUSHER_APP_CLUSTER', None))
        self.clientPusher = pysher.Pusher(
            os.getenv('PUSHER_APP_KEY', None), os.getenv('PUSHER_APP_CLUSTER', None))
        self.clientPusher.connection.bind(
            'pusher:connection_established', self.connectHandler)
        self.clientPusher.connect()

    def connectHandler(self, data):
        ''' This function is called once pusher has successfully established a connection'''
        self.channel = self.clientPusher.subscribe(self.chatroom)
        self.channel.bind('newmessage', self.pusherCallback)

    def pusherCallback(self, message):
        message = json.loads(message)
        if message['user'] != self.user:
            print(colored("{}: {}".format(
                message['user'], message['message']), "blue"))
        # print(colored("{}: ".format(self.user), "green"))

    def getInput(self):
        ''' This function is used to get the user's current message '''
        message = input()
        self.pusher.trigger(self.chatroom, u'newmessage', {
                            'user': self.user, 'message': message})


try:
    if users:
        terminalChat(users).main()
except KeyboardInterrupt:
    disconnect(user)
    print('Bye')
