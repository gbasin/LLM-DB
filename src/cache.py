import json
import os
import threading
from collections.abc import MutableMapping
from concurrent.futures import ThreadPoolExecutor

class ThreadSafeDict(MutableMapping):
    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.lock = threading.Lock()
        self.update(dict(*args, **kwargs))

    def __getitem__(self, key):
        with self.lock:
            return self.store.get(key, False)

    def __setitem__(self, key, value):
        with self.lock:
            self.store[key] = value

    def __delitem__(self, key):
        with self.lock:
            del self.store[key]

    def __iter__(self):
        with self.lock:
            return iter(self.store)

    def __len__(self):
        with self.lock:
            return len(self.store)

class Cache:
    def __init__(self, filename):
        self.filename = filename
        self.cache = ThreadSafeDict()
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=1)
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                self.cache.update(json.load(f))

    def get(self, key):
        value = self.cache.get(key)
        return value if value is not None else False

    def set(self, key, value):
        self.cache[key] = value
        self.executor.submit(self._write_to_file)

    def _write_to_file(self):
        with self.lock:
            with open(self.filename, 'w') as f:
                json.dump(dict(self.cache), f)