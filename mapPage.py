import appBase
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import basic_backend


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
   
        pump = basic_backend.current_backend.get_customer(basic_backend.current_backend.current_id).get_pump()

        self.pump1Icon = Image.open("images/pump.png" if pump=="1" else "images/question.png").resize((80, 80))
        self.pump1Icon= ImageTk.PhotoImage(self.pump1Icon)

        self.pump1Icon_label = tk.Label(self, image=self.pump1Icon)
        self.pump1Icon_label.grid(row=1, column=0,  sticky="ew", pady=10)


        self.pump2Icon = Image.open("images/pump.png" if pump=="2" else "images/question.png").resize((80, 80))
        self.pump2Icon= ImageTk.PhotoImage(self.pump2Icon)

        self.pump2Icon_label = tk.Label(self, image=self.pump2Icon)
        self.pump2Icon_label.grid(row=5, column=0,  sticky="ew", pady=10)


        self.pump3Icon = Image.open("images/pump.png" if pump=="3" else "images/question.png").resize((80, 80))
        self.pump3Icon= ImageTk.PhotoImage(self.pump3Icon)

        self.pump3Icon_label = tk.Label(self, image=self.pump3Icon)
        self.pump3Icon_label.grid(row=1, column=2,  sticky="ew", pady=10)


        self.pipe1Icon = Image.open("images/pipeside.png" if pump=="1" or pump=="3" else "images/question.png").resize((80, 80))
        self.pipe1Icon= ImageTk.PhotoImage(self.pipe1Icon)

        self.pipe1Icon_label = tk.Label(self, image=self.pipe1Icon)
        self.pipe1Icon_label.grid(row=1, column=1,  sticky="ew", pady=10)


        self.pipe2Icon = Image.open("images/pipeup.png" if pump=="1" or pump=="2" else "images/question.png").resize((80, 80))
        self.pipe2Icon= ImageTk.PhotoImage(self.pipe2Icon)

        self.pipe2Icon_label = tk.Label(self, image=self.pipe2Icon)
        self.pipe2Icon_label.grid(row=3, column=0,  sticky="ew", pady=10)


        self.pipe3Icon = Image.open("images/pipeup.png" if pump=="3" else "images/question.png").resize((80, 80))
        self.pipe3Icon= ImageTk.PhotoImage(self.pipe3Icon)

        self.pipe3Icon_label = tk.Label(self, image=self.pipe3Icon)
        self.pipe3Icon_label.grid(row=3, column=2)
        
        self.pump1Text_label = tk.Label(self, text="STATUS:GREEN")
        self.pump1Text_label.grid(row=0, column=0)

        self.pump2Text_label = tk.Label(self, text="STATUS:GREEN")
        self.pump2Text_label.grid(row=4, column=0)

        self.pump3Text_label = tk.Label(self, text="STATUS:GREEN")
        self.pump3Text_label.grid(row=0, column=2)

        self.pipe1Text_label = tk.Label(self, text="100%")
        self.pipe1Text_label.grid(row=0, column=1)

        self.pipe2Text_label = tk.Label(self, text="100%")
        self.pipe2Text_label.grid(row=2, column=0)

        self.pipe3Text_label = tk.Label(self, text="100%")
        self.pipe3Text_label.grid(row=2, column=2)



        


