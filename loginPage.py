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

        def submit():
            if current_backend.login(nameBox.get(),passwordBox.get()):
                controller.show_frame(homePage.Home)
            else:
                loginWarning = ttk.Label(self, text = '*Incorrect user ID or password', font=current_backend.get_font("default_bold"), foreground="red")
                loginWarning.grid(row=4, column=0, columnspan=2, sticky="ew", pady=2)

        def submit_on_enter(event):
            submit()

        def nameBox_focus_in(event):
            if nameBox.get() == "Username":
                nameBox.delete(0, tk.END)
                nameBox.configure(foreground="black")

        def nameBox_focus_out(event):
            if nameBox.get() == "":
                nameBox.insert(0, "Username")
                nameBox.configure(foreground="gray")

        def passwordBox_focus_in(event):
            if passwordBox.get() == "Password":
                if hide.get() == 0:
                    passwordBox.config(show="*")
                passwordBox.delete(0, tk.END)
                passwordBox.configure(foreground="black")

        def passwordBox_focus_out(event):
            if passwordBox.get() == "":
                passwordBox.config(show="")
                passwordBox.insert(0, "Password")
                passwordBox.configure(foreground="gray")

        def show_password():
            if passwordBox.get() == "Password":
                return
            
            if hide.get() == 1:
                passwordBox.config(show="")
            else:
                passwordBox.config(show="*")

        self.columnconfigure(0, weight=1)
        
        nameBox = ttk.Entry(self, font=current_backend.get_font(), foreground="gray")
        nameBox.insert(0, "Username")
        nameBox.bind("<FocusIn>", nameBox_focus_in)
        nameBox.bind("<FocusOut>", nameBox_focus_out)

        passwordBox = ttk.Entry(self, font=current_backend.get_font(), foreground="gray")
        passwordBox.insert(0, "Password")
        passwordBox.bind("<FocusIn>", passwordBox_focus_in)
        passwordBox.bind("<FocusOut>", passwordBox_focus_out)
        passwordBox.bind("<Return>", submit_on_enter)

        hide = tk.IntVar()
        checkbox = ttk.Checkbutton(self, text="show password", variable=hide, onvalue=1, offvalue=0, command= show_password)

        submitButton=ttk.Button(self,text = 'Submit', command = submit)

        nameBox.grid(row=0,column=0, columnspan=2, sticky="ew", pady=5)
        passwordBox.grid(row=1,column=0, columnspan=2, sticky="ew", pady=5)
        checkbox.grid(row=2, column=0, sticky="w")
        submitButton.grid(row=3,column=0, columnspan=2, pady=10)