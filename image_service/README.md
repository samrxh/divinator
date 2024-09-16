# Request Data from the microservice
1- Set up ZeroMQ communication by establishing a ZeroMQ connection to the microservice server, and use the appropriate socket type (REQ) to send the requests.
2- Craft and Send request messages by creating a JSON formatted messages specifing the operation(upload, retrieve, resize) and any other parameters (image ID, width, height...) , and send the request messages using the ZeroMQ socket to the server of the microservice.
3- Handle server responses by receiving them using the ZeroMQ socket from the server, and parse the response JSON to extract the relevant data.
4- Process responses accordingly by checking the status of the response to know whether there was an error or the request was successfull, and handle the received data accordingly.

# Example Call
import zmq
import base64

def upload_image(image_path):
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    socket.send_json({"operation": "upload", "image_data": image_data})
    response = socket.recv_json()
    return response

if __name__ == '__main__':
    upload_response = upload_image('path/to/your/image.png')
    print(upload_response)


# Receiving Data from the microservice
1- Set up ZeroMQ communication by establishing a ZeroMQ connection to the microservice server, and use the appropriate socket type (REQ) to receive the requests and send responses.
2- Listen for the incoming requests from clients using the ZeroMQ socket.
3- Process the incoming requests by receiving them from clients, and parse the request JSON in order to extract any parameters.
4- Handle the requests by processing them based on the operation(upload, retrieve, resize), and generate response messages that contain the requested data.
5- Send response messages back using the ZeroMQ socket to the requesting clients.

# Example Call
import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    message = socket.recv_json()
    operation = message['operation']
    
    if operation == 'upload':
        response = {'status': 'success', 'message': 'Image uploaded successfully'}
    elif operation == 'retrieve':
        response = {'status': 'success', 'image_data': 'base64_encoded_image_data'}
    elif operation == 'resize':
        response = {'status': 'success', 'image_data': 'base64_encoded_resized_image_data'}
    else:
        response = {'status': 'error', 'message': 'Invalid operation'}
    
    socket.send_json(response)


    
![UML diagram](https://github.com/aldehaim/CS361/assets/166167699/03242630-5410-45d5-9b2e-12e570de8ca2)
