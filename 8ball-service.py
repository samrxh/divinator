import zmq
from random import choice

# Set up context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:7000")

divinations = (b"it is certain", b"it is decidedly so", b"without a doubt", b"yes definitely", b"you may rely on it",
               b"as i see it, yes", b"most likely", b"outlook good", b"yes", b"signs point to yes",
               b"reply hazy, try again", b"ask again later", b"better not tell you now", b"cannot predict now",
               b"concentrate and ask again", b"don't count on it", b"my reply is no", b"my sources say no",
               b"outlook not so good", b"very doubtful")

# Receive request and send message
while True:
    request = socket.recv()
    print("Request received.")
    divination = choice(divinations)
    socket.send(divination)
    print("Response sent.")
