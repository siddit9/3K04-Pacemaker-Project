from tkinter import *
from tkinter import messagebox
import os
#Window used to register new users and check the maximum number of users
class registerWindow(object):
    def __init__(self, master):

        #Defines the window as being dependent on the base window's existence to display
        top = self.top=Toplevel(master)

        #Initiates information display and input
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

    #Button function to assess capabilities to add new users
    #Writes new user password to users.txt if available
    def write_new(self):
        count = 0
        dir_path = r'./saves'
        for path in os.scandir(dir_path):
            if path.is_file():
                count += 1
        if count < 10:
            self.write()
        else:
            t = messagebox.Message(self.top, message="Maximum Users Reached", type=messagebox.OK)
            t.show()

    #Button function to write new user password to users.txt
    def write(self):

        #writes into users.txt
        with open("./saves/"+self.user_entry.get()+'.txt', 'a') as f:
            user, passw = self.user_entry.get(), self.password_entry.get()
            if len(user) > 0 and len(passw) > 0:
                f.write(user + ',' + passw + '\n')
                t = messagebox.Message(message="User Created", type=messagebox.OK)
                t.show()
                self.top.destroy()
            elif os.path.isfile("./saves/"+user+'.txt'):
                t = messagebox.Message(self.top, message="Username Already Exists", type=messagebox.OK)
                t.show()
            else:
                t = messagebox.Message(self.top, message="User/Password Invalid", type=messagebox.OK)
                t.show()
