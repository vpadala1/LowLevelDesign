import time
from collections import defaultdict, deque
from RateLimiter import RateLimiter


class SlidingWindowRateLimiter(RateLimiter): # This is Sliding Window Counter.. 
    def __init__(self, max_requests: int, window_size_in_millis: int):
        self.max_requests = max_requests
        self.window_size_in_millis = window_size_in_millis / 1000.0  # Convert to seconds
        self.request_timestamps = defaultdict(deque)

    def allow_request(self, client_id: str) -> bool:
        current_time = time.time()  # Current time in seconds
        timestamps = self.request_timestamps[client_id]

        # Remove timestamps outside the window
        while timestamps and current_time - timestamps[0] > self.window_size_in_millis:
            timestamps.popleft()  # Remove the oldest timestamp

        # Check if a new request can be allowed
        if len(timestamps) < self.max_requests:
            timestamps.append(current_time)  # Add the current timestamp
            return True
        
        return False

# Example usage
if __name__ == "__main__":
    rate_limiter = SlidingWindowRateLimiter(max_requests=5, window_size_in_millis=10000)  # 10 seconds window
    client_id = "client_123"

    for _ in range(7):  # Simulate 7 requests
        allowed = rate_limiter.allow_request(client_id)
        print(f"Request allowed: {allowed}")
        time.sleep(1)  # Sleep for 1 second between requests
