import datetime as dt
import msk, db
import sqlite3 as sql
from tkinter import *
from tkinter import filedialog, messagebox, font, ttk

class Window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("NOVO AGENDAMENTO")
        self.resizable(0, 0)
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=14, weight=font.BOLD)
        self.config()
        
        self.overrideredirect(1)

        largura = 250
        altura = 80

        x = self.winfo_screenwidth() // 2 - largura // 2
        y = self.winfo_screenheight() // 2 - altura // 2

        self.geometry("%dx%d+%d+%d" % (largura,altura,x,y))

        # Frame
        frmPrinc = Frame(self, width=50, padx=15, pady=10, background='#333')
        frmPrinc.pack(side='left', fill=BOTH, expand=True)

        # Buttons
        self.btnCriar = Button(frmPrinc, text="PAGO", command=self.pago)
        self.btnCriar.grid(row=14, column=9, pady=15, sticky=E, padx=20)

        self.btnCriar = Button(frmPrinc, text="NÃO PAGO", command=self.npago)
        self.btnCriar.grid(row=14, column=0, pady=15, sticky=W)
        
    def pago(self):
        self.parent.finaliza(1)
        self.destroy()

    def npago(self):
        self.parent.finaliza(0)
        self.destroy()
        