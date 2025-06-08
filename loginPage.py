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
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        #Label of app title, "Hydr8"
        self.appTitle_label = tk.Label(self, text="Hydr8", font=('calibre', 25,'bold'))
        self.appTitle_label.grid(row=0, column=0, columnspan=2, sticky="new", pady=(0, 20))

        #Opening and creating user icon image
        self.userIcon = Image.open("images/userIcon.png").resize((100, 100))
        self.userIcon = ImageTk.PhotoImage(self.userIcon)

        #Using label to place the user icon image
        self.userIcon_label = tk.Label(self, image=self.userIcon)
        self.userIcon_label.grid(row=1, column=0, columnspan=2, sticky="ew", pady=30)

        notification = LoginBox(self,controller=controller)
        notification.grid(row=2, column=0, sticky="new", padx=5)

class LoginBox(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        def submit():
            #If login is successful
            if current_backend.login(nameBox.get(),passwordBox.get()):
                controller.show_frame(homePage.Home)
            #If login is unsuccessful
            else:
                loginWarning = ttk.Label(self, text = '*Incorrect user ID or password', font=('calibre',10, 'bold'))
                loginWarning.grid(row=3, column=0, columnspan=2, sticky="ew", pady=2)

        #Allows placeholder text inside the username entry box    
        def nameBox_focus_in(event):
            if nameBox.get() == "Username":
                nameBox.delete(0, tk.END)
                nameBox.configure(foreground="black")

        #Placeholder text can reappear if username entry box is empty
        def nameBox_focus_out(event):
            if nameBox.get() == "":
                nameBox.insert(0, "Username")
                nameBox.configure(foreground="gray")

        #Allows placeholder text inside the password entry box    
        def passwordBox_focus_in(event):
            if passwordBox.get() == "Password":
                passwordBox.config(show="*")
                passwordBox.delete(0, tk.END)
                passwordBox.configure(foreground="black")

        #Placeholder text can reappear if password entry box is empty
        def passwordBox_focus_out(event):
            if passwordBox.get() == "":
                passwordBox.config(show="")
                passwordBox.insert(0, "Password")
                passwordBox.configure(foreground="gray")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        #Username entry details
        #nameLabel = ttk.Label(self, text = 'Username', font=('calibre',10, 'bold'))
        nameBox = ttk.Entry(self, font=('calibre',10,'normal'), foreground="gray")
        nameBox.insert(0, "Username")
        nameBox.bind("<FocusIn>", nameBox_focus_in)
        nameBox.bind("<FocusOut>", nameBox_focus_out)

        #Password entry details
        #passwordLabel = ttk.Label(self, text = 'Password', font = ('calibre',10,'bold'))
        passwordBox = ttk.Entry(self, font = ('calibre',10,'normal'), foreground="gray")
        passwordBox.insert(0, "Password")
        passwordBox.bind("<FocusIn>", passwordBox_focus_in)
        passwordBox.bind("<FocusOut>", passwordBox_focus_out)

        submitButton=ttk.Button(self,text = 'Submit', command = submit)
        #nameLabel.grid(row=1,column=0)
        nameBox.grid(row=0,column=0, columnspan=2, sticky="ew", pady=5)
        #passwordLabel.grid(row=2,column=0)
        passwordBox.grid(row=1,column=0, columnspan=2, sticky="ew", pady=5)
        submitButton.grid(row=2,column=0, columnspan=2, pady=10)