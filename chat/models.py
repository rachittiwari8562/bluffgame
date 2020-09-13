from django.db import models

# Create your models here.
class Gameid(models.Model):
    players=models.TextField()
    counting=models.TextField()
    gid=models.TextField()
    decks=models.TextField(null=True)
    chance=models.TextField(null=True)
    deck1=models.IntegerField(default=13)
    deck2=models.IntegerField(default=13)
    deck3=models.IntegerField(default=13)
    deck4=models.IntegerField(default=13)
    played=models.TextField()
    stock=models.TextField(null=True)
    passing=models.IntegerField(null=True)
    by=models.TextField(null=True)
    by2=models.TextField(null=True)
    typ=models.IntegerField(default=-1)