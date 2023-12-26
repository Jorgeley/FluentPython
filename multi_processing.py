# SuperFastPython.com
# example of running a function in another process
from time import sleep
from multiprocessing import Process, Pipe
from random import random


def task():
    sleep(60)


"""
The multiprocessing class allows you to spawn separate python processes,
you'll see that 2 separated python processes are executed, use the 'top'
command in your terminal, you can filter by 'python' keyword and clearly
see something like:

    |_ Python multiprocessing.py
       |_ Python -c from multiprocessing.resource_tracker ...
       |_ Python -c from multiprocessing.spawn ...
"""
if __name__ == '__main__':
    # create a process
    process = Process(target=task)
    # run the process
    process.start()

### uncomment this and comment the previous lines to see the difference  # noqa: E266 E501
### sleep(10) # noqa: E266


"""
This is an example of how to share data between processes using pipes.
The difference between pipe and queue is that pipe is meant to be used
only for sharing data between 2 processes while queue can use more
"""


def sender(connection):
    print('Sender: Running', flush=True)
    for i in range(10):
        value = random()
        # send data
        print(f"sending {value}")
        connection.send(value)
    connection.send(None)
    print('Sender: Done', flush=True)


# consume work
def receiver(connection):
    print('Receiver: Running', flush=True)
    while True:
        item = connection.recv()
        print(f'>receiver got {item}', flush=True)
        if item is None:
            break
    print('Receiver: Done', flush=True)


# entry point
if __name__ == '__main__':
    # create the pipe
    conn1, conn2 = Pipe()
    # start the sender
    sender_process = Process(target=sender, args=(conn2,))
    sender_process.start()
    # start the receiver
    receiver_process = Process(target=receiver, args=(conn1,))
    receiver_process.start()
    # wait for all processes to finish
    sender_process.join()
    receiver_process.join()
