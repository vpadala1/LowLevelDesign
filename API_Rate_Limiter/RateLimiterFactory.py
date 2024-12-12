from FixedWindowRateLimiter import FixedWindowRateLimiter
from SlidingWindowRateLimiter import SlidingWindowRateLimiter

class RateLimiterFactory:
    @staticmethod
    def create_rate_limiter(rate_limiter_type: str, max_requests: int, window_size_in_millis: int):
        if rate_limiter_type.lower() == "fixed":
            return FixedWindowRateLimiter(max_requests, window_size_in_millis)
        elif rate_limiter_type.lower() == "sliding":
            return SlidingWindowRateLimiter(max_requests, window_size_in_millis)
        else:
            raise ValueError("Unknown rate limiter type")

