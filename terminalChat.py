import reqcheq
import pysher
import os
import json
from termcolor import colored
from dotenv import load_dotenv
from pusher import Pusher
from server_handler import connect, disconnect
load_dotenv(dotenv_path='.env')

user = ''


class terminalChat():
    pusher = None
    channel = None
    chatroom = None
    clientPusher = None
    user = None
    chatrooms = ["chatroom"]

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

    def disconnect(self):
        ''' Disconnect the user from the server '''
        global user
        self.chatroom = self.chatrooms[0]
        self.initPusher()
        # print in the channel the user has connected
        self.pusher.trigger(self.chatrooms[0], u'newmessage', {
            'user': 'system', 'message': user+' disconnected'})

    def selectChatroom(self):
        ''' This function is used to select which chatroom will connect to '''
        chatroom = self.chatrooms[0]
        if chatroom in self.chatrooms:
            self.chatroom = chatroom
            self.initPusher()
            # print in the channel the user has connected
            self.pusher.trigger(self.chatrooms[0], u'newmessage', {
                'user': 'system', 'message': self.user+' connected'})

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
        if message['user'] != self.user and message['user'] != 'system':
            print(colored("{}: {}".format(
                message['user'], message['message']), "blue"))
        elif message['user'] == 'system':
            print(colored("{}: {}".format(
                message['user'], message['message']), "green"))
        # print(colored("{}: ".format(self.user), "green"))

    def getInput(self):
        ''' This function is used to get the user's current message '''
        message = input()
        self.pusher.trigger(self.chatroom, u'newmessage', {
                            'user': self.user, 'message': message})


try:
    terminalChat().main()
except KeyboardInterrupt:
    terminalChat().disconnect()
    disconnect(user)
