# User and its subclasses (Customer, Employee)

class User:
    def __init__(self, name, id, password):
        self.name = name
        self.id = id
        self.password = password
    
    # bad login make more secure later
    def login(self, pass_attempt):
        if (pass_attempt == self.password):
            return True
        else:
            return False
        
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id
    
    def notify(self):
        # this method should be hooked up to the UI - see what UI people need
        print("I have been notified")

# THIS IS NOT HOOKED UP TO THE PUMP CLASS YET – DO THIS!!
class Customer(User):
    def __init__(self, name, id, password, pump, balance):
        super().__init__(name, id, password)
        self.pump = pump
        self.balance = balance

    def get_pump(self):
        return self.pump
    
    def get_balance(self):
        return self.balance

    def adjustBalance(self, amount):
        self.balance += amount

class Employee(User):
    # technically this init is unneeded but useful to have in case employees need more attributes later o7
    def __init__(self, name, id, password):
        super().__init__(name, id, password)

    def notify(self, pump):
        # hook up to the UI also
        print("I have been notified about " + pump.get_id())