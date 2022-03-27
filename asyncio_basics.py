import asyncio

# 'async' makes this function a coroutine
async def fake_long_task(limit: int = 1000):
    r = 0
    for i in range(limit):
        if i != 0 and i % 1000000 == 0:
            print(f"sleeping task {asyncio.tasks.current_task().get_name()} at {i}")
            # this makes the longer task to give the others a chance to run, like in parallel
            await asyncio.sleep(0.0001)
        r += i * i ^ i  # pretending doing something
    return r

async def main():
    # adding coroutines to the loop
    t1 = loop.create_task(fake_long_task(33333333))
    t2 = loop.create_task(fake_long_task())
    t3 = loop.create_task(fake_long_task(9999999))
    # if we need the results, we have to wait for them, otherwise all goes to background
    await asyncio.wait([t1, t2, t3])
    return ("task 1", t1), ("task 2", t2), ("task 3", t3)

# loop is the 'manager' for introducing coroutines
loop = asyncio.get_event_loop()
loop.set_debug(1)
t1, t2, t3 = loop.run_until_complete(main())
loop.close()
print(t1)
print(t2)
print(t3)

# another straight forward way is using thread:
import threading

def another_fake_long_task():
    import time
    time.sleep(10)
    print("finished another_fake_long_task()")

threading.Thread(target=another_fake_long_task).start()
print("thread started")