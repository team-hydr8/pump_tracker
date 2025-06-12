from tkinter import ttk

class AppPage(ttk.Frame):
    def __init__(self, parent:ttk.Frame, controller): # controller = Application
        super().__init__(parent)
        self.controller = controller