import appBase
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import basic_backend


##def main():
##    home = Home()
##    home.mainloop()

class Home(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        notification = Notification(self)
        notification.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

class Notification(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        #Alerts displayed
        self.alertLabel = ttk.Label(self, text="Alerts", width=43)
        self.alertLabel.grid(row=0, column=0, columnspan=1, sticky="w", padx=10)
        self.alerts = tk.Listbox(self)
        self.alerts.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)

        user_alerts = basic_backend.current_backend.get_customer(basic_backend.current_backend.current_id).get_alerts()
        for i in range(len(user_alerts)):
            self.alerts.insert(user_alerts[i])

        #Notices displayed
        self.noticeLabel = ttk.Label(self, text="Notices", width=43)
        self.noticeLabel.grid(row=2, column=0, columnspan=1, sticky="w", padx=10)
        self.notices = tk.Listbox(self)
        self.notices.grid(row=3, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)