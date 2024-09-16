import zmq
from random import choice

# Set up context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:7001")

cards = (b"cups01.jpg", b"cups02.jpg", b"cups03.jpg", b"cups04.jpg", b"cups05.jpg", b"cups06.jpg", b"cups07.jpg",
         b"cups08.jpg", b"cups09.jpg", b"cups10.jpg", b"cups11.jpg", b"cups12.jpg", b"cups13.jpg", b"cups14.jpg",
         b"swords01.jpg", b"swords02.jpg", b"swords03.jpg", b"swords04.jpg", b"swords05.jpg", b"swords06.jpg",
         b"swords07.jpg", b"swords08.jpg", b"swords09.jpg", b"swords10.jpg", b"swords11.jpg", b"swords12.jpg",
         b"swords13.jpg", b"swords14.jpg", b"wands01.jpg", b"wands02.jpg", b"wands03.jpg", b"wands04.jpg",
         b"wands05.jpg", b"wands06.jpg", b"wands07.jpg", b"wands08.jpg", b"wands09.jpg", b"wands10.jpg",
         b"wands11.jpg", b"wands12.jpg", b"wands13.jpg", b"wands14.jpg", b"pents01.jpg", b"pents02.jpg", b"pents03.jpg",
         b"pents04.jpg", b"pents05.jpg", b"pents06.jpg", b"pents07.jpg", b"pents08.jpg", b"pents09.jpg", b"pents10.jpg",
         b"pents11.jpg", b"pents12.jpg", b"pents13.jpg", b"pents14.jpg", b"maj00.jpg", b"maj01.jpg", b"maj02.jpg",
         b"maj03.jpg", b"maj04.jpg", b"maj05.jpg", b"maj06.jpg", b"maj07.jpg", b"maj08.jpg", b"maj09.jpg", b"maj10.jpg",
         b"maj11.jpg", b"maj12.jpg", b"maj13.jpg", b"maj14.jpg", b"maj15.jpg", b"maj16.jpg", b"maj17.jpg",
         b"maj18.jpg", b"maj19.jpg", b"maj20.jpg", b"maj21.jpg")


# Receive request and send message
while True:
    request = socket.recv()
    print("Request received.")
    if request == b"1":
        divination = choice(cards)
        socket.send(divination)
        print("One-card response sent.")
    if request == b"3":
        divination = choice(cards) + b" " + choice(cards) + b" " + choice(cards)
        socket.send(divination)
        print("Three-card response sent.")
