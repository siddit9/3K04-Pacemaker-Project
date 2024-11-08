#Importing required libraries
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
from PIL import Image, ImageTk
from windows.about import aboutWindow
from windows.loggedin import loggedinWindow
from windows.register import registerWindow


#Main window used for logging in and registering new users
class mainWindow(object):
    def __init__(self, master):
        #sets itself as the master window all other windows are dependent upon
        self.master = master
        self.style = style

        #Locks the window to specified size
        self.master.geometry("600x550")
        self.master.resizable(False, False)

        #Displays the appropriate labels, buttons and entry boxes
        self.img = ImageTk.PhotoImage(Image.open('./logo1.jpg'))
        self.panel = Label(master, image=self.img)
        self.panel.pack(padx=10, pady=10)
        self.username = ttk.Label(master, text='Username').pack(side=LEFT)
        self.e1 = ttk.Entry(master)
        self.e1.pack(side=LEFT, pady = 10)
        self.e2 = ttk.Entry(master, show="*")
        self.e2.pack(side=RIGHT, pady = 10)
        self.password = ttk.Label(master, text='Password').pack(side=RIGHT)
        self.rn = ttk.Button(master, text='Register New', command=self.createNew, style="Accent.TButton")
        self.rn.pack(side=BOTTOM, pady = 10)
        self.log = ttk.Button(master, text='Login', command=self.login, style="Accent.TButton")
        self.log.pack(side=BOTTOM)
        self.about = ttk.Button(master, text='About', command=self.about, style="Accent.TButton")
        self.about.pack(side=TOP)

    #Function to open the registration window
    def createNew(self):
        self.resgister = registerWindow(self.master)
        self.master.wait_window(self.resgister.top)

    #Function to open the about window
    def about(self):
        self.about = aboutWindow(self.master)
        self.master.wait_window(self.about.top)

    #Function to login to the specified user, returns the appropriate parameter modification window
    def login(self):
        #Retieves entrybox information
        user = self.e1.get()
        passw = self.e2.get()
        check = 0

        #Checks if the user exists in the users.txt file
        with open('./saves/'+user+'.txt', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                username = row[0]
                password = row[1]

                #Returns new window for parameter modification if user password combo is found
                if username == user and password == passw:
                    print('yay')
                    self.n = loggedinWindow(self.master, user, passw)
                    self.master.wait_window(self.n.top)
                    check = 1

        #Display error message if user password combo is not found
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

