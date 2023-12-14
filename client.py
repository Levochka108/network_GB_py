import socket
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    handlers=[
                        logging.FileHandler("logs/client.log"),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger(__name__)

# Choosing Nickname
nickname = input("Choose your nickname: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
                logger.info(message)
        except Exception as e:
            # Close Connection When Error
            logger.error(f"An error occurred: {e}")
            client.close()
            break

def write():
    while True:
        try:
            message = '{}: {}'.format(nickname, input(''))
            client.send(message.encode('ascii'))
        except Exception as e:
            logger.error(f"An error occurred while sending message: {e}")

# Starting Threads For Listening And Writing
if __name__ == '__main__':
    try:
        receive_thread = threading.Thread(target=receive)
        receive_thread.start()

        write_thread = threading.Thread(target=write)
        write_thread.start()
    except Exception as e:
        logger.error(f"An error occurred while starting threads: {e}")
