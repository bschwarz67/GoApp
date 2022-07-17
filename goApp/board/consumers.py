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
        self.player_group = '%s_group' % self.scope['path'].split('/')[3]
        print(' joined player group %s_group' % self.scope['path'].split('/')[3])
        # Join player group
        async_to_sync(self.channel_layer.group_add)(
            self.player_group,
            self.channel_name
        )
        self.accept()
        



    def disconnect(self, close_code):
        #Leave challenge player group
        async_to_sync(self.channel_layer.group_discard)(
            self.player_group,
            self.channel_name
        )
    
    def send_play(self):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)


        if Game.objects.get(id=int(text_data_json['gameID'])).movingPlayer.username == self.scope['user'].username and Game.objects.get(id=int(text_data_json['gameID'])).piecePositions[int(text_data_json['coordinate'])] == '0':

            if self.scope['user'].username == Game.objects.get(id=int(text_data_json['gameID'])).whitePlayer.username:
                game = Game.objects.get(id=int(text_data_json['gameID']))
                print(game.piecePositions)
                game.piecePositions = Game.objects.get(id=int(text_data_json['gameID'])).piecePositions[:int(text_data_json['coordinate'])] + '1' + Game.objects.get(id=int(text_data_json['gameID'])).piecePositions[int(text_data_json['coordinate']) + 1:]
                game.save()
                print(game.piecePositions)
                

                checker = checkPosition.Check('2211111111110000000000000000000000000000000000000', 2, '1')
                checker.checkPlayValidity()
                #checker = checkPosition.Check('2211111111110000000000000000000000000000000000000', int(text_data_json['coordinate']), '1')
                #checker.checkPlayValidity()
            
            else:
                game = Game.objects.get(id=int(text_data_json['gameID']))
                print(game.piecePositions)
                game.piecePositions = Game.objects.get(id=int(text_data_json['gameID'])).piecePositions[:int(text_data_json['coordinate'])] + '2' + Game.objects.get(id=int(text_data_json['gameID'])).piecePositions[int(text_data_json['coordinate']) + 1:]
                game.save()
                print(game.piecePositions)

                checker = checkPosition.Check('2211111111110000000000000000000000000000000000000', 2, '2')
                checker.checkPlayValidity()
                #checker = checkPosition.Check('2211111111110000000000000000000000000000000000000', int(text_data_json['coordinate']), '2')
                #checker.checkPlayValidity()


            
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

            

    #add conditions so that only message will be returned if its one of the two playsers in the game, in the instance of multiple 
    #games with >2 players this could get messy
    def play(self, event):

        
        print("send back to sockets")
        if event['played_against'] == self.scope['user'].username:
            
            try:
                print('send to socket1')
                self.send(text_data=json.dumps({
                    'coordinatePlayed': event['coordinate'],
                    'messageType': 'playedAgainstOpponent',
                    'playedAgainst': event['played_against']
                }))
            except:
                print('err')
        else:
            try:
                print('send to socket2')
                self.send(text_data=json.dumps({
                    'coordinatePlayed': event['coordinate'],
                    'messageType': 'played',
                    'playedAgainst': event['played_against']
                }))
            except:
                print('err')
        print(event['played_against'])
        


    
