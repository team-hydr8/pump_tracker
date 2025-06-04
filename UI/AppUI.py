import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("App UI")
root.geometry("720x1100")

top_bit = tk.Frame(root)
top_bit.grid(row=0, column=0, pady=10)
top_bit.columnconfigure(0, weight=1)
top_bit.rowconfigure(0, weight=1)

#To do later
#profile = PhotoImage(file='./Images/profile.png')

user_profile = ttk.Label(top_bit, text="Not signed in")
user_profile.grid(row=0,column=0)

# ------------------------------------------------------------

main = tk.Frame(root)
main.grid(row=1, column=0, pady=10)
main.columnconfigure(0, weight=1)
main.rowconfigure(0, weight=1)

#--------------------------------------------------------------

section = tk.Frame(root)
section.grid(row=2, column=0, columnspan=3)
section.columnconfigure(0, weight=1)
section.rowconfigure(0, weight=1)

maintenance = tk.Button(section, text="maintenance")
maintenance.grid(column=0, row=0)

home = tk.Button(section, text="home")
home.grid(column=1, row=0)

water = tk.Button(section, text="water")
water.grid(column=2, row=0)

root.mainloop()