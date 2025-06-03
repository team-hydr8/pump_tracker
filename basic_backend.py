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

        for i in range(len(self.pumps - 1)):
            self.pumps[i].add_maintenace(new_emp)

        for i in range(len(self.meters - 1)):
            self.meters[i].add_maintenace(new_emp)