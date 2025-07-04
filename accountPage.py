import tkinter as tk
from tkinter import ttk
import backend
from page import AppPage

class Water(AppPage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.columnconfigure(0, weight=1)
        
        shop = Shop(self)
        shop.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

class Shop(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        current_user = backend.current_backend.get_current_user()

        ttk.Label(self, text="Water Meter Account", font=backend.current_backend.get_font("default_bold")).grid(row=0, column=0, sticky="w", padx=10)
        meter_listbox = tk.Listbox(self, height=5, font=backend.current_backend.get_font())
        meter_listbox.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        if isinstance(current_user, backend.User):
            account_details = current_user.get_account_details()
            for i, detail in enumerate(account_details):
                meter_listbox.insert(i, detail)
        else:
            meter_listbox.insert(0, "Log in to view your account details.")


        ttk.Label(self, text="Purchase Water Vouchers", font=backend.current_backend.get_font("default_bold")).grid(row=2, column=0, sticky="w", padx=10, pady=(10,0))
        branches_listbox = tk.Listbox(self, font=backend.current_backend.get_font())
        branches_listbox.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        
        all_regions = backend.current_backend.get_all_regions()
        if all_regions:
            branches_listbox.insert(0, "Available at Pick'n'Pay stores in:")
            for i, region in enumerate(all_regions, 1):
                branches_listbox.insert(i, f" - {region}")
        else:
            branches_listbox.insert(0, "No regions found.")