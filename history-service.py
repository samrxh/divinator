import zmq
from zmq.utils import jsonapi


class HistoryService:
    def __init__(self):
        self.history = {}

    def add_entry(self, history_id, data):
        self.history[history_id] = data
        print(f"Added entry {history_id}: {data}")

    def list_entries(self):
        print("Listing entries.")
        return self.history

    def get_entry_data(self, history_id):
        print(f"Retrieving data for entry {history_id}.")
        return self.history[history_id]

    def run(self):
        # Set up context and socket
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:7003")

        while True:
            message = socket.recv()
            print("Request received.")
            request = jsonapi.loads(message)

            if request['method'] == 'add':
                self.add_entry(request['id'], request['data'])
                response = {'status': 'OK'}
                print("Entry added.")

            elif request['method'] == 'list':
                response = self.list_entries()
                print("Entries listed.")

            elif request['method'] == 'get':
                response = self.get_entry_data(request['id'])
                print("Entry data retrieved.")

            elif request['method'] == 'clear':
                self.history = {}
                response = {'status': 'OK'}
                print("History cleared.")

            else:
                response = {'status': 'error', 'message': 'Invalid request'}
            socket.send(jsonapi.dumps(response))
            print("Response sent.")


if __name__ == '__main__':
    HistoryService().run()
