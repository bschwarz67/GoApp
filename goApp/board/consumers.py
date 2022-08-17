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
        textDataJson = json.loads(text_data)
        coordinateInt = int(textDataJson['coordinate'])
        scopedUsername = self.scope['user'].username
        game = Game.objects.get(id=int(textDataJson['gameId']))
        player = Player.objects.get(username=scopedUsername)
        playedAgainst = textDataJson['playedAgainst']
        gameId = textDataJson['gameId']
        coordinate = textDataJson['coordinate']

        if game.movingPlayer.username == scopedUsername and game.piecePositions[coordinateInt] == '0':
            coordinatesTaken = []
            if scopedUsername == game.whitePlayer.username:

                opponent = game.blackPlayer

                checker = checkPosition.Check(game, player, coordinateInt, '1')
                result = checker.checkPlay()

                inverseChecker = checkPosition.Check(game, opponent, coordinateInt, '1')
                inverseResult = inverseChecker.checkPlay()

                
                if result[0] == False:
                    self.send(text_data=json.dumps({
                        'errorMessage': 'cannot play this position as it is a repeat position',
                        'messageType': 'invalidPosition'
                    }))
                elif len(inverseResult) > 1 and len(result) == 1:
                    self.send(text_data=json.dumps({
                        'errorMessage': 'cannot play this position as there are no liberties and no takes here',
                        'messageType': 'invalidPosition'
                    }))
                else:
                    checker.finalizeNewMove()
                    result.pop(0)
                    for x in result:
                        coordinateInt = 7 * int(list(x)[0]) + int(list(x)[1])
                        coordinatesTaken.append(coordinateInt)

                    jsonCoordinatesTaken = json.dumps(coordinatesTaken)
                    
                    async_to_sync(self.channel_layer.group_send)(
                        self.player_group,
                        {
                            'type': 'play',
                            'playedAgainst': playedAgainst,
                            'gameId': gameId,
                            'coordinatePlayed': coordinate,
                            'coordinatesTaken': jsonCoordinatesTaken
                        }
                    )
            
            else:

                opponent = game.whitePlayer

                checker = checkPosition.Check(game, player, coordinateInt, '2')
                result = checker.checkPlay()

                inverseChecker = checkPosition.Check(game, opponent, coordinateInt, '2')
                inverseResult = inverseChecker.checkPlay()

                
                if result[0] == False:
                    self.send(text_data=json.dumps({
                        'errorMessage': 'cannot play this position as it is a repeat position',
                        'messageType': 'invalidPosition'
                    }))
                elif len(inverseResult) > 1 and len(result) == 1:
                    self.send(text_data=json.dumps({
                        'errorMessage': 'cannot play this position as there are no liberties and no takes here',
                        'messageType': 'invalidPosition'
                    }))
                else:
                    checker.finalizeNewMove()
                    result.pop(0)
                    for x in result:
                        coordinateInt = 7 * int(list(x)[0]) + int(list(x)[1])
                        coordinatesTaken.append(coordinateInt)

                    jsonCoordinatesTaken = json.dumps(coordinatesTaken)
                    
                    async_to_sync(self.channel_layer.group_send)(
                        self.player_group,
                        {
                            'type': 'play',
                            'playedAgainst': playedAgainst,
                            'gameId': gameId,
                            'coordinatePlayed': coordinate,
                            'coordinatesTaken': jsonCoordinatesTaken
                        }
                    )



        elif game.movingPlayer.username == scopedUsername and game.piecePositions[coordinateInt] != '0':
            self.send(text_data=json.dumps({
                'errorMessage': 'cannot play this position as it is not an empty space',
                'messageType': 'invalidPosition'
            }))

        
        else:
            self.send(text_data=json.dumps({
                'errorMessage': 'it is not your turn',
                'messageType': 'notYourTurn'
            }))

            

    #havent tested cases where player is in one game but someone plays on them in another game, probably will temporarily change
    #thier board, have to write a check for this. need to check this
    def play(self, event):

        
        if event['playedAgainst'] == self.scope['user'].username:
            self.send(text_data=json.dumps({
                'coordinatePlayed': event['coordinatePlayed'],
                'messageType': 'playedAgainstOpponent',
                'playedAgainst': event['playedAgainst'],
                'coordinatesTaken': event['coordinatesTaken']
            }))
            
        else:
            self.send(text_data=json.dumps({
                'coordinatePlayed': event['coordinatePlayed'],
                'coordinatesTaken': event['coordinatesTaken'],
                'messageType': 'played',
                'playedAgainst': event['playedAgainst']
            }))
                    


    
