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
        self.current_id = "none"

    def new_employee(self, name, id, password):
        new_emp = Employee(name, id, password)

        for i in range(len(self.pumps)):
            self.pumps[i].add_maintenance(new_emp)

        for i in range(len(self.meters)):
            self.meters[i].add_maintenace(new_emp)

        self.employees.append(new_emp)

    def new_pump(self, id):
        new_p = Pump(id)
        self.pumps.append(new_p)

        for i in range(len(self.employees)):
            new_p.add_maintenance(self.employees[i])

    def new_meter(self, id):
        new_m = LevelMeter(id)
        self.meters.append(new_m)

        for i in range(len(self.employees)):
            new_m.add_maintenance(self.employees[i])

    def new_customer(self, name, id, password, pump_id):
        pump_found = False
        for i in range(len(self.pumps)):
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
        for i in range(len(self.customers)):
            if self.customers[i].get_id() == user_id:
                user_pos = i
                is_customer = True

        if not is_customer:
            for i in range(len(self.employees)):
                if self.employees[i].get_id() == user_id:
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
            self.current_id = user_id
            if is_customer:
                self.current_view = self.customers[user_pos].get_view()
            else:
                self.current_view = self.employees[user_pos].get_view()
        else:
            print("Incorrect user ID or password")

    def get_employee(self, key):
        if type(key) == int:
            if key < len(self.employees):
                return self.employees[key]
        elif type(key) == str:
            for i in range(len(self.employees)):
                if self.employees[i].get_id() == key:
                    return self.employees[i]
        
    def get_pump(self, key):
        if type(key) == int:
            if key < len(self.pumps):
                return self.pumps[key]
        elif type(key) == str:
            for i in range(len(self.pumps)):
                if self.pumps[i].get_id() == key:
                    return self.pumps[i]
        
    def get_customer(self, key):
        if type(key) == int:
            if key < len(self.customers):
                return self.customers[key]
        elif type(key) == str:
            for i in range(len(self.customers)):
                if self.customers[i].get_id() == key:
                    return self.customers[i]
        
    def get_level_meter(self, key):
        if type(key) == int:
            if key < len(self.meters):
                return self.meters[key]
        elif type(key) == str:
            for i in range(len(self.self.meters)):
                if self.meters[i].get_id() == key:
                    return self.meters[i]
                
    def update_customer_balance(self, customer_id, amount):
        self.get_customer(customer_id).adjust_balance(amount)

def run_test():
    backend = Backend()

    backend.new_pump("12345")
    print(backend.get_pump(0).get_id())

    backend.new_employee("John Smith", "ABCDE", "supersecurepassword")
    print(backend.get_employee(0).get_name())
    print(backend.get_pump(0).get_maintenance(0).get_name())

    backend.new_customer("Smohn Jith", "FGHIJ", "correcthorsebatterystaple", "12345")
    print(backend.get_customer(0).get_pump().get_id())
    print(backend.get_customer("FGHIJ").get_name())

    backend.login("XYZZY", "invalidpassword")
    backend.login("ABCDE", "invalidpassword")
    backend.login("ABCDE", "supersecurepassword")

    print(backend.current_view.language)
    print(backend.current_view.view_type)

if __name__ == "__main__":
    run_test()