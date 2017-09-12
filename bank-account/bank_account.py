class BankAccount:
    def __init__(self, id):
        self.balance = 0
        self.id = id

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount

    @property
    def state(self):
        if self.balance >= 0:
            return 'normal'
        else:
            return 'overdraft'

    def pay_interest(self):
        self.balance += self.balance * 0.1