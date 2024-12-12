from RateLimiterFactory import RateLimiterFactory   

def main():
    fixed_window_rate_limiter = RateLimiterFactory.create_rate_limiter("fixed", 10, 60000)
    sliding_window_rate_limiter = RateLimiterFactory.create_rate_limiter("sliding", 10, 60000)

    # Testing Fixed Window Rate Limiter
    print("Fixed Window Rate Limiter:")
    for i in range(12):
        print(fixed_window_rate_limiter.allow_request("client1"))

    # Testing Sliding Window Rate Limiter
    print("Sliding Window Rate Limiter:")
    for i in range(12):
        print(sliding_window_rate_limiter.allow_request("client2"))

if __name__ == "__main__":
    main()
