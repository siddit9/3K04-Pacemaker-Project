from tkinter import *
from tkinter import ttk
from datetime import datetime
import sys
import csv

class loggedinWindow(object):
    def __init__(self, master, user, password):

        #Initiates window parameters
        self.username = user
        self.password = password
        self.pacing_ints = {"AOO": 1, "VOO": 2, "AAI": 3, "VVI": 4}
        main_frame = self.main_frame = Toplevel(master)
        self.main_frame.geometry("960x600")
        self.style = ttk.Style(main_frame)
        self.style.theme_use('forest-light')
        self.top = top = Canvas(main_frame)
        self.top.pack(side=LEFT, fill=BOTH, expand=1)
        my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=top.yview)
        my_scrollbar.pack(side=RIGHT, fill=Y)
        top.configure(yscrollcommand=my_scrollbar.set)
        top.bind(
            '<Configure>', lambda e: top.configure(scrollregion=top.bbox("all"))
        )
        self.widgets_frame = ttk.Frame(top, padding=(0, 0, 0, 10))
        self.widgets_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
        self.widgets_frame.columnconfigure(index=0, weight=1)
        #Displays the pacemaker ID and patient information as well as saving and new patient switching buttons
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
        self.pacing_modes = ttk.Combobox(self.pacing_modes_frame, values=['AAT','VVT', 'AOO', 'AAI', 'VOO', 'VVI', 'VDD', 'DOO', 'DDI', 'DDD'
                                                                          , 'AOOR', 'AAIR', 'VOOR', 'VVIR', 'VDDR', 'DOOR', 'DDIR', 'DDDR'], state='readonly', style="Accent.TCombobox")
        self.pacing_modes.set('AOO')
        self.pacing_modes.grid(row=1, column=0, padx=5, pady=0)

        self.report_frame = ttk.Frame(top, padding=(20, 10))
        self.report_frame.grid(row=0, column=3, padx=(0, 10), pady=(20, 0), sticky="nsew")
        self.report_button = ttk.Button(self.report_frame, text="Generate Report", style="Accent.TButton",
                                        command=lambda: self.generateReport())
        self.report_button.grid(row=0, column=0, padx=(70, 10), sticky="nsew")
        self.egram_view = ttk.Button(self.report_frame, text="View Egram", style="Accent.TButton",
                                        command=lambda: self.generateReport())
        self.egram_view.grid(row=2, column=0, padx=(70,10), pady=(10,10), sticky="nsew")

        #Frames and spinboxes for altering heartbeat parameters
        #parameters with differening step increments have their own on-use functions for increment control
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


        #Frame and spinboxes for rate adaptive pacing
        self.RAP_frame = ttk.LabelFrame(top, text="Rate Adaptive Pacing", padding=(20, 30))
        self.RAP_frame.grid(row=1, column=0, padx=(20, 10), pady=(10, 20), sticky="nsew")
        self.MSR_label = ttk.Label(self.RAP_frame, text="Maximum Sensor Rate(ppm)")
        self.MSR_label.grid(row=5, column=0, padx=5, pady=10, sticky="ew")
        self.default_MSR = StringVar(top)
        self.default_MSR.set("120")
        self.MSR_spinbox = ttk.Spinbox(self.HR_frame, from_=50, to=175, textvariable=self.default_MSR, increment=5)
        self.MSR_spinbox.grid(row=6, column=0, padx=5, pady=10, sticky="ew")
        self.LHR_label = ttk.Label(self.RAP_frame, text="Lower Heart Rate(ppm)")
        self.LHR_label.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        self.default_LHR = StringVar(top)
        self.default_LHR.set("60")
        self.LHR_inc = 0
        self.LHR_spinbox = ttk.Spinbox(self.HR_frame, from_=30, to=175, textvariable=self.default_LHR,
                                       command=self.calc_LHR_inc, increment=self.LHR_inc)
        self.LHR_spinbox.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        self.UHR_label = ttk.Label(self.HR_frame, text="Upper Heart Rate(ppm)")
        self.UHR_label.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.default_UHR = StringVar(top)
        self.default_UHR.set("120")
        self.UHR_spinbox = ttk.Spinbox(self.HR_frame, from_=50, to=175, textvariable=self.default_UHR, increment=5)
        self.UHR_spinbox.grid(row=4, column=0, padx=5, pady=10, sticky="ew")


        #Frame and spinboxes for altering atrial pacing parameters
        #Parameters with differening step increments have their own on-use functions for increment control
        self.Artial_frame = ttk.LabelFrame(top, text="Artial Paramters", padding=(20, 30))
        self.Artial_frame.grid(row=2, column=2, padx=(20, 10), pady=(10, 20), sticky="nsew")

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

        #Frame and spinboxes for altering ventricular parameters
        # parameters with differening step increments have their own on-use functions for increment control
        self.Ventricular_frame = ttk.LabelFrame(top, text="Ventricular Paramters", padding=(20, 30))
        self.Ventricular_frame.grid(row=2, column=3, padx=(20, 10), pady=(10, 20), sticky="nsew")

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

    def saveData(self):
        # Specify the name to search for and the data to append
        name_to_find = self.username
        data_to_append = [self.pacing_ints[self.pacing_modes.get()], self.LHR_spinbox.get(), self.UHR_spinbox.get(),
                          self.MSR_spinbox.get(), self.Artial_Pulse_Amp_spinbox.get(), self.Artial_Pulse_Width_spinbox.get(),
                          self.Artial_Refractory_Period_spinbox.get(), self.Ventricular_Pulse_Amp_spinbox.get(),
                          self.Ventricular_Pulse_Width_spinbox.get(), self.Ventricular_Refractory_Period_spinbox.get()]
        filename = './saves/'+self.username+'.txt'

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

    # Function to generate a report of the user's data'
    def generateReport(self):
        self.saveData()
        reportWindow = Toplevel()
        reportWindow.title("Report")
        reportWindow.geometry("500x500")
        # Get the current date and time
        current_datetime = datetime.now()
        header_info = ttk.Label(reportWindow,
                                text="McMaster University\n" + current_datetime.strftime("%Y-%m-%d %H:%M") +
                                     "\nModel:\nSerial Number:\nDCM Version 1.5\nBradycardia Parameters Report",
                                font=("Helvetica", 15))
        header_info.grid(row=0, column=0, padx=10, pady=5)

        print_button = ttk.Button(reportWindow, text="Print as PDF", style="Accent.TButton")
        print_button.grid(row=0, column=2, sticky="ne", padx=10, pady=5)

    #Exits window by deleting the current window
    def exit(self):
        self.top.destroy()
        sys.exit()


    #Various calculation functions to calculate the increment amount for the various parameters
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