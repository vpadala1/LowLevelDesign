from abc import ABC, abstractmethod

from RateLimiter import RateLimiter

class AbstractRateLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_size_in_millis: int):
        self.max_requests = max_requests
        self.window_size_in_millis = window_size_in_millis

    def allow_request(self, client_id: str) -> bool:
        return self.is_request_allowed(client_id)

    @abstractmethod
    def is_request_allowed(self, client_id: str) -> bool:
        pass
