from user import Employee, Customer

class TrackedPoint():
    def __init__(self, id):
        self.id = id
        self.status = "green"
        self.maintenance = []

    def get_status(self):
        return self.status
    
    def get_id(self):
        return self.id
    
    def get_maintenance(self, pos):
        if pos >= len(self.maintenance):
            return -1
        else:
            return self.maintenance[pos]
    
    # maybe a way to get a specific maintenance team member by ID? probably unnecessary
    
    def check_damage(self, data):
        if data >= 90:
            # figure out how to enum in python and make status an enum
            self.status = "green"
        elif data >= 50:
            self.status = "yellow"
        else:
            self.status = "red"

    def add_maintenance(self, employee):
        # add member of the maintenance team
        if type(employee) == Employee:
            self.customers.append(employee)

    def notify_damage(self):
        if self.status != "green":
            for i in range(len(self.maintenance - 1)):
                self.maintenance[i].notify(self)

    
class Pump(TrackedPoint):
    def __init__(self, id):
        super.__init__(id)
        self.customers = []

    def get_customer(self, pos):
        if pos >= len(self.customers):
            return -1
        else:
            return self.customers[pos]
        
    def add_customer(self, customer):
        # add customer
        if type(customer) == Customer:
            self.customers.append(customer)

    def notify_damage(self):
        if self.status != "green":
            for i in range(len(self.maintenance - 1)):
                self.maintenance[i].notify(self)
        if self.status == "red":
            for i in range(len(self.customers - 1)):
                self.customers[i].notify()

class LevelMeter(TrackedPoint):
    def __init__(self, id):
        super.__init__(id)

    def check_damage(self, data):
    # level meters have higher alert thresholds because they can idnicate theft or other undetected issues
        if data >= 95:
            self.status = "green"
        elif data >= 75:
            self.status = "yellow"
        else:
            self.status = "red"