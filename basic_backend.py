from enum import Enum

# main backend class
class Backend():
    def __init__(self):
        self.employees = []
        self.customers = []
        self.pumps = []
        self.meters = []
        self.current_view = AppView(ViewType.CUSTOMER)
        self.current_id = "none"

    # methods to create new instances of each major object and add to their respective array
    def new_employee(self, name, id, password):
        new_emp = Employee(name, id, password)

        self.employees.append(new_emp)

    def new_pump(self, id):
        new_p = Pump(id)
        self.pumps.append(new_p)

    def new_meter(self, id):
        new_m = LevelMeter(id)
        self.meters.append(new_m)

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
        self.customers.append(new_customer)

    # login function – user_id is equivalent to a username
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

    # getters
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
            for i in range(len(self.meters)):
                if self.meters[i].get_id() == key:
                    return self.meters[i]
                
    def get_current_view(self):
        return self.current_view
    
    def get_current_id(self):
        return self.current_id
                
    # built-in method to update a balance - remove money by having negative amount
    def update_customer_balance(self, customer_id, amount):
        self.get_customer(customer_id).adjust_balance(amount)

    def notify_point(self, point_id):
        is_pump = False
        for i in range(len(self.customers)):
            if self.pumps[i].get_id() == point_id:
                is_pump = True

        if is_pump:
            if self.get_pump(point_id).get_status() != PumpStatus.GREEN:
                for i in range(len(self.employees)):
                    self.employees[i].notify(self.get_pump(point_id))
            
            if self.get_pump(point_id).get_status() == PumpStatus.RED:
                for i in range(len(self.customers)):
                    if self.customers[i].get_pump().get_id() == point_id:
                        self.customers[i].notify()
        else:
            if self.get_level_meter(point_id).get_status() < 85:
                for i in range(len(self.employees)):
                    self.employees[i].notify(self.get_level_meter(point_id))


# User classes
class User():
    def __init__(self, name, id, password):
        self.name = name
        self.id = id
        self.password = password
        self.alerts = []
    
    # potential future security improvement here
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
    
    # notify method - currently adds to a list of alerts that can be got, can be edited if the UI team need
    def notify(self):
        self.alerts.append("ALERT: There are disruptions in the water network that may impact you.")
        print("I have been notified")

# worth noting – the associated pump here is the pump that serves the customer. 
# customers should not be alerted about all pumps, this may be a security risk
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

    # method to adjust prepaid balance
    def adjust_balance(self, amount):
        self.balance += amount

class Employee(User):
    def __init__(self, name, id, password):
        super().__init__(name, id, password)
        self.view = AppView(ViewType.EMPLOYEE)

    def get_view(self):
        return self.view

    # more in-depth notification for employees
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

# classes for the tracked points on the map
class TrackedPoint():
    def __init__(self, id):
        self.id = id
        self.status = PumpStatus.GREEN

    def get_status(self):
        return self.status
    
    def get_id(self):
        return self.id
    
    # input data is the reading from whatever hypothetical damage-detectors (or maybe just maintenance reports) 
    # should be a number from 0-100 where 100 represents something that is at 100% integrity
    def check_damage(self, data):
        if data >= 90:
            self.status = PumpStatus.GREEN
        elif data >= 50:
            self.status = PumpStatus.YELLOW
        else:
            self.status = PumpStatus.RED

class Pump(TrackedPoint):
    # a bit redundant now but worth differentiating in case of future changes
    def __init__(self, id):
        super().__init__(id)

# customers should never be notified about level meters – these are internal
# also level meters use the raw percentage instead of green/yellow/red abstraction
class LevelMeter(TrackedPoint):
    def __init__(self, id):
        super().__init__(id)
        self.status = 100

    def check_damage(self, data):
        self.status = data

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

# assorted enums
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

# test functions
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
    current_backend.notify_point("12345")
    current_backend.get_pump("12345").notify_damage()

run_test()
     

