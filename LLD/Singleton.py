import threading

class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __init__(self,slots):
        if self._instance is not None:
            raise Exception("It is first to be Constructed!!!")
        self.slots = slots

    @staticmethod
    def get_instance(cls,slots):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(slots)
        return cls._instance