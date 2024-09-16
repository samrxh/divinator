import zmq
from random import choice

# Set up context and socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:7002")

six_sided_die = (b"6d-1.jpg", b"6d-2.jpg", b"6d-3.jpg", b"6d-4.jpg", b"6d-5.jpg", b"6d-6.jpg")

zodiac_die = (b"aries.jpg", b"taurus.jpg", b"gemini.jpg", b"cancer.jpg", b"leo.jpg", b"virgo.jpg", b"libra.jpg",
              b"scorpio.jpg", b"sagittarius.jpg", b"capricorn.jpg", b"aquarius.jpg", b"pisces.jpg")


# Receive request and send message
while True:
    request = socket.recv()
    print("Request received.")
    if request == b"6d":
        divination = choice(six_sided_die)
        socket.send(divination)
        print("Six-sided die response sent.")
    if request == b"zodiac":
        divination = choice(zodiac_die)
        socket.send(divination)
        print("Zodiac die response sent.")
