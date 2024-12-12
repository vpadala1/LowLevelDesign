import time
from collections import defaultdict
from RateLimiter import RateLimiter

class FixedWindowRateLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_size_in_millis: int):
        self.max_requests = max_requests
        self.window_size_in_millis = window_size_in_millis / 1000.0  # Convert to seconds
        self.request_counts = defaultdict(int)
        self.window_start_times = {}

    def allow_request(self, client_id: str) -> bool:
        current_time = time.time()  # Current time in seconds
        print(current_time)
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

# Example usage:
if __name__ == "__main__":
    rate_limiter = FixedWindowRateLimiter(max_requests=5, window_size_in_millis=10000)  # 10 seconds window
    client_id = "client_123"

    for _ in range(7):  # Simulate 7 requests
        allowed = rate_limiter.allow_request(client_id)
        print(f"Request allowed: {allowed}")
        time.sleep(1)  # Sleep for 1 second between requests
