import zmq
import base64


def upload_image(image_path, image_id=None):
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    socket.send_json({"operation": "upload", "image_data": image_data, "image_id": image_id})
    response = socket.recv_json()
    return response


def retrieve_image(image_id, save_path):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    socket.send_json({"operation": "retrieve", "image_id": image_id})
    response = socket.recv_json()

    if response['status'] == 'success':
        image_data = base64.b64decode(response['image_data'])
        with open(save_path, 'wb') as image_file:
            image_file.write(image_data)
        return "Image retrieved and saved successfully."
    else:
        return "Error retrieving image."


def resize_image(image_id, width, height, save_path):
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    socket.send_json({"operation": "resize", "image_id": image_id, "width": width, "height": height})
    response = socket.recv_json()

    if response['status'] == 'success':
        image_data = base64.b64decode(response['image_data'])
        with open(save_path, 'wb') as image_file:
            image_file.write(image_data)
        return "Image resized and saved successfully."
    else:
        return "Error resizing image."
