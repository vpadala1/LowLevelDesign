import threading
from RateLimiterFactory import RateLimiterFactory

class RateLimiterManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:  # Ensure thread safety
                if cls._instance is None:
                    cls._instance = super(RateLimiterManager, cls).__new__(cls)
                    cls._instance.rate_limiter = RateLimiterFactory.create_rate_limiter("fixed", 100, 60000)
        return cls._instance

    def allow_request(self, client_id: str) -> bool:
        return self.rate_limiter.allow_request(client_id)