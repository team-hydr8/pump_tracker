import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from backend import current_backend
import homePage

class Login(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.appTitle_label = tk.Label(self, text="Hydr8", font=current_backend.get_font("login_title"))
        self.appTitle_label.grid(row=0, column=0, columnspan=2, sticky="new", pady=(0, 20))

        self.userIcon = Image.open("images/userIcon.png").resize((100, 100))
        self.userIcon = ImageTk.PhotoImage(self.userIcon)

        self.userIcon_label = tk.Label(self, image=self.userIcon)
        self.userIcon_label.grid(row=1, column=0, columnspan=2, sticky="ew", pady=30)

        notification = LoginBox(self,controller=controller)
        notification.grid(row=2, column=0, sticky="new", padx=5)

class LoginBox(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.nameBox = ttk.Entry(self, font=current_backend.get_font(), foreground="gray")
        self.nameBox.insert(0, "Username")
        self.nameBox.bind("<FocusIn>", self.nameBox_focus_in)
        self.nameBox.bind("<FocusOut>", self.nameBox_focus_out)

        self.passwordBox = ttk.Entry(self, font=current_backend.get_font(), foreground="gray")
        self.passwordBox.insert(0, "Password")
        self.passwordBox.bind("<FocusIn>", self.passwordBox_focus_in)
        self.passwordBox.bind("<FocusOut>", self.passwordBox_focus_out)
        self.passwordBox.bind("<Return>", self.submit_on_enter)

        self.hide = tk.IntVar()
        checkbox = ttk.Checkbutton(self, text="show password", variable=self.hide, onvalue=1, offvalue=0, command=self.show_password)

        submitButton=ttk.Button(self,text = 'Submit', command=self.submit)

        self.nameBox.grid(row=0,column=0, columnspan=2, sticky="ew", pady=5)
        self.passwordBox.grid(row=1,column=0, columnspan=2, sticky="ew", pady=5)
        checkbox.grid(row=2, column=0, sticky="w")
        submitButton.grid(row=3,column=0, columnspan=2, pady=10)
        self.columnconfigure(0, weight=1)

    def submit(self):
        if current_backend.login(self.nameBox.get(), self.passwordBox.get()):
            self.controller.show_frame(homePage.Home)
        else:
            loginWarning = ttk.Label(self, text = '*Incorrect user ID or password', font=current_backend.get_font("default_bold"), foreground="red")
            loginWarning.grid(row=4, column=0, columnspan=2, sticky="ew", pady=2)

    def submit_on_enter(self, event):
        self.submit()

    def nameBox_focus_in(self, event):
        if self.nameBox.get() == "Username":
            self.nameBox.delete(0, tk.END)
            self.nameBox.configure(foreground="black")

    def nameBox_focus_out(self, event):
        if self.nameBox.get() == "":
            self.nameBox.insert(0, "Username")
            self.nameBox.configure(foreground="gray")

    def passwordBox_focus_in(self, event):
        if self.passwordBox.get() == "Password":
            if self.hide.get() == 0:
                self.passwordBox.config(show="*")
            self.passwordBox.delete(0, tk.END)
            self.passwordBox.configure(foreground="black")

    def passwordBox_focus_out(self, event):
        if self.passwordBox.get() == "":
            self.passwordBox.config(show="")
            self.passwordBox.insert(0, "Password")
            self.passwordBox.configure(foreground="gray")

    def show_password(self):
        if self.passwordBox.get() == "Password":
            return
        
        if self.hide.get() == 1:
            self.passwordBox.config(show="")
        else:
            self.passwordBox.config(show="*")
