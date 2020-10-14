#TODO change message sent from revieved to reflect that the user is challenging another player

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChallengeConsumer(WebsocketConsumer):
    def connect(self):

        self.player_name = self.scope['user']
        self.challenge_player_group = 'challenge_%s' % self.player_name

        # Join challenge player group
        async_to_sync(self.channel_layer.group_add)(
            self.challenge_player_group,
            self.channel_name
        )

        self.accept()
        print("{} joined self".format(self.challenge_player_group))

    def disconnect(self, close_code):
        # Leave challenge player group
        print(self.challenge_player_group)
        async_to_sync(self.channel_layer.group_discard)(
            self.challenge_player_group,
            self.channel_name
        )



    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        challenge_player_group = "challenge_"
        challenge_player_group += message

        #connect to challenge player group
        async_to_sync(self.channel_layer.group_add)(
            challenge_player_group,
            self.channel_name
        )
        print("joined {}'s challenge_player_group".format(message))

        # Send message to challenge player group
        async_to_sync(self.channel_layer.group_send)(
            challenge_player_group,
            {
                'type': 'challenge_player',
                'message': message
            }
        )

        #get out of group of the player you just challenged
        async_to_sync(self.channel_layer.group_discard)(
            challenge_player_group,
            self.channel_name
        )
        print("{} discarded group".format(self.scope['user'].username))


    # Receive message from challenge player group
    def challenge_player(self, event):
        message = event['message']
        print("{} got message {}".format(self.scope['user'].username, message))
        if (message == self.scope['user'].username):

            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message
            }))
            print("{} sent message".format(self.scope['user'].username))

