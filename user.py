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

# Customer
# is: a user
# has: associated pump, balance?
# is able to: adjust balance?

# Employee
# is: a user
# has: 
# is able to: get detailed notification, view employee view (may not be in this class)