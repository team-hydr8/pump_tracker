from enum import Enum

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

    def login(self, user_id, password) -> bool:
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

        return success

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

class User():
    def __init__(self, name, id, password):
        self.name = name
        self.id = id
        self.password = password
        self.alerts = []
    
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
    
    def get_alerts(self):
        return self.alerts
    
    def notify(self):
        # this method should be hooked up to the UI - see what UI people need
        self.alerts.append("ALERT: There are disruptions in the water network that may impact you.")
        print("I have been notified")

class Customer(User):
    def __init__(self, name, id, password, pump, balance):
        super().__init__(name, id, password)
        self.pump = pump
        self.balance = balance
        self.view = AppView(ViewType.CUSTOMER)

    def get_view(self):
        return self.view

    def get_pump(self):
        return self.pump
    
    def get_balance(self):
        return self.balance

    def adjust_balance(self, amount):
        self.balance += amount

class Employee(User):
    # technically this init is unneeded but useful to have in case employees need more attributes later o7
    def __init__(self, name, id, password):
        super().__init__(name, id, password)
        self.view = AppView(ViewType.EMPLOYEE)

    def get_view(self):
        return self.view

    def notify(self, pump):
        if type(pump) == Pump:
            if pump.get_status() == PumpStatus.YELLOW:
                self.alerts.append("ALERT: Pump " + pump.get_id() + " requires maintenance")
            elif pump.get_status() == PumpStatus.RED:
                self.alerts.append("ALERT: Pump " + pump.get_id() + " requires urgent maintenance")
        elif type(pump) == LevelMeter:
            if pump.get_status() >= 60:
                self.alerts.append("ALERT: Level Meter " + pump.get_id() + " is at a low water level")
            else:
                self.alerts.append("ALERT: Level Meter " + pump.get_id() + " is at a severely low water level")
                
        print("I have been notified about " + pump.get_id())

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

class AppView():
    def __init__(self, view_type):
        # defaults to english for ease of english-speaking software developers
        self.language = UserLanguage.ENGLISH
        self.view_mode = ViewMode.DARK
        if type(view_type) == ViewType:
            self.view_type = view_type
        else:
            self.view_type = ViewType.CUSTOMER
        self.measure = MeasureSystem.METRIC

class PumpStatus(Enum):
    GREEN = 1
    YELLOW = 2
    RED = 3

class UserLanguage(Enum):
    AFRIKAANS = 0
    ENGLISH = 1
    SEPEDI = 2
    SOUTHERN_NDEBELE = 3
    SOUTHERN_SOTHO = 4
    SWAZI = 5
    TSONGA = 6
    TSWANA = 7
    XHOSA = 8
    VENDA = 9
    ZULU = 10

class ViewMode(Enum):
    DARK = 0
    LIGHT = 1

class ViewType(Enum):
    CUSTOMER = 0
    EMPLOYEE = 1

class MeasureSystem(Enum):
    METRIC = 0
    IMPERIAL = 1

current_backend = Backend()

def run_test():
    current_backend.new_pump("12345")
    #print(backend.get_pump(0).get_id())

    current_backend.new_employee("John Smith", "ABCDE", "supersecurepassword")
    #print(backend.get_employee(0).get_name())
    #print(backend.get_pump(0).get_maintenance(0).get_name())

    current_backend.new_customer("Smohn Jith", "FGHIJ", "correcthorsebatterystaple", "12345")
    #print(backend.get_customer(0).get_pump().get_id())
    #print(backend.get_customer("FGHIJ").get_name())

    current_backend.new_customer("test", "test", "test", "12345")

    #backend.login("XYZZY", "invalidpassword")
    #backend.login("ABCDE", "invalidpassword")
    #current_backend.login("ABCDE", "supersecurepassword")

    print(current_backend.current_view.language)
    print(current_backend.current_view.view_type)

    current_backend.get_pump("12345").check_damage(40)
    current_backend.get_pump("12345").notify_damage()



run_test()
     

