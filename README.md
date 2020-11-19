# Bluffgame
This is a django web app which uses websockets for game.
It is built upon the django-channels which is used for handling both asgi and wsgi requests.
A game room is built by a player which is stored in a sqlite3 database.
All the corresponding game states are stored in the same databse.
However the messages are not stored rather they are first they are temporaly collected in a redis database and then they are distributed to all clients in the same game room.
\nThe game is realtime based on websockets.
Here is the link of the same :-"https://itbluff.herokuapp.com/"
