import json
import random
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from home.models import Player
from board.models import Game
import sys
sys.path.append('/Users/bryan/desktop/personalCodeRepo/goapp/goapp/board')
sys.path.append('/app/goApp/board')
sys.append('/opt/render/project/src/goApp/board')
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
                    if opponent.username == 'demo':
                        availableCoordinates = []
                        checker.finalizeNewMove()
                        result.pop(0)
                        for x in result:
                            coordinateInt = 7 * int(list(x)[0]) + int(list(x)[1])
                            coordinatesTaken.append(coordinateInt)
                        jsonCoordinatesTaken = json.dumps(coordinatesTaken)


                        for x in range(len(game.piecePositions)):
                            if game.piecePositions[x] == '0':
                                availableCoordinates.append(x)


                        validPlayFound = False


                        while len(availableCoordinates) != 0 and validPlayFound == False:
                            coordinateComputer = random.choice(availableCoordinates)
                            coordinateIntComputer = int(coordinateComputer)
                            checker = checkPosition.Check(game, opponent, coordinateIntComputer, '2')
                            result = checker.checkPlay()
                            inverseChecker = checkPosition.Check(game, player, coordinateIntComputer, '2')
                            inverseResult = inverseChecker.checkPlay()

                            if result[0] == False or (len(inverseResult) > 1 and len(result) == 1):
                                availableCoordinates.remove(coordinateComputer)
                            else:
                                validPlayFound = True
                            
                        if validPlayFound == True:
                            coordinatesTakenComputer = []
                            checker.finalizeNewMove()
                            result.pop(0)
                            for x in result:
                                coordinateIntComputer = 7 * int(list(x)[0]) + int(list(x)[1])
                                coordinatesTakenComputer.append(coordinateIntComputer)

                            jsonCoordinatesTakenComputer = json.dumps(coordinatesTakenComputer)
                            
                            async_to_sync(self.channel_layer.group_send)(
                                self.player_group,
                                {
                                    'type': 'play',
                                    'playedAgainst': playedAgainst,
                                    'gameId': gameId,
                                    'coordinatePlayed': coordinate,
                                    'coordinatesTaken': jsonCoordinatesTaken,
                                    'coordinatePlayedComputer': coordinateComputer,
                                    'coordinatesTakenComputer': jsonCoordinatesTakenComputer
                                }
                            )
                        else:
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

            

    
    def play(self, event):

        
        if event['playedAgainst'] == self.scope['user'].username:
            self.send(text_data=json.dumps({
                'coordinatePlayed': event['coordinatePlayed'],
                'messageType': 'playedAgainstOpponent',
                'playedAgainst': event['playedAgainst'],
                'coordinatesTaken': event['coordinatesTaken'],
            }))
            
        else:
            if 'coordinatePlayedComputer' in event and 'coordinatesTakenComputer' in event:
                self.send(text_data=json.dumps({
                    'coordinatePlayed': event['coordinatePlayed'],
                    'coordinatesTaken': event['coordinatesTaken'],
                    'messageType': 'played',
                    'playedAgainst': event['playedAgainst'],
                    'coordinatePlayedComputer': event['coordinatePlayedComputer'],
                    'coordinatesTakenComputer': event['coordinatesTakenComputer']
                }))
            else:
                self.send(text_data=json.dumps({
                    'coordinatePlayed': event['coordinatePlayed'],
                    'coordinatesTaken': event['coordinatesTaken'],
                    'messageType': 'played',
                    'playedAgainst': event['playedAgainst'],
                }))
                    


    
