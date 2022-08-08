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
        coordinate = int(text_data_json['coordinate'])
        scopedUsername = self.scope['user'].username
        game = Game.objects.get(id=int(text_data_json['gameID']))
        player = Player.objects.get(username=scopedUsername)
        

        if game.movingPlayer.username == scopedUsername and game.piecePositions[coordinate] == '0':
            coordinatesTaken = []
            if scopedUsername == game.whitePlayer.username:

                opponent = game.blackPlayer

                checker = checkPosition.Check(game, player, coordinate, '1')
                result = checker.checkPlay()

                inverseChecker = checkPosition.Check(game, opponent, coordinate, '1')
                inverseResult = inverseChecker.checkPlay()

                
                if result[0] == False:
                    self.send(text_data=json.dumps({
                        'message': 'cannot play this position as it is a repeat position',
                        'message_type': 'invalid_position'
                    }))
                elif len(inverseResult) > 1 and len(result) == 1:
                    self.send(text_data=json.dumps({
                        'message': 'cannot play this position as there are no liberties and no takes here',
                        'message_type': 'invalid_position'
                    }))
                else:
                    checker.finalizeNewMove()
                    result.pop(0)
                    for x in result:
                        coordinate = 7 * int(list(x)[0]) + int(list(x)[1])
                        coordinatesTaken.append(coordinate)

                    JSONcoordinatesTaken = json.dumps(coordinatesTaken)
                    
                    async_to_sync(self.channel_layer.group_send)(
                        self.player_group,
                        {
                            'type': 'play',
                            'played_against': text_data_json['playedAgainst'],
                            'game_id': text_data_json['gameID'],
                            'coordinate_played': text_data_json['coordinate'],
                            'coordinates_taken': JSONcoordinatesTaken
                        }
                    )
            
            else:

                opponent = game.whitePlayer

                checker = checkPosition.Check(game, player, coordinate, '2')
                result = checker.checkPlay()

                inverseChecker = checkPosition.Check(game, opponent, coordinate, '2')
                inverseResult = inverseChecker.checkPlay()

                
                if result[0] == False:
                    self.send(text_data=json.dumps({
                        'message': 'cannot play this position as it is a repeat position',
                        'message_type': 'invalid_position'
                    }))
                elif len(inverseResult) > 1 and len(result) == 1:
                    self.send(text_data=json.dumps({
                        'message': 'cannot play this position as there are no liberties and no takes here',
                        'message_type': 'invalid_position'
                    }))
                else:
                    checker.finalizeNewMove()
                    result.pop(0)
                    for x in result:
                        coordinate = 7 * int(list(x)[0]) + int(list(x)[1])
                        coordinatesTaken.append(coordinate)

                    JSONcoordinatesTaken = json.dumps(coordinatesTaken)
                    
                    async_to_sync(self.channel_layer.group_send)(
                        self.player_group,
                        {
                            'type': 'play',
                            'played_against': text_data_json['playedAgainst'],
                            'game_id': text_data_json['gameID'],
                            'coordinate_played': text_data_json['coordinate'],
                            'coordinates_taken': JSONcoordinatesTaken
                        }
                    )



        elif game.movingPlayer.username == scopedUsername and game.piecePositions[coordinate] != '0':
            self.send(text_data=json.dumps({
                'message': 'cannot play this position as it is not an empty space',
                'message_type': 'invalid_position'
            }))

        
        else:
            self.send(text_data=json.dumps({
                'message': 'it is not your turn',
                'message_type': 'not_your_turn'
            }))

            

    #havent tested cases where player is in one game but someone plays on them in another game, probably will temporarily change
    #thier board, have to write a check for this. need to check this
    def play(self, event):

        
        if event['played_against'] == self.scope['user'].username:
            self.send(text_data=json.dumps({
                'coordinate_played': event['coordinate_played'],
                'message_type': 'played_against_opponent',
                'played_against': event['played_against'],
                'coordinates_taken': event['coordinates_taken']
            }))
            
        else:
            self.send(text_data=json.dumps({
                'coordinate_played': event['coordinate_played'],
                'coordinates_taken': event['coordinates_taken'],
                'message_type': 'played',
                'played_against': event['played_against']
            }))
                    


    
