from tkinter import *
import sys
from PIL import Image, ImageTk
class loginWindow(object):
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
        with open('users.txt', 'a') as f:
            f.write(self.user_entry.get() + ',' + self.password_entry.get() + '\n')
        self.top.destroy()

class loggedInUser(object, User):
class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.img = ImageTk.PhotoImage(Image.open('./logo1.jpg'))
        self.panel = Label(master, image=self.img)
        self.panel.pack(padx=10, pady=10)

        self.username = Label(master, text='Username').pack(side=LEFT)
        self.e1 = Entry(master)
        self.e1.pack(side=LEFT)
        self.e2 = Entry(master)
        self.e2.pack(side=RIGHT)
        self.password = Label(master, text='Password').pack(side=RIGHT)
        self.w = Button(master, text='Register New', command=self.createNew)
        self.w.pack(side=BOTTOM)
        self.w = Button(master, text='Login', command=self.login)
        self.w.pack(side=BOTTOM)

    def createNew(self):
        self.n = loginWindow(self.master)
        self.master.wait_window(self.n.top)

    def login(self):


root = Tk()
m = mainWindow(root)
root.mainloop()