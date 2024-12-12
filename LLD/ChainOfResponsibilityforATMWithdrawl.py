from abc import ABC, abstractmethod

class CashHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    def set_next_handler(self, next_handler):
        self.next_handler = next_handler

    @abstractmethod
    def withdraw(self, amount):
        pass

class TwoThousandHandler(CashHandler):
    def withdraw(self, amount):
        if amount >= 2000:
            num_notes = amount // 2000
            remainder = amount % 2000
            print(f"Dispensing {num_notes} ₹2000 notes")
            if remainder != 0 and self.next_handler:
                self.next_handler.withdraw(remainder)
        else:
            if self.next_handler:
                self.next_handler.withdraw(amount)

class FiveHundredHandler(CashHandler):
    def withdraw(self, amount):
        if amount >= 500:
            num_notes = amount // 500
            remainder = amount % 500
            print(f"Dispensing {num_notes} ₹500 notes")
            if remainder != 0 and self.next_handler:
                self.next_handler.withdraw(remainder)
        else:
            if self.next_handler:
                self.next_handler.withdraw(amount)

class OneHundredHandler(CashHandler):
    def withdraw(self, amount):
        if amount >= 100:
            num_notes = amount // 100
            remainder = amount % 100
            print(f"Dispensing {num_notes} ₹100 notes")
            if remainder != 0 and self.next_handler:
                self.next_handler.withdraw(remainder)
        else:
            if self.next_handler:
                self.next_handler.withdraw(amount)

def main():
    # Set up the chain
    one_hundred_handler = OneHundredHandler(None)
    five_hundred_handler = FiveHundredHandler(one_hundred_handler)
    two_thousand_handler = TwoThousandHandler(five_hundred_handler)

    # Customer withdraws 3500
    amount_to_withdraw = 3700
    print(f"Customer wants to withdraw ₹{amount_to_withdraw}")
    two_thousand_handler.withdraw(amount_to_withdraw)

if __name__ == "__main__":
    main()
