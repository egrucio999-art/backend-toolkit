"""Queue-based task scheduler with delayed execution."""
import time
import threading
import queue


class TaskScheduler:
    def __init__(self):
        self.tasks = queue.Queue()
        self.running = False

    def add_task(self, task_function, *args, **kwargs):
        self.tasks.put((task_function, args, kwargs))

    def start(self):
        self.running = True
        threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        while self.running:
            try:
                task_function, args, kwargs = self.tasks.get(timeout=1)
                try:
                    task_function(*args, **kwargs)
                except Exception:
                    pass
                self.tasks.task_done()
            except queue.Empty:
                continue

    def stop(self):
        self.running = False

    def schedule_delayed(self, delay, task_function, *args, **kwargs):
        def delayed_task():
            time.sleep(delay)
            task_function(*args, **kwargs)
        threading.Thread(target=delayed_task, daemon=True).start()
