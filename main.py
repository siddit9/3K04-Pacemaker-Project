from tkinter import *
import sys
from tkinter import messagebox

from PIL import Image, ImageTk
class loginWindow(object):
    def __init__(self, master):
        top = self.top=Toplevel(master)
        self.user = Label(top, text = 'New Username')
        self.user.pack()
        self.user_entry = Entry(top)
        self.user_entry.pack()
        self.password = Label(top, text = 'New Password')
        self.password.pack(pady=(10,0))
        self.password_entry = Entry(top, show = '*')
        self.password_entry.pack()
        self.b_ok = Button(top, text = 'Ok', command = self.write_new)
        self.b_ok.pack(pady=10)
        self.b_cancel = Button(top, text = 'Cancel', command = self.top.destroy)
        self.b_cancel.pack()

    # Window creates new
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

#class loggedInUser(object, User):
class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.frame = Frame(master)

        self.frame.pack(expand=True)
        self.img = ImageTk.PhotoImage(Image.open('./logo1.jpg'))
        self.panel = Label(self.frame, image=self.img)
        self.panel.grid(row=0, column=0, padx=10, pady=10)
        self.username = Label(self.frame, text='Username').grid(row = 1, padx=10)
        self.e1 = Entry(self.frame)
        self.e1.grid(row = 2, padx=10)

        self.password = Label(self.frame, text='Password').grid(row = 3, padx=10, pady=(10,0))
        self.e2 = Entry(self.frame)
        self.e2.grid(row=4, padx=10)

        self.w = Button(self.frame, text='Register New', command=self.createNew)
        self.w.grid(row = 5, padx=10, pady=10)

        #self.w = Button(master, text='Login', command=self.login)
        #self.w.grid(row = 6, padx=10, pady=10)

    def createNew(self):
        self.n = loginWindow(self.master)
        self.master.wait_window(self.n.top)

    #def login(self):


root = Tk()
m = mainWindow(root)
root.mainloop()