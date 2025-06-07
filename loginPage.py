import appBase
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from basic_backend import current_backend
import appBase
import homePage


##def main():
##    home = Home()
##    home.mainloop()

class Login(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        notification = LoginBox(self,controller=controller)
        notification.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

class LoginBox(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        def submit():          
            if current_backend.login(nameBox.get(),passwordBox.get()):
                controller.show_frame(homePage.Home)
            

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)

        nameLabel = tk.Label(self, text = 'Username', font=('calibre',10, 'bold'))
        nameBox = tk.Entry(self, font=('calibre',10,'normal'))
        passwordLabel = tk.Label(self, text = 'Password', font = ('calibre',10,'bold'))
        passwordBox = tk.Entry(self, font = ('calibre',10,'normal'), show = '*')
        submitButton=tk.Button(self,text = 'Submit', command = submit)
        nameLabel.grid(row=0,column=0)
        nameBox.grid(row=0,column=1)
        passwordLabel.grid(row=1,column=0)
        passwordBox.grid(row=1,column=1)
        submitButton.grid(row=2,column=1)