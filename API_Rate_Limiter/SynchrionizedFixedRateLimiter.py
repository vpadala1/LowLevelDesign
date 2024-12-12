import time
from collections import defaultdict
from RateLimiter import RateLimiter
from threading import Lock, Thread

class SynchronizedFixedWindowRateLimiter(RateLimiter):
    def __init__(self, max_requests: int, window_size_in_millis: int):
        self.max_requests = max_requests
        self.window_size_in_millis = window_size_in_millis / 1000.0  # Convert to seconds
        self.request_counts = defaultdict(int)
        self.window_start_times = {}
        self.locks = defaultdict(Lock)  # Dictionary of locks for each client

    def allow_request(self, client_id: str) -> bool:
        with self.locks[client_id]:  # Lock for the specific client
            current_time = time.time()  # Current time in seconds
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
                print(f"[{client_id}] Request allowed: {request_count + 1}")
                return True
            
            print(f"[{client_id}] Request denied: {request_count + 1} (limit reached)")
            return False

def simulate_requests(rate_limiter, client_id):
    for _ in range(7):  # Simulate 7 requests
        allowed = rate_limiter.allow_request(client_id)
        print(f"Request allowed for {client_id}: {allowed}")
        time.sleep(1)  # Sleep for 1 second between requests
    

if __name__ == "__main__":
    rate_limiter = SynchronizedFixedWindowRateLimiter(max_requests=5, window_size_in_millis=10000)  # 10 seconds window
    client_ids = ["client_1", "client_2"]

    # Create and start threads for each client
    threads = []
    for client_id in client_ids:
        thread = Thread(target=simulate_requests, args=(rate_limiter, client_id))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
