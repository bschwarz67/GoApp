import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class ChallengeConsumer(WebsocketConsumer):
    def connect(self):
        self.player_name = self.scope['user']
        self.player_group = '%s_group' % self.player_name
        # Join player group
        async_to_sync(self.channel_layer.group_add)(
            self.player_group,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave challenge player group
        async_to_sync(self.channel_layer.group_discard)(
            self.player_group,
            self.channel_name
        )



    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        acting_player = self.scope['user'].username
        player_group = text_data_json['message']
        player_group += "_group"

        #connect to player group
        async_to_sync(self.channel_layer.group_add)(
            player_group,
            self.channel_name
        )

        if text_data_json['messageType'] == 'accept':
            # Send accept message to both players involved
            async_to_sync(self.channel_layer.group_send)(
                player_group,
                {
                    'type': 'accept_player',
                    'accepting_player': acting_player,
                    'accepted_player': text_data_json['message']
                }
            )
        else:
            # Send challenge message to challenged player
            async_to_sync(self.channel_layer.group_send)(
                player_group,
                {
                    'type': 'challenge_player',
                    'challenging_player': acting_player,
                    'challenged_player' : text_data_json['message']
                }
            )


        #get out of group the player you just challenged
        async_to_sync(self.channel_layer.group_discard)(
            player_group,
            self.channel_name
        )



    # Receive message from accepting player
    def accept_player(self, event):
        accepting_player = event['accepting_player']
        accepted_player = event['accepted_player']
        username = self.scope['user'].username

        if (username == accepted_player):
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': accepting_player,
                'messageType': 'accept'
            }))
        elif (username == accepting_player):
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': accepted_player,
                'messageType': 'accept'
            }))
        else:
            pass


    # Receive message from challenging player
    def challenge_player(self, event):
        challenging_player = event['challenging_player']
        challenged_player = event['challenged_player']
        username = self.scope['user'].username

        if (username == challenged_player):
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': challenging_player,
                'messageType': 'challenge'
            }))


