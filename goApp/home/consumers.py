import json
from asgiref.sync import async_to_sync
from channels.auth import login
#from django.contrib.auth import login
from channels.generic.websocket import WebsocketConsumer
from home.models import Player
from board.models import Game
from django.utils import timezone

class ChallengeConsumer(WebsocketConsumer):
    def connect(self):

        self.player_group = '%s_challenge_group' % self.scope['user']
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
        if self.scope['session'].has_key('test'):
            print(self.scope['session']['test'])
        else:
            print('not saved')
        textDataJson = json.loads(text_data)
        if textDataJson['messageType'] != 'createNewPlayer':

            selectedPlayer = Player.objects.get(username=textDataJson['selectedPlayer'])
            actingPlayer = Player.objects.get(username=self.scope['user'].username)

            player_group = '%s_challenge_group' % selectedPlayer.username
            #connect to player group
            async_to_sync(self.channel_layer.group_add)(
                player_group,
                self.channel_name
            )

            if textDataJson['messageType'] == 'accept':
                # Send accept message to both players involved
                newGame = Game()
                newGame.whitePlayer = actingPlayer
                newGame.blackPlayer = selectedPlayer
                newGame.movingPlayer = actingPlayer
                newGame.save()
                selectedPlayer.challengedPlayers.remove(actingPlayer)
                selectedPlayer.opponents.add(actingPlayer)
                if selectedPlayer.challengingPlayers.contains(actingPlayer):
                    selectedPlayer.challengingPlayers.remove(actingPlayer)
                actingPlayer.opponents.add(selectedPlayer)
                actingPlayer.challengingPlayers.remove(selectedPlayer)
                if actingPlayer.challengedPlayers.contains(selectedPlayer):
                    actingPlayer.challengedPlayers.remove(selectedPlayer)

                async_to_sync(self.channel_layer.group_send)(
                    player_group,
                    {
                        'type': 'acceptPlayer',
                        'acceptingPlayer': actingPlayer.username,
                        'acceptedPlayer': selectedPlayer.username,
                        'newGameId': newGame.id
                    }
                )
            else:
                
                selectedPlayer.challengingPlayers.add(actingPlayer)
                actingPlayer.challengedPlayers.add(selectedPlayer)
                
                # Send challenge message to challenged player
                async_to_sync(self.channel_layer.group_send)(
                    player_group,
                    {
                        'type': 'challengePlayer',
                        'challengingPlayer': actingPlayer.username,
                        'challengedPlayer' : selectedPlayer.username
                    }
                )


            #get out of group the player you just challenged
            async_to_sync(self.channel_layer.group_discard)(
                player_group,
                self.channel_name
            )
        else:
            possibleNewPlayer = textDataJson['possibleNewPlayer']
            if(Player.objects.filter(username=possibleNewPlayer).exists()):
                if(self.scope['user'].is_authenticated):
                    if(self.scope['user'].username == possibleNewPlayer):
                        Player.objects.get(username=self.scope['user'].username).save()        
                    else:
                        Player.objects.get(username=possibleNewPlayer).save()
                else:
                    pass
            else:
                if(self.scope['user'].is_authenticated):
                    updatedPlayer = Player.objects.get(username=self.scope['user'].username)
                    #updatedPlayer.username = request.POST['name']
                    updatedPlayer.save()
                else:
                    sessionObject = self.scope['session']
                    newPlayerUsername = possibleNewPlayer
                    newPlayer = Player(username=newPlayerUsername)
                    newPlayer.save()
                    async_to_sync(login)(self.scope, newPlayer)
                    self.scope['session']['test'] = 'test'
                    self.scope['session'].save()
                    async_to_sync(self.channel_layer.group_discard)(
                        self.player_group,
                        self.channel_name
                    )

                    self.player_group = '%s_challenge_group' % self.scope['user']

                    async_to_sync(self.channel_layer.group_add)(
                        self.player_group,
                        self.channel_name
                    )

                    async_to_sync(self.channel_layer.group_send)(
                        self.player_group,
                        {
                            'type': 'displayNewPlayer',
                            'newPlayerUsername': newPlayer.username,
                            'wsEventForScopedUser': 'True',
                        }
                    )

                    for player in Player.objects.all():
                        timeSinceLastOutOfGameAction = timezone.now() - player.lastOutOfGameAction
                        if timeSinceLastOutOfGameAction.days < 1:
                            if timeSinceLastOutOfGameAction.seconds <= 1200 and not player.username == newPlayer.username:
                                player_group = '%s_challenge_group' % player.username
                                #connect to player group
                                async_to_sync(self.channel_layer.group_add)(
                                    player_group,
                                    self.channel_name
                                )
                                async_to_sync(self.channel_layer.group_send)(
                                    player_group,
                                    {
                                        'type': 'displayNewPlayer',
                                        'newPlayerUsername': newPlayer.username,
                                        'wsEventForScopedUser': 'False',
                                    }
                                )
                                async_to_sync(self.channel_layer.group_discard)(
                                    player_group,
                                    self.channel_name
                                )
                    player_group = "AnonymousUser_challenge_group"

                    async_to_sync(self.channel_layer.group_add)(
                        player_group,
                        self.channel_name
                    )
                    async_to_sync(self.channel_layer.group_send)(
                        player_group,
                        {
                            'type': 'displayNewPlayer',
                            'newPlayerUsername': newPlayer.username,
                            'wsEventForScopedUser': 'False',
                        }
                    )
                    async_to_sync(self.channel_layer.group_discard)(
                        player_group,
                        self.channel_name
                    )

                    
                    
    #send new player to everyone still in the arena the update the available players
    def displayNewPlayer(self, event):
        if event['wsEventForScopedUser'] == 'True':
            self.send(text_data=json.dumps({
                    'newPlayerUsername': event['newPlayerUsername'],
                    'messageType': 'newPlayer',
                    'addToPossibleOpponents': 'False',
            }))
        else:
            if event['newPlayerUsername'] != self.scope['user'].username:
                self.send(text_data=json.dumps({
                    'newPlayerUsername': event['newPlayerUsername'],
                    'messageType': 'newPlayer',
                    'addToPossibleOpponents': 'True',
                }))

    # Receive message from accepting player
    def acceptPlayer(self, event):
        acceptingPlayer = event['acceptingPlayer']
        acceptedPlayer = event['acceptedPlayer']
        newGameId = event['newGameId']
        username = self.scope['user'].username

        if (username == acceptedPlayer):
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'newOpponent': acceptingPlayer,
                'messageType': 'accept',
                'gameId': newGameId
            }))
        else:
            if username == acceptingPlayer:
                # Send message to WebSocket
                self.send(text_data=json.dumps({
                    'newOpponent': acceptedPlayer,
                    'messageType': 'accept',
                    'gameId': newGameId
                }))

    

    # Receive message from challenging player
    def challengePlayer(self, event):
        challengingPlayer = event['challengingPlayer']
        challengedPlayer = event['challengedPlayer']
        username = self.scope['user'].username

        if (username == challengedPlayer):
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'challengingPlayer': challengingPlayer,
                'messageType': 'challenge'
            }))
        




