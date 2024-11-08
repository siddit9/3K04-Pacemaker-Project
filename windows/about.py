from tkinter import *
from tkinter import ttk
class aboutWindow(object):
    def __init__(self, master):

        #Defines the window as being dependent on the base window's existence to display, initializes style
        top = self.top=Toplevel(master)
        self.style = ttk.Style(top)
        self.style.theme_use('forest-light')

        #Initiates frame for information display
        self.about_frame = ttk.Frame(top, padding=(20, 10))
        self.about_frame.grid(row=0, column=0, padx=(0, 10), pady=(20, 0), sticky="nsew")

        #Displays McMaster University and version information in the window's title bar
        self.uni = ttk.Label(self.about_frame, text = 'McMaster University', font = (15))
        self.uni.grid(row=1, column=0, padx=5, pady=0, sticky="new")
        self.ver = ttk.Label(self.about_frame, text='Version 0.1.0', font = (15))
        self.ver.grid(row=2, column=0, padx=5, pady=0, sticky="new")
        self.serial = ttk.Label(self.about_frame, text='x', font = (15))
        self.serial.grid(row=3, column=0, padx=5, pady=0, sticky="new")

        #Cancel button to close the window when clicked
        self.b_cancel = ttk.Button(self.about_frame, text = 'Cancel', command = self.top.destroy, style="Accent.TButton")
        self.b_cancel.grid(row=4, column=0, padx=5, pady=20, sticky="new")