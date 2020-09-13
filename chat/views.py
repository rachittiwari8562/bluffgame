import random
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from .models import Gameid
import json
# Create your views here.
generate=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
def index(request):
    if request.method=="GET":
        return render(request, 'index.html')
    elif request.method=="POST":
        post=request.POST
        if post['name']=="":
            print("/n//nenter name/n/n")
            return render(request, 'index.html')
        print(post)
        if post['action']=="create":
            gameid=Gameid()
            key=random.choice(generate)+random.choice(generate)+random.choice(generate)+random.choice(generate)+random.choice(generate)
            gameid.gid=key
            gameid.players=post['name']
            gameid.counting+="1"
            k=list(range(0,52))
            random.shuffle(k)
            gameid.decks=json.dumps(k)
            gameid.save()
            print('\n\nusercreated\n\n')
            print(key)
            return redirect(reverse('room',args=[key]))
        elif post['action']=="join":
            gameid=Gameid.objects.filter(gid=post['code'])
            if gameid:
                gameid=gameid[0]
                tally=gameid.players
                count = tally.count("\n")
                if count<3:
                    gameid.players+= "\n"+post['name']
                    gameid.counting+=str((int(gameid.counting[-1])+1))
                    gameid.save()
                    print("\n\nuseradded\n\n")
                    return redirect(reverse('room',args=[post['code']]))
                else:
                    print("\n\nLIMIT EXCEEDED\n\n")
                    return render(request, 'index.html',{'message':'~~~Room limit exceeded.Join another room'})
            else:
                print("not found")
                return render(request, 'index.html',{'message':'~~~Room not found . Enter correct room-code'})
def room(request, room_name):
    if Gameid.objects.filter(gid=room_name):
        gameid=Gameid.objects.filter(gid=room_name)[0]
        player=gameid.players.split("\n")
        val=int(gameid.counting[-1])
        sets=json.loads(gameid.decks)[13*(val-1):(13*val)]
        if request.method=="GET":
            return render(request,'lobby.html', {'room_name': room_name,'player':player[-1],'all_players':player[:-1],'ids':gameid.counting[-1],'sets':sets,'chance':'1','drawing':'0','check':'0','played':[],'master':1})
        else:
            print("none")
    else:
        return redirect(reverse('index'))