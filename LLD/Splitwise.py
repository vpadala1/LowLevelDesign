class User:
    user_id_counter = 1

    def __init__(self, name, email, phone, bio=None, imageURI=None):
        self.user_id = User.user_id_counter
        User.user_id_counter += 1
        self.name = name
        self.email = email
        self.phone = phone
        self.bio = bio
        self.imageURI = imageURI

class Group:
    def __init__(self, gid, users, title, description, imageURI=None):
        self.gid = gid
        self.users = users  # List of User objects
        self.title = title
        self.description = description
        self.imageURI = imageURI
        self.expenses = []  # List of Expense objects

    def delete_group(self):
        # Notify users about group deletion
        NotificationService.notify_users(self.users, f"The group '{self.title}' has been deleted.")
        # Perform the deletion logic here
        self.users = []
        self.expenses = []
        self.gid = None
        self.title = None
        self.description = None
        self.imageURI = None

    def edit_group(self, new_title=None, new_description=None, new_imageURI=None):
        if new_title:
            self.title = new_title
        if new_description:
            self.description = new_description
        if new_imageURI:
            self.imageURI = new_imageURI

        # Notify users about group edit
        NotificationService.notify_users(self.users, f"The group '{self.title}' has been updated.")

class Balance:
    def __init__(self, currency, amount):
        self.currency = currency
        self.amount = amount  # Positive if owed, negative if paid

class Expense:
    def __init__(self, expenseId, amount, currency, gid=None, title=None):
        self.expenseId = expenseId
        self.amount = amount
        self.currency = currency
        self.gid = gid
        self.title = title
        self.balances = {}  # Mapping from User to Balance
        self.isSettled = False

    def add_exact_split(self, split_details):
        """
        split_details: Dictionary {user: exact_amount}
        """
        total_split = sum(split_details.values())
        if total_split != self.amount:
            raise ValueError("Total split amounts do not match the expense amount.")

        for user, exact_amount in split_details.items():
            self.balances[user] = Balance(currency=self.currency, amount=exact_amount)

        # Notify users about the added expense
        NotificationService.notify_users(list(split_details.keys()), f"An exact split expense '{self.title}' has been added.")

    def add_equal_split(self, users):
        split_amount = self.amount / len(users)
        for user in users:
            self.balances[user] = Balance(currency=self.currency, amount=split_amount)

        # Notify users about the added expense
        NotificationService.notify_users(users, f"An equal split expense '{self.title}' has been added.")

    def add_unequal_split(self, split_details):
        """
        split_details: Dictionary {user: percentage}
        """
        total_percentage = sum(split_details.values())
        if total_percentage != 100:
            raise ValueError("Total percentages do not sum up to 100%.")

        for user, percentage in split_details.items():
            split_amount = (percentage / 100) * self.amount
            self.balances[user] = Balance(currency=self.currency, amount=split_amount)

        # Notify users about the added expense
        NotificationService.notify_users(list(split_details.keys()), f"An unequal split expense '{self.title}' has been added.")

    def edit_expense(self, new_amount=None, new_currency=None, new_title=None):
        if new_amount:
            self.amount = new_amount
        if new_currency:
            self.currency = new_currency
        if new_title:
            self.title = new_title

        # Notify users about the edited expense
        NotificationService.notify_users(self.balances.keys(), f"The expense '{self.title}' has been edited.")

    def delete_expense(self):
        # Notify users about the expense deletion
        NotificationService.notify_users(self.balances.keys(), f"The expense '{self.title}' has been deleted.")
        self.balances = {}
        self.expenseId = None
        self.amount = None
        self.currency = None
        self.gid = None
        self.title = None

class NotificationService:
    @staticmethod
    def notify_users(users, message):
        for user in users:
            print(f"Notification to {user.name}: {message}")

def main():
    # Create users
    user1 = User(name="Alice", email="alice@example.com", phone="1234567890")
    user2 = User(name="Bob", email="bob@example.com", phone="0987654321")
    user3 = User(name="Charlie", email="charlie@example.com", phone="1122334455")

    # Create group
    group = Group(gid=1, users=[user1, user2, user3], title="Trip", description="Trip to Hawaii")

    # Add expenses
    expense1 = Expense(expenseId=1, amount=300, currency="USD", gid=group.gid, title="Hotel")
    expense1.add_equal_split([user1, user2, user3])
    group.expenses.append(expense1)

    expense2 = Expense(expenseId=2, amount=200, currency="USD", gid=group.gid, title="Dinner")
    expense2.add_exact_split({user1: 100, user2: 50, user3: 50})
    group.expenses.append(expense2)

    expense3 = Expense(expenseId=3, amount=150, currency="USD", gid=group.gid, title="Car Rental")
    expense3.add_unequal_split({user1: 50, user2: 30, user3: 20})
    group.expenses.append(expense3)

    # Edit expense
    expense1.edit_expense(new_amount=350)

    # Delete expense
    expense2.delete_expense()

    # Edit group
    group.edit_group(new_title="Hawaii Trip")

    # Delete group
    group.delete_group()

if __name__ == "__main__":
    main()

