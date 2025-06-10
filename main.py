from tkinter import PhotoImage
from appBase import Application

app = Application()
try:
    app.iconbitmap("images/logo.ico")
except:
    # On MacOS, Linux and other platforms iconbitmap throws an error so use this instead
    # https://stackoverflow.com/questions/52826692/set-tkinter-icon-on-mac-os
    img = PhotoImage(file="images/logo.png")
    app.tk.call("wm", "iconphoto", app._w, img)

app.mainloop()