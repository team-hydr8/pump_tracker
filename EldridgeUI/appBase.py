import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import homePage
import mapPage
import waterPage

def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(self.container, controller=self)
        self.current_frame.grid(row=0, column=0, sticky="nsew")
        
    
    def __init__(self):
        super().__init__()
        self.title("Hydr8")
        self.geometry("300x570")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.profile = Profile(self)
        self.profile.grid(row=0, column=0, sticky="new", padx=5, pady=5)

        self.container = ttk.Frame(self, width=300, height=400)
        self.container.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.container.columnconfigure(0, weight=1)
        self.container.rowconfigure(0, weight=1)

        self.section = Section(self, controller=self)
        self.section.grid(row=2, column=0, sticky="sew", padx=5, pady=5)

        self.current_frame = None
        self.show_frame(homePage.Home)  # default view

class Profile(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        #self.columnconfigure(0, weight=0)
        #self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        #Opening and creating user icon image
        self.userIcon = Image.open("images/userIcon.png").resize((40, 40))
        self.userIcon = ImageTk.PhotoImage(self.userIcon)

        #Using label to place the user icon image
        self.userIcon_label = tk.Label(self, image=self.userIcon)
        self.userIcon_label.grid(row=0, column=0, columnspan=1, sticky="w", pady=2)

        #Label of user's name
        self.userName_label = tk.Label(self, text="Not logged in")
        self.userName_label.grid(row=0, column=1, columnspan=1, sticky="w")

        #Opening and creating user icon image
        self.settingIcon = Image.open("images/settingIcon.png").resize((40, 40))
        self.settingIcon = ImageTk.PhotoImage(self.settingIcon)

        #Using label to place the user icon image
        self.settingIcon_button = ttk.Button(self, image=self.settingIcon)
        self.settingIcon_button.grid(row=0, column=2, columnspan=1, sticky="e", pady=2)


#class InputForm(ttk.Frame):
#    def __init__(self, parent):
#        super().__init__(parent)
#        
#        self.columnconfigure(0, weight=1)
#        self.rowconfigure(1, weight=1)
#
#        self.entry = ttk.Entry(self)
#        self.entry.grid(row=0, column=0, sticky="ew")
#
#        self.entry.bind("<Return>", self.add_to_list)
#
#        self.entry_btn = ttk.Button(self, text="Send Feedback", command=self.add_to_list)
#        self.entry_btn.grid(row=0, column=1)
#
#        self.clear_btn = ttk.Button(self, text="Clear", command=self.clear_list)
#
#        self.text_list = tk.Listbox(self)
#        self.text_list.grid(row=1, column=0, columnspan=2, sticky="nsew")
#
#    def add_to_list(self, event=None):
#        text = self.entry.get()
#        if text:
#            self.text_list.insert(tk.END, text)
#            self.entry.delete(0, tk.END)
#
#    def clear_list(self):
#        self.text_list.delete(0, tk.END)


class Section(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        def open_home():
            self.controller.show_frame(homePage.Home)

        def open_water():
            self.controller.show_frame(waterPage.Water)

        def open_map():
            self.controller.show_frame(mapPage.Map)


        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        #Opening and creating maintenance icon image
        self.maintenanceIcon = Image.open("images/maintenanceIcon.png").resize((40, 40))
        self.maintenanceIcon = ImageTk.PhotoImage(self.maintenanceIcon)

        #Using label to place the maintenance icon image
        self.maintenanceIcon_btn = ttk.Button(self, image=self.maintenanceIcon, command=open_map)
        self.maintenanceIcon_btn.grid(row=0, column=0, columnspan=1, sticky="nsew")

        #Opening and creating home icon image
        self.homeIcon = Image.open("images/homeIcon.png").resize((40, 40))
        self.homeIcon = ImageTk.PhotoImage(self.homeIcon)

        #Using label to place the home icon image
        self.homeIcon_btn = ttk.Button(self, image=self.homeIcon, command=open_home)
        self.homeIcon_btn.grid(row=0, column=1, columnspan=1, sticky="nsew")

        #Opening and creating water icon image
        self.waterIcon = Image.open("images/waterIcon.png").resize((40, 40))
        self.waterIcon = ImageTk.PhotoImage(self.waterIcon)

        #Using label to place the water icon image
        self.waterIcon_btn = ttk.Button(self, image=self.waterIcon, command=open_water)
        self.waterIcon_btn.grid(row=0, column=2, columnspan=1, sticky="nsew")



if __name__ == "__main__":
    main()

