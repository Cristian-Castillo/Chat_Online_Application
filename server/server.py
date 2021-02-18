""" Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 8080
ADDR = (HOST,PORT)
MAX_CONNECTIONS = 10
BUFSIZE = 512

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR) # set up server


def broadcast(msg,name):
    """
    send new messages to all clients
    :param msg: bytes["utf8"]
    :param name: str
    :return:
    """
    for person in persons:
        client = person.client
        client.send(bytes(name, "utf8") + msg) # combo of bytes and edecode it


def client_communication(person):
    """
    Thread to handle all messages from client
    :param person: socket
    :return: None
    """
    client = person.client

    # first msg received is always the persons name
    name  = client.recv(BUFSIZE).decode("utf8")
    person.set_name(name)

    msg = bytes(f"{name} has joined the chat!\n", "utf8")
    broadcast(msg, "") # broadcast welcome message

    while True: # wait for any msgs from person
        try:
            msg = client.recv(BUFSIZE) # wait, if we receive

            if msg == bytes("{quit}", "utf8"): # if msg is quit disconnect client
                client.close()
                persons.remove(person)
                broadcast(bytes(f"{name} has left the chat...", "utf8"), "")
                print(f"[DISCONNECTED] {name} disconnected")
                break
            else: # otherwise, broadcast their msg to all clients
                broadcast(msg, name+": ")
                print(f"{name}: ", msg.decode("utf8"))

        except Exception as e:
            print("[EXCEPTION]",e)
            break

def wait_for_connection():
    """
    Wait for connection from new clients, start new thread once connected
    : param SERVER: SOCKET
    : return: None
    """


    while True: 
        try: # try to connect, else show fail msg
            client,addr = SERVER.accept()  # wait for any new connections
            person = Person(addr,client) # create new person for connection
            persons.append(person) # all clients in person list

            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication,args=(person,)).start()
        except Exception as e:
            print("[EXCEPTION]",e)
            break

    print("SERVER CRASHED")



if __name__ == "__main__":
    SERVER.listen(MAX_CONNECTIONS) # open server to listen for connections in backlog
    print("[STARTED] Waiting for connections...")
    # Starts a new thread
    ACCEPT_THREAD = Thread(target = wait_for_connection) 
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()