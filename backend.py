import sqlite3
from enum import Enum
import bcrypt

DB_FILE = "database.db"

def hash_new_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')

def verify_password(stored_hash, provided_password):
    if not stored_hash or not provided_password:
        return False
    password_bytes = provided_password.encode('utf-8')
    stored_hash_bytes = stored_hash.encode('utf-8')
    try:
        return bcrypt.checkpw(password_bytes, stored_hash_bytes)
    except ValueError:
        return False

def db_query(query, params=()):
    try:
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        cur.execute(query, params)
        results = cur.fetchall()
        con.close()
        return results
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def db_execute(query, params=()):
    try:
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()
        cur.execute(query, params)
        con.commit()
        con.close()
        return True
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

class PumpStatus(Enum):
    GREEN = 1
    YELLOW = 2
    RED = 3

class UserLanguage(Enum):
    ENGLISH = "English"
    AFRIKAANS = "Afrikaans"
    ZULU = "isiZulu"

class ViewType(Enum):
    CUSTOMER = 0
    EMPLOYEE = 1
    
class MeasureSystem(Enum):
    METRIC = "Metric"
    IMPERIAL = "Imperial"

class TrackedPoint():
    def __init__(self, id, integrity, active):
        self.id = id
        self.integrity = integrity
        self.active = active if active == 1 else False
        self.status = self._get_status_from_integrity()

    def _get_status_from_integrity(self):
        if not self.active:
            return PumpStatus.GREEN
        if self.integrity >= 90:
            return PumpStatus.GREEN
        elif self.integrity >= 50:
            return PumpStatus.YELLOW
        else:
            return PumpStatus.RED

    def get_status(self):
        return self.status
    
    def get_id(self):
        return self.id
    
    def get_integrity(self):
        return self.integrity

class Pump(TrackedPoint):
    def __init__(self, id, integrity, active, water_usage, region=None):
        super().__init__(id, integrity, active)
        self.water_usage = water_usage
        self.region = region

    def get_water_usage(self):
        return self.water_usage

class WaterTank(TrackedPoint):
    def __init__(self, id, integrity, active, water_level, region=None):
        super().__init__(id, integrity, active)
        self.water_level = water_level
        self.region = region
    
    def get_water_level(self):
        return self.water_level

class AppView():
    def __init__(self, view_type):
        self.language = UserLanguage.ENGLISH
        self.view_type = view_type
        self.measure = MeasureSystem.METRIC

class User:
    def __init__(self, id, name, region):
        self.id = id
        self.name = name
        self.region = region

    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.id

class Customer(User):
    def __init__(self, id, name, region, balance, water_usage):
        super().__init__(id, name, region)
        self.balance = balance
        self.water_usage = water_usage

    def get_alerts(self):
        critical_pumps = db_query("SELECT PumpID FROM WaterPump WHERE Region = ? AND Active = 1 AND Integrity < 50", (self.region,))
        if critical_pumps:
            return ["ALERT: There are disruptions in the water network that may impact you."]
        return []
        
    def get_account_details(self):
        converted_usage, unit_label = current_backend.convert_volume(self.water_usage)
        return [
            f"Customer Name: {self.get_name()}",
            f"Region: {self.region}",
            f"Account Balance: R{self.get_balance():.2f}",
            f"Monthly Water Usage: {converted_usage:,.1f} {unit_label}"
        ]

    def get_balance(self):
        return self.balance
    
    def adjust_balance(self, amount):
        current_backend.update_customer_balance(self.get_id(), amount)
        self.balance += amount


class Employee(User):
    def __init__(self, id, name, region, role, access_level):
        super().__init__(id, name, region)
        self.role = role
        self.access_level = access_level

    def get_alerts(self):
        tasks = db_query("SELECT Description, Priority FROM Task WHERE StaffNo = ? AND Completed = 0 ORDER BY Priority", (self.get_id(),))
        return [f"PRIORITY: {priority} - {desc}" for desc, priority in tasks]

class Backend:
    def __init__(self):
        self.current_user_id = None
        self.current_user_type = None
        self.view_settings = AppView(ViewType.CUSTOMER)
        self.font_config = {}
        self.set_font_size("Medium")

    def login(self, username, password):
        customer_data = db_query("SELECT CustNo, Password FROM Customer WHERE Name = ?", (username,))
        if customer_data:
            cust_no, stored_password = customer_data[0]
            if verify_password(stored_password, password):
                self.current_user_id = cust_no
                self.current_user_type = 'customer'
                print(f"Customer '{username}' logged in successfully.")
                return True

        staff_data = db_query("SELECT StaffNo, Password FROM Staff WHERE Name = ?", (username,))
        if staff_data:
            staff_no, stored_password = staff_data[0]
            if verify_password(stored_password, password):
                self.current_user_id = staff_no
                self.current_user_type = 'staff'
                print(f"Staff '{username}' logged in successfully.")
                return True

        print(f"Login failed for user '{username}'.")
        return False

    def logout(self):
        self.current_user_id = None
        self.current_user_type = None

    def get_current_user(self):
        if self.current_user_type == 'customer':
            return self.get_customer(self.current_user_id)
        elif self.current_user_type == 'staff':
            return self.get_employee(self.current_user_id)
        return None

    def get_current_id(self):
        return self.current_user_id

    def change_password(self, user_id, old_password, new_password):
        table = "Customer" if self.current_user_type == 'customer' else "Staff"
        id_col = "CustNo" if self.current_user_type == 'customer' else "StaffNo"
        
        user_data = db_query(f"SELECT Password FROM {table} WHERE {id_col} = ?", (user_id,))
        if not user_data or not verify_password(user_data[0][0], old_password):
            return False, "Current password is not correct."

        new_hashed_password = hash_new_password(new_password)
        success = db_execute(f"UPDATE {table} SET Password = ? WHERE {id_col} = ?", (new_hashed_password, user_id))
        
        if success:
            return True, "Password updated successfully."
        else:
            return False, "An error occurred while updating the password."

    def get_customer(self, cust_no):
        data = db_query("SELECT CustNo, Name, Region, Balance, WaterUsage FROM Customer WHERE CustNo = ?", (cust_no,))
        return Customer(*data[0]) if data else None

    def get_employee(self, staff_no):
        data = db_query("SELECT StaffNo, Name, Region, Role, AccessLevel FROM Staff WHERE StaffNo = ?", (staff_no,))
        return Employee(*data[0]) if data else None

    def update_customer_balance(self, customer_id, amount):
        return db_execute("UPDATE Customer SET Balance = Balance + ? WHERE CustNo = ?", (amount, customer_id))

    def get_infrastructure_by_region(self, region):
        pumps_data = db_query("SELECT PumpID, Integrity, Active, WaterUsage FROM WaterPump WHERE Region = ?", (region,))
        tanks_data = db_query("SELECT TankID, Integrity, Active, WaterLevel FROM WaterTank WHERE Region = ?", (region,))
        pumps = [Pump(p[0], p[1], p[2], p[3]) for p in pumps_data]
        tanks = [WaterTank(t[0], t[1], t[2], t[3]) for t in tanks_data]
        return {'pumps': pumps, 'tanks': tanks}

    def get_all_infrastructure(self):
        pumps_data = db_query("SELECT PumpID, Integrity, Active, WaterUsage, Region FROM WaterPump ORDER BY Region, PumpID")
        tanks_data = db_query("SELECT TankID, Integrity, Active, WaterLevel, Region FROM WaterTank ORDER BY Region, TankID")
        pumps = [Pump(p[0], p[1], p[2], p[3], p[4]) for p in pumps_data]
        tanks = [WaterTank(t[0], t[1], t[2], t[3], t[4]) for t in tanks_data]
        return {'pumps': pumps, 'tanks': tanks}

    def get_all_regions(self):
        regions = db_query("SELECT DISTINCT Region FROM WaterPump UNION SELECT DISTINCT Region FROM WaterTank")
        return [region[0] for region in regions if region[0] is not None]
    
    def submit_report(self, cust_no, description):
        if not description or not cust_no:
            return False
        return db_execute("INSERT INTO Report (CustNo, Description) VALUES (?, ?)", (cust_no, description))

    def get_all_reports(self):
        query = """
            SELECT substr(r.DateAndTime, 1, 16), c.Name, r.Description
            FROM Report r
            JOIN Customer c ON r.CustNo = c.CustNo
            ORDER BY r.DateAndTime DESC
        """
        reports_data = db_query(query)
        return [f"[{date}] From {name}: {desc}" for date, name, desc in reports_data]
        
    def set_language(self, language):
        self.view_settings.language = UserLanguage(language)

    def get_language(self):
        return self.view_settings.language.value
        
    def set_measurement_unit(self, unit_string):
        self.view_settings.measure = MeasureSystem("Imperial" if "Imperial" in unit_string else "Metric")
        
    def get_measurement_unit_string(self):
        return f"{self.view_settings.measure.value} (Liters)" if self.view_settings.measure == MeasureSystem.METRIC else f"{self.view_settings.measure.value} (Gallons)"

    def convert_volume(self, value_liters):
        if self.view_settings.measure == MeasureSystem.IMPERIAL:
            return (value_liters * 0.264172, "gal")
        return (value_liters, "L")
        
    def set_font_size(self, size_str):
        self.font_size_str = size_str
        base_size = 10
        if size_str == "Small":
            base_size = 8
        elif size_str == "Large":
            base_size = 12
        
        self.font_config = {
            "default": ("Calibre", base_size),
            "default_bold": ("Calibre", base_size, "bold"),
            "italic": ("Calibre", base_size, "italic"),
            "title": ("Calibre", base_size + 4, "bold"),
            "login_title": ("Calibre", base_size + 15, "bold"),
        }

    def get_font(self, name="default"):
        return self.font_config.get(name, ("Calibre", 10))
        
    def get_font_size(self):
        return self.font_size_str

current_backend = Backend()