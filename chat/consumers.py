import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Gameid
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        gameid=Gameid.objects.filter(gid=text_data_json['gid'])[0]
        if 'message' in text_data_json:
            message = text_data_json['message']
            name = text_data_json['name']
            naam = text_data_json['naam']
            # Send message to room group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'name' :name,
                    'naam' :naam,
                }
            )
        if 'player' in text_data_json:
            player = text_data_json['player']
            #sending player name to group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'player_add',
                    'player': player
                }
            )
        if 'start' in text_data_json:
            #sending start-signal to group
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'start',
                }
            )
        if 'icon'  in text_data_json:
            #changing icon
                async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'icon',
                    'data':text_data_json
                }
            )
        if 'action' in text_data_json:
            if text_data_json['action']=="throw":
                if gameid.deck1==0 or gameid.deck2==0 or gameid.deck3==0 or gameid.deck4==0:
                    if gameid.deck1==0:
                        winner=gameid.players.split("\n")[0]
                        icon=1
                    elif gameid.deck2==0:
                        winner=gameid.players.split("\n")[1]
                        icon=2
                    elif gameid.deck3==0:
                        winner=gameid.players.split("\n")[2]
                        icon=3
                    elif gameid.deck4==0:
                        winner=gameid.players.split("\n")[3]
                        icon=4
                    gameid.delete()
                    async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                        {
                            'type': 'win',
                            'winner':winner,
                            'icon':icon
                        }
                        )
                else:
                    chance=text_data_json['chance']
                    gameid.passing=0
                    gameid.by=self.channel_name
                    gameid.by2=chance
                    if chance=="1":
                        gameid.deck1-=len(text_data_json['cards'])
                    elif chance=="2":
                        gameid.deck2-=len(text_data_json['cards'])
                    elif chance=="3":
                        gameid.deck3-=len(text_data_json['cards'])
                    else:
                        gameid.deck4-=len(text_data_json['cards'])
                    if gameid.played:
                        gameid.played=json.dumps(json.loads(gameid.played)+text_data_json['cards'])
                    else:
                        gameid.played=json.dumps(text_data_json['cards'])
                    gameid.stock=json.dumps(text_data_json['cards'])
                    chance =(int(chance))%4+1
                    gameid.chance=str(chance)
                    if gameid.typ==-1:
                        gameid.typ=text_data_json['typ']
                    gameid.save()
                #sending player name to group
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,

                        {
                            'type': 'action',
                            'state': text_data_json,
                            'chance': chance
                        }
                    )
            elif text_data_json['action']=="check":
                arr=json.loads(gameid.stock)
                arr2=json.loads(gameid.played)
                gameid.stock=""
                gameid.played=""
                oth=[]
                for i in arr:
                    oth.append(i%13)
                ch=[gameid.typ]*len(arr)
                gameid.typ=-1
                if ch==oth:
                    if gameid.deck1==0 or gameid.deck2==0 or gameid.deck3==0 or gameid.deck4==0:
                        if gameid.deck1==0:
                            winner=gameid.players.split("\n")[0]
                            icon=1
                        elif gameid.deck2==0:
                            winner=gameid.players.split("\n")[1]
                            icon=2
                        elif gameid.deck3==0:
                            winner=gameid.players.split("\n")[2]
                            icon=3
                        elif gameid.deck4==0:
                            winner=gameid.players.split("\n")[3]
                            icon=4
                        gameid.delete()
                        async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                            {
                                'type': 'win',
                                'winner':winner,
                                'icon':icon
                            }
                            )
                    else:
                        chance=gameid.chance
                        if chance=="1":
                            gameid.deck1+=len(arr2)
                        elif chance=="2":
                            gameid.deck2+=len(arr2)
                        elif chance=="3":
                            gameid.deck3+=len(arr2)
                        else:
                            gameid.deck4+=len(arr2)
                        self.send(text_data=json.dumps({
                            'take':"take",
                            'cards': arr2,
                        }))
                        async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type':'bluff',
                            'bluff':"no"
                        })
                else:
                    chance=str(gameid.by2)
                    gameid.chance=chance
                    if chance=="1":
                        gameid.deck1+=len(arr2)
                    elif chance=="2":
                        gameid.deck2+=len(arr2)
                    elif chance=="3":
                        gameid.deck3+=len(arr2)
                    else:
                        gameid.deck4+=len(arr2)
                    async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'take',
                        'cards': arr2,
                        'by':gameid.by,
                    })
                    async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'bluff',
                        'bluff':"yes"
                    })
                async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'changing',
                })
                async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'modify',
                    'chance':chance

                })
                gameid.save()
        if 'pass' in text_data_json:
            chance =(int(gameid.chance))%4+1
            gameid.chance=chance
            pas=gameid.passing
            if pas==3:
                if gameid.deck1==0 or gameid.deck2==0 or gameid.deck3==0 or gameid.deck4==0:
                    if gameid.deck1==0:
                        winner=gameid.players.split("\n")[0]
                        icon=1
                    elif gameid.deck2==0:
                        winner=gameid.players.split("\n")[1]
                        icon=2
                    elif gameid.deck3==0:
                        winner=gameid.players.split("\n")[2]
                        icon=3
                    elif gameid.deck4==0:
                        winner=gameid.players.split("\n")[3]
                        icon=4
                    gameid.delete()
                    async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                        {
                            'type': 'win',
                            'winner':winner,
                            'icon':icon
                        }
                        )
                else:
                    gameid.passing=0
                    gameid.played=""
                    gameid.played=""
                    gameid.typ=-1
                    async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                            'type':'changing',
                    })
            else:
                gameid.passing+=1
            gameid.save()
            async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                    'type':'modify',
                    'chance':chance,
                    'message':'passing'
            })







    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'name': event['name'],
            'naam':event['naam'],
        }))

    # Receive message from room group
    def player_add(self, event):
        player = event['player']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'player': player
        }))
    def start(self,event):
        self.send(text_data=json.dumps({
            'start': "start"}))
    def action(self, event):
        state  = event['state']
        action = state['action']
        if action == "throw":
            total=len(state['cards'])
            typ =state['typ']
            chance=event['chance']
            # Send message to WebSocket
            self.send(text_data=json.dumps({
                'chance':chance,
                'total':total,
                'typ':typ,
                'throwing':'1'
            }))
    def take(self,event):
        if event['by']==self.channel_name:
            self.send(text_data=json.dumps({
                            'take':"take",
                            'cards': event['cards'],
                        }))
    def changing(self,event):
        self.send(text_data=json.dumps({
            'changing':'changing',
            }))
    def modify(self,event):
        if 'message' in event:
            self.send(text_data=json.dumps({
                'modify':"modify",
                'chance':event['chance'],
                'passing':'passing',
                }))
        else:
            self.send(text_data=json.dumps({
                'modify':"modify",
                'chance':event['chance'],
                }))
    def bluff(self,event):
        self.send(text_data=json.dumps({
            'bluff':event['bluff']
        }))
    def win(self,event):
        self.send(text_data=json.dumps({
            'winner':event['winner'],
            'icon':event['icon']
        }))
    def icon(self,event):
        data=event['data']
        self.send(text_data=json.dumps({
            'by':data['by'],
            'icon':data['icon'],
            'changingicon':"1"
        }))