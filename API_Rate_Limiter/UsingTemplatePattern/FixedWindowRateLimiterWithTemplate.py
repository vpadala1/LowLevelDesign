import time
from collections import defaultdict

from AbstractRateLimiter import AbstractRateLimiter

class FixedWindowRateLimiterWithTemplate(AbstractRateLimiter):
    def __init__(self, max_requests: int, window_size_in_millis: int):
        super().__init__(max_requests, window_size_in_millis)
        self.request_counts = defaultdict(int)
        self.window_start_times = {}

    def is_request_allowed(self, client_id: str) -> bool:
        current_time = time.time() * 1000  # Convert to milliseconds

        # Initialize the window start time if not present
        if client_id not in self.window_start_times:
            self.window_start_times[client_id] = current_time

        window_start_time = self.window_start_times[client_id]

        # Reset the count if the current time exceeds the window size
        if current_time - window_start_time >= self.window_size_in_millis:
            self.window_start_times[client_id] = current_time
            self.request_counts[client_id] = 0

        request_count = self.request_counts[client_id]

        # Check if the request is allowed
        if request_count < self.max_requests:
            self.request_counts[client_id] += 1
            return True
        
        return False
