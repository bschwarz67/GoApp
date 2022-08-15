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

        self.player_name = self.scope['user']
        self.player_group = '%s_challenge_group' % self.player_name
        print(self.player_group)
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
        text_data_json = json.loads(text_data)
        if text_data_json['messageType'] != 'createNewPlayer':
            acting_player = self.scope['user'].username
            player_group = text_data_json['message']
            player_group += "_challenge_group"
            #connect to player group
            async_to_sync(self.channel_layer.group_add)(
                player_group,
                self.channel_name
            )

            if text_data_json['messageType'] == 'accept':
                # Send accept message to both players involved
                newGame = Game()
                newGame.whitePlayer = Player.objects.get(username=acting_player)
                newGame.blackPlayer = Player.objects.get(username=text_data_json['message'])
                newGame.movingPlayer = Player.objects.get(username=acting_player)
                newGame.save()
                Player.objects.get(username=text_data_json['message']).challengedPlayers.remove(Player.objects.get(username=acting_player))
                Player.objects.get(username=text_data_json['message']).opponents.add(Player.objects.get(username=acting_player))
                Player.objects.get(username=acting_player).opponents.add(Player.objects.get(username=text_data_json['message']))
                Player.objects.get(username=acting_player).challengingPlayers.remove(Player.objects.get(username=text_data_json['message']))
                async_to_sync(self.channel_layer.group_send)(
                    player_group,
                    {
                        'type': 'accept_player',
                        'accepting_player': acting_player,
                        'accepted_player': text_data_json['message'],
                        'new_game_id': newGame.id
                    }
                )
            else:
                
                Player.objects.get(username=text_data_json['message']).challengingPlayers.add(Player.objects.get(username=acting_player))
                Player.objects.get(username=acting_player).challengedPlayers.add(Player.objects.get(username=text_data_json['message']))
                
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
        else:
            if(Player.objects.filter(username=text_data_json['possibleNewPlayer']).exists()):
                if(self.scope['user'].is_authenticated):
                    if(self.scope['user'].username == text_data_json['possibleNewPlayer']):
                        Player.objects.get(username=self.scope['user'].username).save()        
                    else:
                        Player.objects.get(username=text_data_json['possibleNewPlayer']).save()
                else:
                    pass
            else:
                if(self.scope['user'].is_authenticated):
                    updatedPlayer = Player.objects.get(username=self.scope['user'].username)
                    #updatedPlayer.username = request.POST['name']
                    updatedPlayer.save()
                else:
                    sessionObject = self.scope['session']
                    newPlayerUsername = text_data_json['possibleNewPlayer']
                    newPlayer = Player(username=newPlayerUsername)
                    newPlayer.save()
                    async_to_sync(login)(self.scope, newPlayer)
                    self.scope['session']['test'] = 'test'
                    self.scope['session'].save()
                    async_to_sync(self.channel_layer.group_discard)(
                        self.player_group,
                        self.channel_name
                    )
                    self.player_name = self.scope['user']
                    self.player_group = '%s_challenge_group' % self.player_name

                    async_to_sync(self.channel_layer.group_add)(
                        self.player_group,
                        self.channel_name
                    )

                    async_to_sync(self.channel_layer.group_send)(
                        self.player_group,
                        {
                            'type': 'display_new_player',
                            'new_player_username': newPlayer.username,
                            'ws_event_for_scoped_user': 'True',
                        }
                    )

                    for player in Player.objects.all():
                        timeSinceLastOutOfGameAction = timezone.now() - player.lastOutOfGameAction
                        if timeSinceLastOutOfGameAction.days < 1:
                            if timeSinceLastOutOfGameAction.seconds <= 1200 and not player.username == newPlayer.username:
                                player_group = player.username
                                player_group += "_challenge_group"
                                #connect to player group
                                async_to_sync(self.channel_layer.group_add)(
                                    player_group,
                                    self.channel_name
                                )
                                async_to_sync(self.channel_layer.group_send)(
                                    player_group,
                                    {
                                        'type': 'display_new_player',
                                        'new_player_username': newPlayer.username,
                                        'ws_event_for_scoped_user': 'False',
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
                            'type': 'display_new_player',
                            'new_player_username': newPlayer.username,
                            'ws_event_for_scoped_user': 'False',
                        }
                    )
                    async_to_sync(self.channel_layer.group_discard)(
                        player_group,
                        self.channel_name
                    )

                    
                    
    #send new player to everyone still in the arena the update the available players
    def display_new_player(self, event):
        if event['ws_event_for_scoped_user'] == 'True':
            self.send(text_data=json.dumps({
                    'message': event['new_player_username'],
                    'messageType': 'new_player',
                    'addToPossibleOpponents': 'False',
            }))
        else:
            if event['new_player_username'] != self.scope['user'].username:
                self.send(text_data=json.dumps({
                    'message': event['new_player_username'],
                    'messageType': 'new_player',
                    'addToPossibleOpponents': 'True',
                }))

    # Receive message from accepting player
    def accept_player(self, event):
        accepting_player = event['accepting_player']
        accepted_player = event['accepted_player']
        new_game_id = event['new_game_id']
        username = self.scope['user'].username

        if (username == accepted_player):
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'message': accepting_player,
                'messageType': 'accept',
                'gameId': new_game_id
            }))
        else:
            if username == accepting_player:
                # Send message to WebSocket
                self.send(text_data=json.dumps({
                    'message': accepted_player,
                    'messageType': 'accept',
                    'gameId': new_game_id
                }))

    

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
        




