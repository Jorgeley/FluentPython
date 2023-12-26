"""
Threads or Concurrent Scripts can be used to submit callables to be executed
concurrently. The ThreadPoolExecutor will manage an internal pool of workers
and the queue of tasks for execution.
For our example, this is a script for downloading stuff, nothing special
"""

import os
import sys
import time
from concurrent import futures

import requests

COUNTRY_CODES = (
    "CN IN US ID BR PK NG BD RU JP " "MX PH VN ET EG DE IR TR CD FR"
).split()
BASE_URL = "http://flupy.org/data/flags"  # flags images URL
DEST_DIR = "/Users/jorgeleyjunior/Downloads/Flags/"  # make sure exists


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, "wb") as fp:
        fp.write(img)
        # fp.write(img * 500000)  # making the file 500000 times bigger to
        # simulate heavy download


def get_flag(cc):
    url = "{}/{cc}/{cc}.gif".format(BASE_URL, cc=cc.lower())
    resp = requests.get(url)
    return resp.content


def show(text):
    print(text, end=" ")
    # this is needed because Python normally waits for a line break to flush
    # the stdout buffer.
    sys.stdout.flush()


# running a normal sequential download, no thread, check the DEST_DIR folder.
def simple_sequential_download_many(cc_list):
    for cc in sorted(cc_list):
        image = get_flag(cc)
        show(cc)
        save_flag(image, cc.lower() + ".gif")
    return len(cc_list)


MAX_WORKERS = 12


def download_one(cc):
    image = get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + ".gif")
    return cc


# This IS NOT truly parallel computation
def thread_download_many_v1(cc_list):
    """
    Even though we're sorting the list, you'll see the output
    isn't sorted since they're running concurrently
    :param cc_list:
    :return:
    """
    workers = min(MAX_WORKERS, len(cc_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))


# This IS NOT truly parallel computation
def thread_download_many_v2(cc_list):
    """
    In this 2nd version, we're scheduling the threads and retrieving the
    results. We're hard coding the number of workers to 10, this way we can
    see the pending tasks since we have actually 20 to run. The main
    difference between executor.map and executor.submit is that the fist one
    returns the callable results as an iterator and the last one only returns
    a Future instance which represents the task execution.
    In few words: executor.map returns the results, executor.submit returns
    the task instance.
    :param cc_list:
    :return:
    """
    with futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        to_do = []
        for cc in sorted(cc_list):
            # schedules the callable to be executed, and returns a future
            # representing this pending operation
            future = executor.submit(download_one, cc)
            to_do.append(future)
            msg = "Scheduled for {}: {}"
            print(msg.format(cc, future))
        results = []
        # 'as_completed()' yields futures as they are completed,
        # it won't block the threads
        for future in futures.as_completed(to_do):
            res = future.result()
            msg = "{} result: {!r}"
            print(msg.format(future, res))
            results.append(res)
    return len(results)


# This IS INDEED truly parallel computation
def thread_download_many_v3(cc_list):
    """
    In this 3rd version we're running the tasks using real parallel
    computation.
    :param cc_list:
    :return:
    """
    # 'ProcessPoolExecutor' will launch as many workers as machine CPU cores
    with futures.ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))


def main(download_many):
    t0 = time.time()
    count = download_many(COUNTRY_CODES)
    elapsed = time.time() - t0
    msg = "\n{} flags downloaded in {:.2f}s"
    print(msg.format(count, elapsed))


"""
Here's the fun! Let's run a normal sequential call and a threaded one and see
the difference!
IMPORTANT:  you'll have to delete the downloaded flags, comment out the other
'main()' calls to see the difference between the the
'simple_sequential_download_many' and 'thread_download_many' versions and
vice versa.
"""
if __name__ == "__main__":
    # main(simple_sequential_download_many)  # if you're running this, don't
    # run the next 'main()' calls
    # main(thread_download_many_v1)  # if you're running this, don't run the
    # previous and next 'main()' calls
    # main(thread_download_many_v2)  # if you're running this, don't run the
    # previous and next 'main()' calls
    main(
        thread_download_many_v3
    )  # if you're running this, don't run the previous 'main()' calls

"""
***** BENCHMARK (MacBook Pro, 6-Core Intel Core i7 2.6 GHz, 16 GB RAM) *******
- simple_sequential_download_many: 11.04s
- thread_download_many_v1: 0.91s
- thread_download_many_v2 (10 workers): 1.55s
- thread_download_many_v2 (20 workers): 1.03s
- thread_download_many_v3: 1.73s

Conclusion: not much gain using parallel computation since 6 cores spawn only
6 workers against 20 in the other threads, although if we equalize the workers
to 6, parallel computation will be the fastest.
In summary, using parallel computation is more balanced.
"""
