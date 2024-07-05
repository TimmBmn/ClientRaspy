from main import main
import threading
import random
import time

NUMBER_OF_CLIENTS = 11

thread: threading.Thread | None = None
for i in range(NUMBER_OF_CLIENTS):
    room = random.randint(1, 300)
    thread = threading.Thread(target=main, daemon=True, args=(room, False))
    thread.start()
    print("Started Room: " + str(room))
    time.sleep(2)

if thread is not None:
    thread.join()
