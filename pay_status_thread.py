import logging
import threading
import time

import logging
import threading
import time
from db.db import fetch_all_invoice, update_db

def pay_status():
    logging.info("Thread %s: starting")
    while True:
        #print(f"[{threading.current_thread().name}] Printing this message every 2 seconds")
        update_db()
        time.sleep(2)
    logging.info("Thread %s: finishing")

# initiate the thread with daemon set to True
daemon_thread = threading.Thread(target=pay_status, name="daemon-thread", daemon=True)
# or
# daemon_thread.daemon = True
# or
# daemon_thread.setDaemon(True)
#daemon_thread.start()
