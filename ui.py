import base64
from datetime import datetime
from PIL import Image, ImageTk
import os
from tkinter import Frame, Label, Button, Tk, Entry
import zmq
from zmq.utils import jsonapi

# Set up sockets
context = zmq.Context()
eight_ball_socket = context.socket(zmq.REQ)
eight_ball_socket.connect("tcp://localhost:7000")
tarot_socket = context.socket(zmq.REQ)
tarot_socket.connect("tcp://localhost:7001")
dice_socket = context.socket(zmq.REQ)
dice_socket.connect("tcp://localhost:7002")
history_socket = context.socket(zmq.REQ)
history_socket.connect("tcp://localhost:7003")
image_socket = context.socket(zmq.REQ)
image_socket.connect("tcp://localhost:5555")

# Set up pages
root = Tk()
home = Frame(root)
home.grid(row=0, column=0, sticky="news")
eight_ball = Frame(root)
eight_ball.grid(row=0, column=0, sticky="news")
tarot = Frame(root)
tarot.grid(row=0, column=0, sticky="news")
upload = Frame(root)
upload.grid(row=0, column=0, sticky="news")
dice = Frame(root)
dice.grid(row=0, column=0, sticky="news")
history = Frame(root)
history.grid(row=0, column=0, sticky="news")

# Home page
welcome = Label(home, text="Welcome to the divinator. Please select a divination method.")
welcome.pack()
eight_ball_button = Button(home, text="Eight-ball", command=eight_ball.tkraise)
eight_ball_button.pack()
tarot_button = Button(home, text="Tarot", command=tarot.tkraise)
tarot_button.pack()
dice_button = Button(home, text="Dice", command=dice.tkraise)
dice_button.pack()
helpful_tip = Label(home, text="You may generate a divination from any of these options by selecting the kind you "
                               "would like to use.")
helpful_tip.pack()
history_button = Button(home, text="History", command=history.tkraise)
history_button.pack()
history_tip = Label(home, text="You may view the history of your divinations by selecting the History option.")
history_tip.pack()


# Eight-ball page
def request_8ball():
    eight_ball_socket.send(b"req")
    print("Eight-ball request sent.")
    message = eight_ball_socket.recv()
    print("Eight-ball response received.")
    decoded_message = message.decode('utf-8')
    generate_8ball.config(text=decoded_message)
    history_entry = {'method': 'add', 'id': str(datetime.now()), 'data': decoded_message}
    history_socket.send(jsonapi.dumps(history_entry))
    print("History entry sent.")
    response = history_socket.recv()
    print(response)


generate_8ball = Label(eight_ball, text="Press the Generate button below to get a divination.")
generate_8ball.pack()
warning = Label(eight_ball, text="WARNING: After generating a divination, the previous divination will be lost.")
warning.pack()
req_8ball_button = Button(eight_ball, text="Generate", command=request_8ball)
req_8ball_button.pack()
home_button = Button(eight_ball, text="Home", command=home.tkraise)
home_button.pack()


# Tarot page
def request_1tarot():
    tarot_socket.send(b"1")
    print("Tarot (1 card) request sent.")
    image_name = tarot_socket.recv()
    print("Tarot (1 card) response received.")
    decoded_message = image_name.decode('utf-8')
    history_entry = jsonapi.dumps({'method': 'add', 'id': str(datetime.now()), 'data': decoded_message[:-4]})
    history_socket.send(history_entry)
    print("History entry sent.")
    response = history_socket.recv()
    print(response)

    curr_path = os.path.dirname(os.path.abspath(__file__))
    image_path = curr_path + "\\images\\" + decoded_message

    with Image.open(image_path) as image:
        photo = ImageTk.PhotoImage(image)
        generate_tarot1.config(image=photo)
        generate_tarot1.image = photo


def request_3tarot():
    tarot_socket.send(b"3")
    print("Tarot (3 cards) request sent.")
    message = tarot_socket.recv()
    print("Tarot (3 cards) response received.")
    decoded_message = message.decode('utf-8')
    cards = decoded_message.split()
    history_entry = jsonapi.dumps({'method': 'add', 'id': str(datetime.now()),
                                   'data': cards[0][:-4] + ", " + cards[1][:-4] + ", " + cards[2][:-4]})
    history_socket.send(history_entry)
    print("History entry sent.")
    response = history_socket.recv()
    print(response)

    curr_path = os.path.dirname(os.path.abspath(__file__))
    image_path1 = curr_path + "\\images\\" + cards[0]
    image_path2 = curr_path + "\\images\\" + cards[1]
    image_path3 = curr_path + "\\images\\" + cards[2]

    with Image.open(image_path1) as image1:
        photo1 = ImageTk.PhotoImage(image1)
        generate_tarot1.config(image=photo1)
        generate_tarot1.image = photo1
    with Image.open(image_path2) as image2:
        photo2 = ImageTk.PhotoImage(image2)
        generate_tarot2.config(image=photo2)
        generate_tarot2.image = photo2
    with Image.open(image_path3) as image3:
        photo3 = ImageTk.PhotoImage(image3)
        generate_tarot3.config(image=photo3)
        generate_tarot3.image = photo3


generate_tarot1 = Label(tarot, text="")
generate_tarot1.pack(side="left")
generate_tarot2 = Label(tarot, text="")
generate_tarot2.pack(side="left")
generate_tarot3 = Label(tarot, text="")
generate_tarot3.pack(side="left")
generate_tip = Label(tarot, text="Press either Generate button below to get a divination.")
generate_tip.pack()
warning = Label(tarot, text="WARNING: After generating a divination, the previous divination will be lost.")
warning.pack()
req_1tarot_button = Button(tarot, text="Generate 1 card", command=request_1tarot)
req_1tarot_button.pack()
req_3tarot_button = Button(tarot, text="Generate 3 cards", command=request_3tarot)
req_3tarot_button.pack()
upload_button = Button(tarot, text="Upload a tarot card", command=upload.tkraise)
upload_button.pack()
home_button = Button(tarot, text="Home", command=home.tkraise)
home_button.pack()


# Upload page
def upload_image(image_id):
    with open(image_id + ".jpg", 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    image_socket.send_json({"operation": "upload", "image_data": image_data, "image_id": image_id})
    print("Image upload request sent.")
    response = image_socket.recv_json()
    print("Image upload response received.")
    print(response)
    return response


upload_tip = Label(upload, text="Type the image name below to upload a tarot card.")
upload_tip.pack()
convention_tip = Label(upload, text="Naming: Major (majXX), Wands (wandsXX), Pentacles (pentsXX), Swords (swordsXX), "
                                    "Cups (cupsXX).")
convention_tip.pack()
upload_entry = Entry(upload)
upload_entry.pack()
upload_button = Button(upload, text="Upload", command=lambda: upload_image(upload_entry.get()))
upload_button.pack()
home_button = Button(upload, text="Home", command=home.tkraise)
home_button.pack()


# Dice page
def request_6d():
    dice_socket.send(b"6d")
    print("Six-sided die request sent.")
    image_name = dice_socket.recv()
    print("Six-sided die response received.")
    decoded_message = image_name.decode('utf-8')
    history_entry = jsonapi.dumps({'method': 'add', 'id': str(datetime.now()), 'data': decoded_message[:-4]})
    history_socket.send(history_entry)
    print("History entry sent.")
    response = history_socket.recv()
    print(response)

    curr_path = os.path.dirname(os.path.abspath(__file__))
    image_path = curr_path + "\\images\\" + decoded_message

    with Image.open(image_path) as image:
        photo = ImageTk.PhotoImage(image)
        die_roll.config(image=photo)
        die_roll.image = photo


def request_zodiac():
    dice_socket.send(b"zodiac")
    print("Zodiac die request sent.")
    image_name = dice_socket.recv()
    print("Zodiac die response received.")
    decoded_message = image_name.decode('utf-8')
    history_entry = jsonapi.dumps({'method': 'add', 'id': str(datetime.now()), 'data': decoded_message[:-4]})
    history_socket.send(history_entry)
    print("History entry sent.")
    response = history_socket.recv()
    print(response)

    curr_path = os.path.dirname(os.path.abspath(__file__))
    image_path = curr_path + "\\images\\" + decoded_message

    with Image.open(image_path) as image:
        photo = ImageTk.PhotoImage(image)
        die_roll.config(image=photo)
        die_roll.image = photo


die_roll = Label(dice, text="")
die_roll.pack(side="left")
generate_dice = Label(dice, text="Press either Roll button below to get a divination.")
generate_dice.pack()
warning = Label(dice, text="WARNING: After generating a divination, the previous divination will be lost.")
warning.pack()
req_6d_button = Button(dice, text="Roll six-sided die", command=request_6d)
req_6d_button.pack()
req_zodiac_button = Button(dice, text="Roll zodiac die", command=request_zodiac)
req_zodiac_button.pack()
home_button = Button(dice, text="Home", command=home.tkraise)
home_button.pack()


# History page
def request_history():
    request = jsonapi.dumps({'method': 'list'})
    history_socket.send(request)
    print("History request sent.")
    message = history_socket.recv()
    print("History response received.")
    history_entries = jsonapi.loads(message)
    full_history = ""
    if history_entries:
        for key in history_entries:
            history_entry = jsonapi.dumps({'method': 'get', 'id': key})
            history_socket.send(history_entry)
            message = history_socket.recv()
            decoded_message = message.decode('utf-8')
            full_history += key + ": " + decoded_message + "\n"
    else:
        full_history = "No history."
    generate_history.config(text=full_history)


def clear_history():
    history_entry = jsonapi.dumps({'method': 'clear'})
    history_socket.send(history_entry)
    print("History clear request sent.")
    history_socket.recv()
    print("History clear response received.")
    generate_history.config(text="History cleared.")


generate_history = Label(history, text="Get your divination history by pressing the button below.")
generate_history.pack()
clear_history_button = Button(history, text="Clear history", command=clear_history)
clear_history_button.pack()
req_history_button = Button(history, text="Get history", command=request_history)
req_history_button.pack()
home_button = Button(history, text="Home", command=home.tkraise)
home_button.pack()


# Start on home page
home.tkraise()
root.title("divinator")
root.mainloop()
