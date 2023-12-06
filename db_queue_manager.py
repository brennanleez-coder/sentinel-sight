import queue # For thread-safe communication between threads
import threading
from db import get_db_connection

db_operation_queue = queue.Queue()

# DBQueueManager ensures a single thread is used to access the database
# This is necessary because SQLite does not support multithreaded access
# See https://docs.python.org/3/library/sqlite3.html#multithreading
class DBQueueManager:
    def __init__(self):
        self.db_operation_queue = queue.Queue()
        self.db_thread = threading.Thread(target=self.db_worker, daemon=True)
        self.db_thread.start()

    def db_worker(self):
        global conn
        while True:
            task = self.db_operation_queue.get()
            if task is None:  # None is a signal to stop the worker
                break
            function, args = task
            try:
                conn = get_db_connection()
                function(conn, *args)
                conn.close()
            except Exception as e:
                print(f"Database operation error: {e}")
            finally:
                self.db_operation_queue.task_done()

    def enqueue_db_task(self, function, *args):
        self.db_operation_queue.put((function, args))

    def stop_db_worker(self):
        self.db_operation_queue.put(None)
        self.db_thread.join()