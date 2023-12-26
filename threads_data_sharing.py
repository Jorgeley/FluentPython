# SuperFastPython.com
# example benchmark data transfer between threads
from multiprocessing import set_start_method, Manager
from time import time
from multiprocessing.pool import ThreadPool, Pool
from queue import Queue


# task to generate data and send to the consumer
def producer_task(queue):
    # generate data
    data = [i for i in range(1000000)]
    # send the data
    queue.put(data)


# task to consume data sent from producer
def consumer_task(queue):
    # retrieve the data
    data = queue.get()  # noqa: F841


# run a test and time how long it takes
def test(pool, queue, n_repeats):
    # repeat many times
    for i in range(n_repeats):
        # issue the consumer task
        consumer = pool.apply_async(consumer_task, args=(queue,))
        # issue the producer task
        producer = pool.apply_async(producer_task, args=(queue,))  # noqa: F841
        # wait for the consumer to get the data
        consumer.wait()


# entry point
if __name__ == '__main__':
    # record the start time
    time_start = time()
    n_repeats = 1000

    """
    This is a process data sharing mechanism, it will be slowest compared
    to the Thread approach. This happens because transmitting data between
    processes involves SERIALIZATION, TRANSMISSION, and DESERIALIZATION
    of the Python objects.
    Uncomment the 2 'with' blocks below and comment the ThreadPool one if you
    want to see the difference
    """
    # set_start_method('spawn')
    # with Pool(2) as pool:
    #     with Manager() as manager:
    #         queue = manager.Queue()
    #         test(pool, queue, n_repeats)

    """
    This is a Thread data sharing mechanism, it will be fastest compared
    to the previous Process approach. This happens because THREADS SHARE
    MEMORY DIRECTLY, no serialization and deserialization is involved.
    Comment the 'with' block below and uncomment the previous 2 ones if you
    want to see the difference.
    """
    with ThreadPool(2) as pool:
        queue = Queue()
        test(pool, queue, n_repeats)
    # record the end time
    time_end = time()
    # report the total time
    duration = time_end - time_start
    print(f'Total Time {duration:.3} seconds')
    # report estimated time per task
    per_task = duration / n_repeats
    print(f'About {per_task:.3} seconds per task')

"""
***** BENCHMARK (MacBook Pro, 6-Core Intel Core i7 2.6 GHz, 16 GB RAM) *******
- Process Data Sharing:
    - Total = 223s
    - Per Task = 0.223s
- Thread Data Sharing:
    - Total = 64.1s
    - Per Task = 0.0641s
"""