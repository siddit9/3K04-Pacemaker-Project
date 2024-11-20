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
        root = self.main_frame = Toplevel(master)
        self.style = ttk.Style(root)
        self.style.theme_use('forest-light')



        self.container = ttk.Frame(root)
        self.canvas = Canvas(self.container, height = 600, width = 1000)
        self.scrollbar = Scrollbar(self.container,  orient="vertical", command=self.canvas.yview)
        self.scrollbarh = Scrollbar(self.container, orient="horizontal", command=self.canvas.xview)
        top = self.top = ttk.Frame(self.canvas)
        top.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        self.canvas.create_window((0, 0), window=self.top, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set, xscrollcommand=self.scrollbarh.set)
        """
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.top = top = ttk.Frame(main_frame)
        self.top.pack(side=LEFT, fill=BOTH, expand=1)
        self.scrollbar.config(command=top.yview)
        """
        #top.configure(yscrollcommand=self.scrollbar.set)
        #top.bind(
           # '<Configure>', lambda e: top.configure(scrollregion=top.bbox("all"))
        #)



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
        self.new_patient_button = ttk.Button(self.id_frame, text="New Patient", command = root.destroy, style="Accent.TButton")
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
        self.report_frame.grid(row=0, column=1, padx=(0, 10), pady=(20, 0), sticky="nsew")
        self.report_button = ttk.Button(self.report_frame, text="Generate Report", style="Accent.TButton",
                                        command=lambda: self.generateReport())
        self.report_button.grid(row=0, column=0, padx=(70, 10), sticky="nsew")
        self.egram_view = ttk.Button(self.report_frame, text="View Egram", style="Accent.TButton",
                                        command=lambda: self.generateReport())
        self.egram_view.grid(row=2, column=0, padx=(70,10), pady=(10,10), sticky="nsew")

###############################################################################################################################################
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

        self.Hysteresis_limit_label = ttk.Label(self.HR_frame, text="Hysteresis Rate Limit(ppm)")
        self.Hysteresis_limit_label.grid(row=7, column=0, padx=5, pady=10, sticky="ew")
        self.default_HL = StringVar(top)
        self.default_HL.set("60")
        self.HL_inc = 0
        self.HL_spinbox = ttk.Spinbox(self.HR_frame, from_=30, to=175, textvariable=self.default_HL,
                                       command=self.calc_HL_inc, increment=self.HL_inc)
        self.HL_spinbox.grid(row=8, column=0, padx=5, pady=10, sticky="ew")

####################################################################################################################################################
        #Frame and spinboxes for rate adaptive pacing
        self.RAP_frame = ttk.LabelFrame(top, text="Rate Adaptive Pacing", padding=(20, 30))
        self.RAP_frame.grid(row=1, column=1, padx=(20, 10), pady=(10, 20), sticky="nsew")
        self.MSR_label = ttk.Label(self.RAP_frame, text="Maximum Sensor Rate(ppm)")
        self.MSR_label.grid(row=1, column=0, padx=5, pady=10, sticky="ew")
        self.default_MSR = StringVar(top)
        self.default_MSR.set("120")
        self.MSR_spinbox = ttk.Spinbox(self.RAP_frame, from_=50, to=175, textvariable=self.default_MSR, increment=5)
        self.MSR_spinbox.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        self.Activitythreshold_label = ttk.Label(self.RAP_frame, text="Activity Threshold")
        self.Activitythreshold_label.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.default_Activitythreshold = StringVar(top)
        self.default_Activitythreshold.set("Med")
        self.Activitythreshold_combobox = ttk.Combobox(self.RAP_frame, values = ["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"], state = "readonly", style="Accent.TCombobox", textvariable = self.default_Activitythreshold)
        self.Activitythreshold_combobox.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        self.Responsefactor_label = ttk.Label(self.RAP_frame, text="Response Factor")
        self.Responsefactor_label.grid(row=5, column=0, padx=5, pady=10, sticky="ew")
        self.default_Responsefactor = StringVar(top)
        self.default_Responsefactor.set("8")
        self.Responsefactor_spinbox = ttk.Spinbox(self.RAP_frame, from_=1, to=16, textvariable=self.default_Responsefactor, increment=1)
        self.Responsefactor_spinbox.grid(row=6, column=0, padx=5, pady=10, sticky="ew")

        self.Reactiontime_label = ttk.Label(self.RAP_frame, text="Reaction Time(sec)")
        self.Reactiontime_label.grid(row=7, column=0, padx=5, pady=10, sticky="ew")
        self.default_Reactiontime = StringVar(top)
        self.default_Reactiontime.set("30")
        self.Reactiontime_spinbox = ttk.Spinbox(self.RAP_frame, from_=10, to=50,
                                                  textvariable=self.default_Reactiontime, increment=10)
        self.Reactiontime_spinbox.grid(row=8, column=0, padx=5, pady=10, sticky="ew")

        self.Recoverytime_label = ttk.Label(self.RAP_frame, text="Recovery Time(Min)")
        self.Recoverytime_label.grid(row=9, column=0, padx=5, pady=10, sticky="ew")
        self.default_Recoverytime = StringVar(top)
        self.default_Recoverytime.set("5")
        self.Recoverytime_spinbox = ttk.Spinbox(self.RAP_frame, from_=2, to=16,
                                                  textvariable=self.default_Recoverytime, increment=1)
        self.Recoverytime_spinbox.grid(row=10, column=0, padx=5, pady=10, sticky="ew")

#####################################################################################################################################################
        #Frame and spinboxes for altering articular-ventricular general parameters
        self.AV_frame = ttk.LabelFrame(top, text="Artial-Ventricular Delay", padding=(20, 30))
        self.AV_frame.grid(row=1, column=2, padx=(20, 10), pady=(10, 20), sticky="nsew")

        self.FixedAVdelay_label = ttk.Label(self.AV_frame, text="Fixed AV Delay(ms)")
        self.FixedAVdelay_label.grid(row=0, column=0, padx=5, pady=10, sticky="ew")
        self.default_FixedAVdelay = StringVar(top)
        self.default_FixedAVdelay.set("150")
        self.FixedAVdelay_spinbox = ttk.Spinbox(self.AV_frame, from_=70, to=300, textvariable=self.default_FixedAVdelay,
                                                   increment=10)
        self.FixedAVdelay_spinbox.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        self.DynamicAVDelay_label = ttk.Label(self.AV_frame, text="Dynamic AV Delay")
        self.DynamicAVDelay_label.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
        self.default_DynamicAVDelay = StringVar(top)
        self.default_DynamicAVDelay.set("OFF")
        self.DynamicAVDelay_combobox = ttk.Combobox(self.AV_frame, state = "readonly", values = ["ON", "OFF"], style="Accent.TCombobox", textvariable=self.default_DynamicAVDelay)
        self.DynamicAVDelay_combobox.grid(row=4, column=0, padx=5, pady=10, sticky="ew")

        self.MinDynamicAVdelay_label = ttk.Label(self.AV_frame, text="Minimum Dynamic AV Delay(ms)")
        self.MinDynamicAVdelay_label.grid(row=5, column=0, padx=5, pady=10, sticky="ew")
        self.default_MinDynamicAVdelay = StringVar(top)
        self.default_MinDynamicAVdelay.set("50")
        self.MinDynamicAVdelay_spinbox = ttk.Spinbox(self.AV_frame, from_=30, to=100,
                                                            textvariable=self.default_MinDynamicAVdelay,
                                                            increment=10)
        self.MinDynamicAVdelay_spinbox.grid(row=6, column=0, padx=5, pady=10, sticky="ew")

        self.SensedAVdelayOffset_label = ttk.Label(self.AV_frame, text="Sensed Dynamic AV Delay Offset(ms)")
        self.SensedAVdelayOffset_label.grid(row=7, column=0, padx=5, pady=10, sticky="ew")
        self.default_SensedAVdelayOffset = StringVar(top)
        self.default_SensedAVdelayOffset.set("0")
        self.SensedAVdelayOffset_inc = 0
        self.SensedAVdelayOffset_spinbox = ttk.Spinbox(self.AV_frame, from_=-100, to=0, textvariable=self.default_SensedAVdelayOffset,
                                                     increment=10)
        self.SensedAVdelayOffset_spinbox.grid(row=8, column=0, padx=5, pady=10, sticky="ew")

############################################################################################################################################################
        #Frame and spinboxes for altering atrial pacing parameters
        #Parameters with differening step increments have their own on-use functions for increment control
        self.Artial_frame = ttk.LabelFrame(top, text="Artial Paramters", padding=(20, 30))
        self.Artial_frame.grid(row=2, column=1, padx=(20, 10), pady=(10, 20), sticky="nsew")

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

##########################################################################################################################################################
        #Frame and spinboxes for altering ventricular parameters
        #Parameters with differening step increments have their own on-use functions for increment control
        self.Ventricular_frame = ttk.LabelFrame(top, text="Ventricular Paramters", padding=(20, 30))
        self.Ventricular_frame.grid(row=2, column=2, padx=(20, 10), pady=(10, 20), sticky="nsew")

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

    # Pack the frames and spinboxes in the main window
        self.scrollbar.pack(side="left", fill="both")
        self.scrollbarh.pack(side="top", fill="both")
        self.container.pack(side = "top", fill = "both")
        self.canvas.pack(side="left", fill="both", expand=True)

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

    def calc_HL_inc(self):
        val = int(self.HL_spinbox.get())
        if val >= 30 and val < 50:
            self.HL_inc = 5
        elif val >= 50 and val < 90:
            self.HL_inc = 1
        elif val >= 90 and val < 175:
            self.HL_inc = 5
        self.HL_spinbox.config(increment=self.HL_inc)
        return