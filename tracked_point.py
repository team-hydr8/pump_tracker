from user import Employee, Customer
from enums import PumpStatus

class TrackedPoint():
    def __init__(self, id):
        self.id = id
        self.status = PumpStatus.GREEN
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
        
    def remove_maintenance(self, id):
        for i in range(len(self.self.maintenance)):
            if self.maintenance[i].get_id() == id:
                self.maintenance.pop(i)
    
    def check_damage(self, data):
        if data >= 90:
            self.status = PumpStatus.GREEN
        elif data >= 50:
            self.status = PumpStatus.YELLOW
        else:
            self.status = PumpStatus.RED

    def add_maintenance(self, employee):
        # add member of the maintenance team
        if type(employee) == Employee:
            self.maintenance.append(employee)

    def notify_damage(self):
        if self.status != PumpStatus.GREEN:
            for i in range(len(self.maintenance)):
                self.maintenance[i].notify(self)

    
class Pump(TrackedPoint):
    def __init__(self, id):
        super().__init__(id)
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
        if self.status != PumpStatus.GREEN:
            for i in range(len(self.maintenance)):
                self.maintenance[i].notify(self)
        if self.status == "red":
            for i in range(len(self.customers)):
                self.customers[i].notify()

class LevelMeter(TrackedPoint):
    def __init__(self, id):
        super().__init__(id)
        self.status = 100

    def check_damage(self, data):
        self.status = data

    def notify_damage(self):
        if self.status < 85:
            for i in range(len(self.maintenance)):
                self.maintenance[i].notify(self)