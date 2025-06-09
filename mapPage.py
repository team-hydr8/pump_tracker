import appBase
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image


##def main():
##    map = Map()
##    map.mainloop()

class Map(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
  
        mapSection = MapSection(self)
        mapSection.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

class MapSection(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        #Map displayed
        self.mapLabel = ttk.Label(self, text="Water Levels + Pump Integrity")
        self.mapLabel.grid(row=0, column=0, columnspan=1, sticky="w", padx=10)
        self.mapSection = tk.Listbox(self, width=43, height=25)
        self.mapSection.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=10, pady=10)


if __name__ == "__main__":
    main()
