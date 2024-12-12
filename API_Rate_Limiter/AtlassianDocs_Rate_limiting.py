import time
import random
import requests  # You might need to install the requests library if you haven't already.

class RequestHandler:
    def __init__(self, max_retries=4, last_retry_delay_millis=5000, 
                 max_retry_delay_millis=30000, jitter_multiplier_range=(0.7, 1.3)):
        self.max_retries = max_retries
        self.last_retry_delay_millis = last_retry_delay_millis
        self.max_retry_delay_millis = max_retry_delay_millis
        self.jitter_multiplier_range = jitter_multiplier_range

    def random_in_range(self):
        """Generate a random multiplier within the jitter range."""
        return random.uniform(self.jitter_multiplier_range[0], self.jitter_multiplier_range[1])

    def delay(self, milliseconds):
        """Delay execution for a specified number of milliseconds."""
        time.sleep(milliseconds / 1000.0)  # Convert milliseconds to seconds

    def fetch(self, url, params=None):
        """Send an HTTP request and handle retries."""
        retry_count = 0
        last_retry_delay = self.last_retry_delay_millis

        while retry_count <= self.max_retries:
            try:
                response = requests.get(url, params=params)
                if response.ok:  # Check if the response status code is OK (200-299)
                    self.handle_success(response)
                    return
                else:
                    # Process error responses
                    retry_delay_millis = -1

                    # Check for Retry-After header
                    if 'Retry-After' in response.headers:
                        retry_delay_millis = int(response.headers['Retry-After']) * 1000  # Convert seconds to milliseconds
                    elif response.status_code == 429:  # Too Many Requests
                        retry_delay_millis = min(2 * last_retry_delay, self.max_retry_delay_millis)

                    if retry_delay_millis > 0:
                        # Add jitter to the retry delay
                        retry_delay_millis *= self.random_in_range()
                        self.delay(retry_delay_millis)
                        retry_count += 1
                        last_retry_delay = retry_delay_millis  # Update last retry delay
                    else:
                        self.handle_failure(response)
                        return

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                self.handle_failure(e)
                return

    def handle_success(self, response):
        """Handle a successful response."""
        print("Success:", response.json())

    def handle_failure(self, response):
        """Handle a failed response."""
        print("Failure:", response.status_code, response.text)

# Example usage
if __name__ == "__main__":
    handler = RequestHandler()
    handler.fetch("https://api.example.com/resource")  # Replace with the actual URL
