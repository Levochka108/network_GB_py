import socket
import threading
import logging

# Connection Data
HOST = '127.0.0.1'
PORT = 55555

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.FileHandler("/logs/server.log"),
                        logging.StreamHandler()
                    ])

logger = logging.getLogger(__name__)


# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except Exception as e:
            logger.error(f"An error occurred while broadcasting message: {e}")

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except Exception as e:
            # Removing And Closing Clients
            logger.error(f"An error occurred while handling client: {e}")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        try:
            # Accept Connection
            client, address = server.accept()
            logger.info("Connected with {}".format(str(address)))

            # Request And Store Nicknames
            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)
            clients.append(client)

            # Print And Broadcast Nickname
            logger.info("Nickname is {}".format(nickname))
            broadcast("{} joined!".format(nickname).encode('ascii'))
            client.send('Connected to server!'.encode('ascii'))

            # Start Handling Thread For Client
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except Exception as e:
            logger.error(f"An error occurred while accepting connection: {e}")

if __name__ == "__main__":
    try:
        logger.info("Server is listening...")
        receive()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
