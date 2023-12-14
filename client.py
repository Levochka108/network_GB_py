import socket
import threading
import logging

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.nickname = input("Choose your nickname: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.client.connect((self.host, self.port))
            logging.info("Connected to server.")
        except Exception as e:
            logging.error(f"Error connecting to server: {e}")
            raise

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('ascii')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('ascii'))
                else:
                    print(message)
                    logging.info(message)
            except Exception as e:
                logging.error(f"An error occurred while receiving messages: {e}")
                self.client.close()
                break

    def send(self):
        while True:
            try:
                message = input('Your message: ')
                if message.lower() == 'exit':
                    break
                full_message = '{}: {}'.format(self.nickname, message)
                self.client.send(full_message.encode('ascii'))
            except Exception as e:
                logging.error(f"An error occurred while sending messages: {e}")
                self.client.close()
                break

    def start(self):
        try:
            self.connect_to_server()

            receive_thread = threading.Thread(target=self.receive)
            receive_thread.start()

            send_thread = threading.Thread(target=self.send)
            send_thread.start()

        except Exception as e:
            print(f"An error occurred! {e}")

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] %(message)s',
                        handlers=[
                            logging.FileHandler("client.log"),
                            logging.StreamHandler()
                        ])

    # Create and start the client
    chat_client = ChatClient('127.0.0.1', 55555)
    chat_client.start()
