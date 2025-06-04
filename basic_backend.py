from user import Employee, Customer
from tracked_point import Pump, LevelMeter
from view import AppView
from enums import ViewType

class Backend():
    def __init__(self):
        self.employees = []
        self.customers = []
        self.pumps = []
        self.meters = []
        self.current_view = AppView(ViewType.CUSTOMER)

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

    def login(self, user_id, password):
        is_customer = False
        user_pos = -1
        for i in range(len(self.customers) - 1):
            if self.customers[i].get_id == user_id:
                user_pos = i
                is_customer = True

        if not is_customer:
            for i in range(len(self.employees) - 1):
                if self.employees[i].get_id == user_id:
                    user_pos = i

        if user_pos != -1:
            if is_customer:
                success = self.customers[user_pos].login(password)
            else:
                success = self.employees[user_pos].login(password)
        else:
            success = False

        if success:
            print("Successfully logged in!")
            if is_customer:
                self.current_view = self.customers[user_pos].get_view()
            else:
                self.current_view = self.employees[user_pos].get_view()
        else:
            print("Incorrect user ID or password")

