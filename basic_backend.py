class Pump():
    def __init__(self, status, id):
        self.status = status
        self.id = id
        self.customers = []
        self.maintenance = []

    def get_status(self):
        return self.status
    
    def get_id(self):
        return self.id
    
    def get_customer(self, pos):
        if pos >= len(self.customers):
            return -1
        else:
            return self.customers[pos]
        
    def get_maintenance(self, pos):
        if pos >= len(self.maintenance):
            return -1
        else:
            return self.maintenance[pos]
    
    def check_damage(self, data):
        if data >= 90:
            # figure out how to enum in python and make status an enum
            self.status = "green"
        elif data >= 50:
            self.status = "yellow"
        else:
            self.status = "red"

    def add_customer(self, customer):
        # add customer
        if type(customer) == Customer:
            self.customers.append(customer)

    def add_maintenance(self, employee):
        # add member of the maintenance team
        if type(employee) == Employee:
            self.customers.append(employee)

    def notify_damage(self):
        if self.status != "green":
            for i in range(len(self.maintenance - 1)):
                self.maintenance[i].notify(self)
        if self.status == "red":
            for i in range(len(self.customers - 1)):
                self.customers[i].notify()

#create a water mete class (subclass of pump? both subclasses of some "measurement" class??)

#temporary person classes – remake into subclasses of person/user/whatever later
class Customer():
    # maybe add balance stuff later - is a Can Have
    def __init__(self, name, id, pump):
        self.name = name
        self.id = id
        self.pumpID = pump.get_id()
        pump.addCustomer(self)

    def notify():
        print("I have been notified")

class Employee():
    def __init__(self, name):
        self.name = name

    def notify(pump):
        print("I have been notified about " + pump.get_id())