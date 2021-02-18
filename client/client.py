from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread, Lock
import time

class Client:
    """
    for communication with server
    """
    # GLOBAL CONSTANTS
    HOST = "localhost"
    PORT = 8080
    ADDR = (HOST,PORT)
    BUFSIZE = 512

    def __init__(self,name):
        """
        Init object and send name to server
        :param name: str
        """
        self.client_socket = socket(AF_INET,SOCK_STREAM)
        self.client_socket.connect(self.ADDR)
        self.messages = [] # keep track of msgs
        receive_thread = Thread(target=self.receive_messages)
        receive_thread.start()
        self.send_message(name)
        self.lock = Lock()

    # Runs concurrently pinging to update msgs on this obj
    def receive_messages(self):
        """
        receive messages from server
        :return: None
        """
        while True:
            try:
                msg = self.client_socket.recv(self.BUFSIZE).decode()
                # make sure safe to access
                self.lock.acquire()
                self.messages.append(msg)
                self.lock.release()
            except Exception as e:
                print("[EXCEPTION]",e)
                break

    def send_message(self,msg):
        """
        send messages to server
        :param msg: str
        :return: None
        """
        self.client_socket.send(bytes(msg,"utf8"))
        if msg == "{quit}":
            self.client_socket.close()

    # interface for client
    def get_messages(self):
        """
        :returns a list of str messages
        :return: list[str]
        """

        messages_copy = self.messages[:]

        # make sure memory is safe to access
        self.lock.acquire()
        self.messages = []
        self.lock.release()
        return messages_copy

    def disconnect(self):
        self.send_message("{quit}")
    