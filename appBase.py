import tkinter as tk
from tkinter import ttk, messagebox
from PIL import ImageTk, Image
import homePage
import statusPage
import accountPage
import loginPage
import backend
import settings

class Application(tk.Tk):
    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()

        if frame_class != loginPage.Login:
            if self.profile is not None:
                self.profile.destroy()

            if self.section is not None:
                self.section.destroy()
            
            self.profile = Profile(self, controller=self)
            self.profile.grid(row=0, column=0, sticky="new", padx=5, pady=5)

            self.section = Section(self, controller=self)
            self.section.grid(row=2, column=0, sticky="sew", padx=5, pady=5)
            
        self.current_frame = frame_class(self.container, controller=self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def update_ttk_styles(self):
        s = ttk.Style()
        default_font = backend.current_backend.get_font("default")
        bold_font = backend.current_backend.get_font("default_bold")
        
        s.configure('TButton', font=default_font)
        s.configure('TCheckbutton', font=default_font)
        s.configure('TLabelframe.Label', font=bold_font)

    def __init__(self):
        super().__init__()
        self.title("Hydr8")
        self.geometry("300x570")
        self.resizable(False, False)

        self.update_ttk_styles()

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.container = ttk.Frame(self, width=300, height=400)
        self.container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        self.profile = None
        self.section = None
        self.current_frame = None
        self.show_frame(homePage.Home)

class Profile(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.columnconfigure(2, weight=1)

        self.current_user = backend.current_backend.get_current_user()

        self.userIcon = Image.open("images/userIcon.png").resize((40, 40))
        self.userIcon = ImageTk.PhotoImage(self.userIcon)

        self.userIcon_label = tk.Label(self, image=self.userIcon, cursor="hand2")
        self.userIcon_label.grid(row=0, column=0, columnspan=1, sticky="w", pady=2)
        self.userIcon_label.bind("<Button-1>", self.handle_profile_click)

        if self.current_user:
            login_text = self.current_user.get_name()
        else:
            login_text = "Click to sign in"

        self.userName_label = tk.Label(self, text=login_text, font=backend.current_backend.get_font(), cursor="hand2")
        self.userName_label.grid(row=0, column=1, columnspan=1, sticky="w", padx=5)
        self.userName_label.bind("<Button-1>", self.handle_profile_click)

        self.settingIcon = Image.open("images/settingIcon.png").resize((40, 40))
        self.settingIcon = ImageTk.PhotoImage(self.settingIcon)

        self.settingIcon_button = ttk.Button(self, image=self.settingIcon, command=lambda: self.controller.show_frame(settings.Settings))
        self.settingIcon_button.grid(row=0, column=2, columnspan=1, sticky="e", pady=2)

    def handle_profile_click(self, event=None):
        if self.current_user:
            self.prompt_logout()
        else:
            self.controller.show_frame(loginPage.Login)

    def prompt_logout(self, event=None):
        response = messagebox.askyesno("Logout", "Are you sure you want to log out?")
        if response:
            backend.current_backend.logout()
            self.controller.show_frame(homePage.Home)


class Section(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        def open_home():
            self.controller.show_frame(homePage.Home)

        def open_water():
            self.controller.show_frame(accountPage.Water)

        def open_map():
            self.controller.show_frame(statusPage.Map)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.maintenanceIcon = Image.open("images/maintenanceIcon.png").resize((40, 40))
        self.maintenanceIcon = ImageTk.PhotoImage(self.maintenanceIcon)

        self.maintenanceIcon_btn = ttk.Button(self, image=self.maintenanceIcon, command=open_map)
        self.maintenanceIcon_btn.grid(row=0, column=0, columnspan=1, sticky="nsew")

        self.homeIcon = Image.open("images/homeIcon.png").resize((40, 40))
        self.homeIcon = ImageTk.PhotoImage(self.homeIcon)

        self.homeIcon_btn = ttk.Button(self, image=self.homeIcon, command=open_home)
        self.homeIcon_btn.grid(row=0, column=1, columnspan=1, sticky="nsew")

        self.waterIcon = Image.open("images/waterIcon.png").resize((40, 40))
        self.waterIcon = ImageTk.PhotoImage(self.waterIcon)

        self.waterIcon_btn = ttk.Button(self, image=self.waterIcon, command=open_water)
        self.waterIcon_btn.grid(row=0, column=2, columnspan=1, sticky="nsew")