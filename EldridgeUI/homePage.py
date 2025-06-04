import appBase
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


def main():
    home = Home()
    home.mainloop()

class Home(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hydr8")

        self.geometry('300x570')
        self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        #self.rowconfigure(2, weight=1)

        profile = appBase.Profile(self)
        profile.grid(row=0, column=0, sticky="new", padx=5, pady=5)

        notification = Notification(self)
        notification.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        section = appBase.Section(self)
        section.grid(row=2, column=0, sticky="sew", padx=5, pady=5)

class Notification(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        #Alerts displayed
        self.alertLabel = ttk.Label(self, text="Alerts")
        self.alertLabel.grid(row=0, column=0, columnspan=1, sticky="w", padx=10)
        self.alerts = tk.Listbox(self)
        self.alerts.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)

        #Notices displayed
        self.noticeLabel = ttk.Label(self, text="Notices")
        self.noticeLabel.grid(row=2, column=0, columnspan=1, sticky="w", padx=10)
        self.notices = tk.Listbox(self)
        self.notices.grid(row=3, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)

if __name__ == "__main__":
    main()