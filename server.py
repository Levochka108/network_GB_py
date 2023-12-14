import socket
import threading
import logging

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicknames = []

    def start(self):
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
            logger.info("Server is listening on {}:{}".format(self.host, self.port))
            self.receive_connections()
        except Exception as e:
            logger.error(f"An error occurred while starting the server: {e}")
            raise

    def broadcast(self, message, client):
        for c in self.clients:
            if c != client:
                try:
                    c.send(message)
                except Exception as e:
                    logger.error(f"An error occurred while broadcasting message: {e}")

    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                self.broadcast(message, client)
            except Exception as e:
                logger.error(f"An error occurred while handling client: {e}")
                index = self.clients.index(client)
                self.remove_client(client, index)
                break

    def receive_connections(self):
        while True:
            try:
                client, address = self.server.accept()
                logger.info("Connected with {}".format(str(address)))

                client.send('NICK'.encode('ascii'))
                nickname = client.recv(1024).decode('ascii')
                self.nicknames.append(nickname)
                self.clients.append(client)

                logger.info("Nickname '{}' joined!".format(nickname))
                self.broadcast("{} joined!".format(nickname).encode('ascii'), client)
                client.send('Connected to server!'.encode('ascii'))

                thread = threading.Thread(target=self.handle_client, args=(client,))
                thread.start()
            except Exception as e:
                logger.error(f"An error occurred while accepting connection: {e}")

    def remove_client(self, client, index):
        try:
            nickname = self.nicknames[index]
            self.broadcast('{} left!'.format(nickname).encode('ascii'), client)
            self.nicknames.remove(nickname)
            self.clients.remove(client)
            client.close()
        except Exception as e:
            logger.error(f"An error occurred while removing client: {e}")

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=[
                            logging.FileHandler("server.log"),
                            logging.StreamHandler()
                        ])
    logger = logging.getLogger(__name__)
    # Create and start the server
    chat_server = ChatServer('127.0.0.1', 55555)
    chat_server.start()
