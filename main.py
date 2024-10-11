from tkinter import *
import sys
from tkinter import messagebox
from tkinter import ttk

from PIL import Image, ImageTk
class registerWindow(object):
    def __init__(self, master):
        top = self.top=Toplevel(master)
        self.user = Label(top, text = 'New Username')
        self.user.pack()
        self.user_entry = Entry(top)
        self.user_entry.pack()
        self.password = Label(top, text = 'New Password')
        self.password.pack()
        self.password_entry = Entry(top, show = '*')
        self.password_entry.pack()
        self.b_ok = Button(top, text = 'Ok', command = self.write_new)
        self.b_ok.pack()
        self.b_cancel = Button(top, text = 'Cancel', command = self.top.destroy)
        self.b_cancel.pack()
    def write_new(self):
        with open('users.txt', 'r') as f:
            l = 0
            for line in f:
                l += 1
            if l >= 10:
                t = messagebox.Message(self.top, message="Maximum Users Reached", type=messagebox.OK)
                t.show()
            else:
                self.write()

    def write(self):
        with open('users.txt', 'a') as f:
            user, passw = self.user_entry.get(), self.password_entry.get()
            if len(user) > 0 and len(passw) > 0:
                f.write(user + ',' + passw + '\n')
                t = messagebox.Message(message="User Created", type=messagebox.OK)
                t.show()
                self.top.destroy()
            else:
                t = messagebox.Message(self.top, message="User/Password Invalid", type=messagebox.OK)
                t.show()


class loggedinWindow(object):
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.style = ttk.Style(top)
        self.style.theme_use('forest-light')
        self.widgets_frame = ttk.Frame(top, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
        self.widgets_frame.columnconfigure(index=0, weight=1)
        self.LHR_spinbox = ttk.Spinbox(self.widgets_frame, from_=30, to=50)
        self.LHR_spinbox.insert(0)
        self.LHR_spinbox.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

    def exit(self):
        self.top.destroy()
        sys.exit()
class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.style = style

        self.img = ImageTk.PhotoImage(Image.open('./logo1.jpg'))
        self.panel = Label(master, image=self.img)
        self.panel.pack(padx=10, pady=10)

        self.username = Label(master, text='Username').pack(side=LEFT)
        self.e1 = Entry(master)
        self.e1.pack(side=LEFT)
        self.e2 = Entry(master, show="*")
        self.e2.pack(side=RIGHT)
        self.password = Label(master, text='Password').pack(side=RIGHT)
        self.w = Button(master, text='Register New', command=self.createNew)
        self.w.pack(side=BOTTOM)
        self.w = Button(master, text='Login', command=self.login)
        self.w.pack(side=BOTTOM)

    def createNew(self):
        self.resgister = registerWindow(self.master)
        self.master.wait_window(self.resgister.top)

    def login(self):
        user = self.e1.get()
        passw = self.e2.get()
        check = 0
        with open('users.txt', 'r') as f:
            for line in f:
                username, password = line.split(',')
                username = username.strip()
                password = password.strip()
                if username == user and password == passw:
                    print('yay')
                    self.n = loggedinWindow(self.master)
                    self.master.wait_window(self.n.top)
                    check = 1
        if check == 0:
            t = messagebox.Message(message="Invalid Username or Password", type=messagebox.OK)
            t.show()



root = Tk()
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", "./Forest-ttk-theme/forest-light.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-light")
m = mainWindow(root)
root.mainloop()