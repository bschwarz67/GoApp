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
        message = self.scope['user'].username
        challenge_player_group = "challenge_"
        challenge_player_group += text_data_json['message']

        #connect to challenge player group
        async_to_sync(self.channel_layer.group_add)(
            challenge_player_group,
            self.channel_name
        )
        print("joined {}'s challenge_player_group".format(text_data_json['message']))

        # Send message to challenge player group
        async_to_sync(self.channel_layer.group_send)(
            challenge_player_group,
            {
                'type': 'challenge_player',
                'message': message,
                'recipient' : text_data_json['message']
            }
        )

        #get out of group the player you just challenged
        async_to_sync(self.channel_layer.group_discard)(
            challenge_player_group,
            self.channel_name
        )
        print("{} discarded group".format(self.scope['user'].username))


    # Receive message from challenge player group
    def challenge_player(self, event):
        message = event['message']
        recipient = event['recipient']
        username = self.scope['user'].username

        print("{} got message {}".format(username, message))
        if (recipient == username):

            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': message
            }))
            print("{} sent message".format(username))

