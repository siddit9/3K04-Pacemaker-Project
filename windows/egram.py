import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from tkinter import Toplevel


class ElectrogramData:
    def __init__(self, AS, AP, AT, TN, VS, VP, PVC, Hy, Sr,
                UpSmoothing, DownSmoothing, ATRDur, ATRFB,
                ATREnd, PVP):
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




