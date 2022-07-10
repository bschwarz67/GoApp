import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from home.models import Player
from board.models import Game
import sys
sys.path.append('/Users/bryan/desktop/personalCodeRepo/goapp/goapp/board')
import checkPosition



class PlayConsumer(WebsocketConsumer):
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

        player_name = text_data_json['playedAgainst']
        player_group = '%s_group' % player_name
        
        

        if Game.objects.get(id=int(text_data_json['gameID'])).movingPlayer.username == self.scope['user'].username and Game.objects.get(id=int(text_data_json['gameID'])).piecePositions[int(text_data_json['coordinate'])] == '0':


            # Join player group
            async_to_sync(self.channel_layer.group_add)(
                player_group,
                self.channel_name
            )

            try:

                async_to_sync(self.channel_layer.group_send)(
                        player_group,
                        {
                            'type': 'play',
                            'played_against': text_data_json['playedAgainst'],
                            'game_id': text_data_json['gameID'],
                            'coordinate': text_data_json['coordinate']
                        }
                )

                async_to_sync(self.channel_layer.group_discard)(
                    player_group,
                    self.channel_name
                )


            except ValueError:

                async_to_sync(self.channel_layer.group_discard)(
                    player_group,
                    self.channel_name
                )

                async_to_sync(self.channel_layer.group_send)(
                        self.player_group,
                        {
                            'type': 'play',
                            'played_against': text_data_json['playedAgainst'],
                            'game_id': text_data_json['gameID'],
                            'coordinate': text_data_json['coordinate']
                        }
                )
                




        elif Game.objects.get(id=int(text_data_json['gameID'])).movingPlayer.username == self.scope['user'].username and Game.objects.get(id=int(text_data_json['gameID'])).piecePositions[int(text_data_json['coordinate'])] != '0':
            self.send(text_data=json.dumps({
                'message': 'cannot play this position',
                'messageType': 'invalidPosition'
            }))

        
        else:
            self.send(text_data=json.dumps({
                'message': 'it is not your turn',
                'messageType': 'notYourTurn'
            }))

            


    def play(self, event):

        checker = checkPosition.Check()
        checker.checkPlayValidity()

        if event['played_against'] == self.scope['user'].username:
            self.send(text_data=json.dumps({
                'coordinatePlayed': event['coordinate'],
                'messageType': 'playedAgainstOpponent',
                'playedAgainst': event['played_against']
            }))
        else:
            self.send(text_data=json.dumps({
                'coordinatePlayed': event['coordinate'],
                'messageType': 'played',
                'playedAgainst': event['played_against']
            }))

        print(event['played_against'])
        


    
