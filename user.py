# User and its subclasses (Customer, Employee)
from tracked_point import Pump, LevelMeter
from view import AppView
from enums import ViewType, PumpStatus

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