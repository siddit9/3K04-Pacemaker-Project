from tkinter import *
import sys
from tkinter import messagebox
from tkinter import ttk
import csv
from datetime import datetime
from PIL import Image, ImageTk


class aboutWindow(object):
    def __init__(self, master):
        top = self.top=Toplevel(master)
        self.style = ttk.Style(top)
        self.style.theme_use('forest-light')
        self.about_frame = ttk.Frame(top, padding=(20, 10))
        self.about_frame.grid(row=0, column=0, padx=(0, 10), pady=(20, 0), sticky="nsew")
        self.uni = ttk.Label(self.about_frame, text = 'McMaster University', font = (15))
        self.uni.grid(row=1, column=0, padx=5, pady=0, sticky="new")
        self.ver = ttk.Label(self.about_frame, text='Version 0.1.0', font = (15))
        self.ver.grid(row=2, column=0, padx=5, pady=0, sticky="new")
        self.serial = ttk.Label(self.about_frame, text='x', font = (15))
        self.serial.grid(row=3, column=0, padx=5, pady=0, sticky="new")
        self.b_cancel = ttk.Button(self.about_frame, text = 'Cancel', command = self.top.destroy, style="Accent.TButton")
        self.b_cancel.grid(row=4, column=0, padx=5, pady=20, sticky="new")

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
    def __init__(self, master, user, password):
        self.username = user
        self.password = password
        top = self.top = Toplevel(master)
        self.top.geometry("1000x600")
        self.style = ttk.Style(top)
        self.style.theme_use('forest-light')
        self.widgets_frame = ttk.Frame(top, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
        self.widgets_frame.columnconfigure(index=0, weight=1)

        self.pacemaker_id = "pc_102"
        self.id_frame = ttk.Frame(top, padding=(20, 10))
        self.id_frame.grid(row=0, column=0, padx=(0, 10), pady=(20, 0), sticky="nsew")
        self.ID_label = ttk.Label(self.id_frame, text=self.pacemaker_id, font = (25))
        self.ID_label.grid(row=1, column=0, padx=5, pady=10, sticky="new")
        self.patient_label = ttk.Label(self.id_frame, text="Patient: " + self.username, font = (25))
        self.patient_label.grid(row=2, column=0, padx=5, pady=0, sticky="new")
        self.new_patient_button = ttk.Button(self.id_frame, text="New Patient", command = self.top.destroy, style="Accent.TButton")
        self.new_patient_button.grid(row=2, column=4, padx=20, pady=0, sticky="new")
        self.save_button = ttk.Button(self.id_frame, text="Save", command=lambda: self.saveData(), style="Accent.TButton")
        self.save_button.grid(row=1, column=4, padx=20, pady=10, sticky="ew")

        self.pacing_modes_frame = ttk.Frame(top)
        self.pacing_modes_frame.grid(row = 0, column = 2)
        self.pacing_mode_label = ttk.Label(self.pacing_modes_frame, text="Select Pacing Mode:", font=(25))
        self.pacing_mode_label.grid(row=0, column=0, padx=5, pady=0)
        self.pacing_modes = ttk.Combobox(self.pacing_modes_frame, values=['AOO', 'VOO', 'AAI', 'VVI'], state='readonly', style="Accent.TCombobox")
        self.pacing_modes.set('AOO')
        self.pacing_modes.grid(row=1, column=0, padx=5, pady=0)

        self.report_button = ttk.Button(top, text="Generate Report", style="Accent.TButton", command=lambda:self.generateReport())
        self.report_button.grid(row=2, column=0)

        self.HR_frame = ttk.LabelFrame(top, text="Heart Rate Control", padding=(20, 30))
        self.HR_frame.grid(row=1, column=0, padx=(20, 10), pady=(10, 20), sticky="nsew")

        self.LHR_label = ttk.Label(self.HR_frame, text="Lower Heart Rate(ppm)")
        self.LHR_label.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        self.default_LHR = StringVar(top)
        self.default_LHR.set("60")
        self.LHR_inc = 0
        self.LHR_spinbox = ttk.Spinbox(self.HR_frame, from_=30, to=175, textvariable=self.default_LHR, command = self.calc_LHR_inc, increment= self.LHR_inc)
        self.LHR_spinbox.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        self.UHR_label = ttk.Label(self.HR_frame, text="Upper Heart Rate(ppm)")
        self.UHR_label.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.default_UHR = StringVar(top)
        self.default_UHR.set("120")
        self.UHR_spinbox = ttk.Spinbox(self.HR_frame, from_=50, to=175, textvariable=self.default_UHR, increment=5)
        self.UHR_spinbox.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        self.MSR_label = ttk.Label(self.HR_frame, text="Maximum Sensor Rate(ppm)")
        self.MSR_label.grid(row=5, column=0, padx=5, pady=10, sticky="ew")
        self.default_MSR = StringVar(top)
        self.default_MSR.set("120")
        self.MSR_spinbox = ttk.Spinbox(self.HR_frame, from_=50, to=175, textvariable=self.default_MSR, increment=5)
        self.MSR_spinbox.grid(row=6, column=0, padx=5, pady=10, sticky="ew")

        self.Artial_frame = ttk.LabelFrame(top, text="Artial Paramters", padding=(20, 30))
        self.Artial_frame.grid(row=1, column=2, padx=(20, 10), pady=(10, 20), sticky="nsew")

        self.Artial_Pulse_Amp_label = ttk.Label(self.Artial_frame, text="Artial Pulse Amplitude(V)")
        self.Artial_Pulse_Amp_label.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.default_APA = StringVar(top)
        self.default_APA.set("3.5")
        self.APA_inc = 0
        self.Artial_Pulse_Amp_spinbox = ttk.Spinbox(self.Artial_frame, from_=0, to=7, textvariable=self.default_APA, command = self.calc_APA_inc, increment=self.APA_inc)
        self.Artial_Pulse_Amp_spinbox.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        self.Artial_Pulse_Width_label = ttk.Label(self.Artial_frame, text="Artial Pulse Width(ms)")
        self.Artial_Pulse_Width_label.grid(row=5, column=0, padx=5, pady=10, sticky="ew")
        self.default_APW = StringVar(top)
        self.default_APW.set("0.4")
        self.APW_inc = 0
        self.Artial_Pulse_Width_spinbox = ttk.Spinbox(self.Artial_frame, from_=0.05, to=1.9, textvariable=self.default_APW,
                                                    command=self.calc_APW_inc, increment=self.APW_inc, format = "%.2f")
        self.Artial_Pulse_Width_spinbox.grid(row=6, column=0, padx=5, pady=10, sticky="ew")

        self.Artial_Refractory_Period_label = ttk.Label(self.Artial_frame, text="Artial Refractory Period(ms)")
        self.Artial_Refractory_Period_label.grid(row=7, column=0, padx=5, pady=10, sticky="ew")
        self.default_ARP = StringVar(top)
        self.default_ARP.set("250")
        self.ARP_inc = 10
        self.Artial_Refractory_Period_spinbox = ttk.Spinbox(self.Artial_frame, from_=150, to=500,
                                                      textvariable=self.default_ARP,
                                                       increment=self.ARP_inc)
        self.Artial_Refractory_Period_spinbox.grid(row=8, column=0, padx=5, pady=10, sticky="ew")



        self.Ventricular_frame = ttk.LabelFrame(top, text="Ventricular Paramters", padding=(20, 30))
        self.Ventricular_frame.grid(row=1, column=3, padx=(20, 10), pady=(10, 20), sticky="nsew")

        self.Ventricular_Pulse_Amp_label = ttk.Label(self.Ventricular_frame, text="Ventricular Pulse Amplitude(V)")
        self.Ventricular_Pulse_Amp_label.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.default_VPA = StringVar(top)
        self.default_VPA.set("3.5")
        self.VPA_inc = 0
        self.Ventricular_Pulse_Amp_spinbox = ttk.Spinbox(self.Ventricular_frame, from_=0, to=7, textvariable=self.default_VPA,
                                                    command=self.calc_VPA_inc, increment=self.VPA_inc)
        self.Ventricular_Pulse_Amp_spinbox.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        self.Ventricular_Pulse_Width_label = ttk.Label(self.Ventricular_frame, text="Ventricular Pulse Width(ms)")
        self.Ventricular_Pulse_Width_label.grid(row=5, column=0, padx=5, pady=10, sticky="ew")
        self.default_VPW = StringVar(top)
        self.default_VPW.set("0.4")
        self.VPW_inc = 0
        self.Ventricular_Pulse_Width_spinbox = ttk.Spinbox(self.Ventricular_frame, from_=0.05, to=1.9,
                                                      textvariable=self.default_VPW,
                                                      command=self.calc_VPW_inc, increment=self.VPW_inc, format="%.2f")
        self.Ventricular_Pulse_Width_spinbox.grid(row=6, column=0, padx=5, pady=10, sticky="ew")

        self.Ventricular_Refractory_Period_label = ttk.Label(self.Ventricular_frame, text="Ventricular Refractory Period(ms)")
        self.Ventricular_Refractory_Period_label.grid(row=7, column=0, padx=5, pady=10, sticky="ew")
        self.default_VRP = StringVar(top)
        self.default_VRP.set("320")
        self.VRP_inc = 10
        self.Ventricular_Refractory_Period_spinbox = ttk.Spinbox(self.Ventricular_frame, from_=150, to=500,
                                       textvariable=self.default_VRP,
                                       increment=self.VRP_inc)
        self.Ventricular_Refractory_Period_spinbox.grid(row=8, column=0, padx=5, pady=10, sticky="ew")
        self.pacing_conv = {'AOO': 1, 'VOO': 2, 'AAI' : 3, 'VVI' : 4}

    def saveData(self):
        # Specify the name to search for and the data to append
        name_to_find = self.username
        data_to_append = [self.pacing_conv[self.pacing_modes.get()], self.LHR_spinbox.get(), self.UHR_spinbox.get(),
                          self.MSR_spinbox.get(), self.Artial_Pulse_Amp_spinbox.get(), self.Artial_Pulse_Width_spinbox.get(),
                          self.Artial_Refractory_Period_spinbox.get(), self.Ventricular_Pulse_Amp_spinbox.get(),
                          self.Ventricular_Pulse_Width_spinbox.get(), self.Ventricular_Refractory_Period_spinbox.get()]
        filename = 'users.txt'

        # Read the existing data and modify it
        rows = []
        with open(filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 3 and row[0] == name_to_find:  # Check if the first item matches the specific name
                    row.extend(data_to_append)  # add the data
                elif len(row) >= 3 and row[0] == name_to_find:
                    row[2:] = data_to_append  # Replace columns 3 onward with new data
                rows.append(row)

        # Write the updated data back to the CSV file
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    def generateReport(self):
        self.saveData()
        reportWindow = Toplevel()
        reportWindow.title("Report")
        reportWindow.geometry("500x500")
        # Get the current date and time
        current_datetime = datetime.now()
        header_info = ttk.Label(reportWindow, text="McMaster University\n" + current_datetime.strftime("%Y-%m-%d %H:%M") +
                                "\nModel:\nSerial Number:\nDCM Version 1.5\nBradycardia Parameters Report",
                                font=("Helvetica", 15))
        header_info.grid(row=0, column=0)

    def exit(self):
        self.top.destroy()
        sys.exit()

    def calc_APA_inc(self):
        val = float(self.Artial_Pulse_Amp_spinbox.get())
        if val >= 0 and val < 0.5:
            self.APA_inc = 0.5
        elif val >= 0.5 and val < 3.5:
            self.APA_inc = 0.1
        elif val >= 3.5 and val < 7:
            self.APA_inc = 0.5
        self.Artial_Pulse_Amp_spinbox.config(increment=self.APA_inc)
        return

    def calc_VPA_inc(self):
        val = float(self.Ventricular_Pulse_Amp_spinbox.get())
        if val >= 0 and val < 0.5:
            self.VPA_inc = 0.5
        elif val >= 0.5 and val < 3.5:
            self.VPA_inc = 0.1
        elif val >= 3.5 and val < 7:
            self.VPA_inc = 0.5
        self.Ventricular_Pulse_Amp_spinbox.config(increment=self.VPA_inc)
        return

    def calc_APW_inc(self):
        val = float(self.Artial_Pulse_Width_spinbox.get())
        if val >= 0.05 and val < 0.1:
            self.APW_inc = 0.05
        elif val >= 0.1 and val < 1.9:
            self.APW_inc = 0.1
        self.Artial_Pulse_Width_spinbox.config(increment=self.APW_inc)
        return

    def calc_VPW_inc(self):
        val = float(self.Ventricular_Pulse_Width_spinbox.get())
        if val >= 0.05 and val < 0.1:
            self.VPW_inc = 0.05
        elif val >= 0.1 and val < 1.9:
            self.VPW_inc = 0.1
        self.Ventricular_Pulse_Width_spinbox.config(increment=self.VPW_inc)
        return

    def calc_LHR_inc(self):
        val = int(self.LHR_spinbox.get())
        if val >= 30 and val < 50:
            self.LHR_inc = 5
        elif val >= 50 and val < 90:
            self.LHR_inc = 1
        elif val >= 90 and val < 175:
            self.LHR_inc = 5
        self.LHR_spinbox.config(increment=self.LHR_inc)
        return

class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.style = style
        self.master.geometry("600x550")
        self.master.resizable(False, False)
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
    def createNew(self):
        self.resgister = registerWindow(self.master)
        self.master.wait_window(self.resgister.top)

    def about(self):
        self.about = aboutWindow(self.master)
        self.master.wait_window(self.about.top)
    def login(self):
        user = self.e1.get()
        passw = self.e2.get()
        check = 0
        with open('users.txt', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                username = row[0]
                password = row[1]
                #username, password = line.split(',')
                #username = username.strip()
                #password = password.strip()
                if username == user and password == passw:
                    print('yay')
                    self.n = loggedinWindow(self.master, user, passw)
                    self.master.wait_window(self.n.top)
                    check = 1
        if check == 0:
            t = messagebox.Message(message="Invalid Username or Password", type=messagebox.OK)
            t.show()
class ElectrogramData:
    def __int__(self, timestamp, AS, AP, AT, TN, VS, VP, PVC, Hy, Sr,
                UpSmoothing, DownSmoothing, ATRDur, ATRFB,
                ATREnd, PVP):
        self.timestamp = timestamp;
        self.AS = AS
        self.AP = AP
        self.AT = AT
        self.TN = TN
        self.VS = VS
        self.VP = VP
        self. PVC = PVC
        self.Hy = Hy
        self.Sr = Sr
        self.UpSmoothing = UpSmoothing
        self.DownSmoothing = DownSmoothing
        self.ATRDur = ATRDur
        self.ATRFB = ATRFB
        self.ATREnd = ATREnd
        self.PVP = PVP


root = Tk()
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", "./Forest-ttk-theme/forest-light.tcl")

# Set the theme with the theme_use method
style.theme_use("forest-light")
m = mainWindow(root)
root.mainloop()

