import appBase
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


##def main():
##    water = Water()
##    water.mainloop()

class Water(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        shop = Shop(self)
        shop.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

class Shop(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        #Water metre
        self.metreLabel = ttk.Label(self, text="Water Metre Account", width=43)
        self.metreLabel.grid(row=0, column=0, columnspan=1, sticky="w", padx=10)
        self.metre = tk.Listbox(self)
        self.metre.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)

        #Picknpay branches
        self.branchesLabel = ttk.Label(self, text="Pick'n'Pay Branches", width=43)
        self.branchesLabel.grid(row=2, column=0, columnspan=1, sticky="w", padx=10)
        self.branches = tk.Listbox(self)
        self.branches.grid(row=3, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)

if __name__ == "__main__":
    main()
