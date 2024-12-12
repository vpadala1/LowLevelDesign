from collections import deque
from time import time
from AbstractRateLimiter import AbstractRateLimiter

class SlidingWindowRateLimiterWithTemplate(AbstractRateLimiter):
    def __init__(self, max_requests: int, window_size_in_millis: int):
        super().__init__(max_requests, window_size_in_millis)
        self.request_timestamps = {}

    def is_request_allowed(self, client_id: str) -> bool:
        current_time = time() * 1000  # Current time in milliseconds
        if client_id not in self.request_timestamps:
            self.request_timestamps[client_id] = deque()

        timestamps = self.request_timestamps[client_id]

        # Remove timestamps that are outside the sliding window
        while timestamps and (current_time - timestamps[0]) > self.window_size_in_millis:
            timestamps.popleft()

        # Check if the request can be allowed
        if len(timestamps) < self.max_requests:
            timestamps.append(current_time)  # Add the current timestamp
            return True
        
        return False
