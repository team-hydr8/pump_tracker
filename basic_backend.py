from user import Employee, Customer
from tracked_point import Pump, LevelMeter

class Backend():
    def __init__(self):
        self.employees = []
        self.customers = []
        self.pumps = []
        self.meters = []

    def new_employee(self, name, id, password):
        new_emp = Employee(name, id, password)

        for i in range(len(self.pumps) - 1):
            self.pumps[i].add_maintenace(new_emp)

        for i in range(len(self.meters) - 1):
            self.meters[i].add_maintenace(new_emp)

        self.employees.append(new_emp)

    def new_pump(self, id):
        new_p = Pump(id)
        self.pumps.append(new_p)

        for i in range(len(self.employees) - 1):
            new_p.add_maintenance(self.employees[i])

    def new_meter(self, id):
        new_m = LevelMeter(id)
        self.meters.append(new_m)

        for i in range(len(self.employees) - 1):
            new_m.add_maintenance(self.employees[i])

    def new_customer(self, name, id, password, pump_id):
        pump_found = False
        for i in range(len(self.pumps) - 1):
            if self.pumps[i].get_id == pump_id:
                pump_position = i
                pump_found = True
                break

        if not pump_found:
            self.new_pump(pump_id)
            pump_position = len(self.pumps) - 1

        new_customer = Customer(name, id, password, self.pumps[pump_position], 0)
        self.pumps[pump_position].add_customer(new_customer)
        self.customers.append(new_customer)
