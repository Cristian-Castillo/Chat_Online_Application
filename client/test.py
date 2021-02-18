from client import Client
import time
from threading import Thread

def update_messages():
    """
    updates the local list of messages 
    :return: None
    """
    msgs = []
    run = True
    while run:
        time.sleep(0.1) # update every 1/10 of a sec
        new_messages = c1.get_messages() # get any new msgs from client
        msgs.extend(new_messages) # add to local list of messages

        for msg in new_messages: # display new messages
            print(msg)

            if msg == "{quit}":
                run = False
                break

Thread(target = update_messages).start()

c1 = Client('Cris')
c2 = Client('Tom')

c1.send_message('Hello')
c2.send_message('Whats up')
time.sleep(5)
c1.send_message('Nothing much, how about you?')
time.sleep(5)
c2.send_message('Same here...')
time.sleep(5)

c1.disconnect()
time.sleep(2)
c2.disconnect()