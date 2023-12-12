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

        largura = 600
        altura = 450

        x = self.winfo_screenwidth() // 2 - largura // 2
        y = self.winfo_screenheight() // 2 - altura // 2

        self.geometry("%dx%d+%d+%d" % (largura,altura,x,y))

        # Frame
        frmPrinc = Frame(self, width=50, padx=15, pady=10, background='#DDD')
        frmPrinc.pack(side='left', fill=BOTH, expand=True)

        # Buttons
        self.btnCriar = Button(frmPrinc, text="CRIAR", command=self.criar)
        self.btnCriar.grid(row=14, column=9, pady=15, sticky=E)

        self.btnCriar = Button(frmPrinc, text="VOLTAR", command=self.sair)
        self.btnCriar.grid(row=14, column=0, pady=15, sticky=W)
        
        # ComboBox
        self.comboBox = ttk.Combobox(frmPrinc, justify='left', state='readonly', font=("Arial", 14, font.BOLD), width=15)
        self.comboBox.grid(row=9, column=0, columnspan=10, pady= 10, sticky=W)
        self.carregaCombo()
        
        self.comboLevaTraz = ttk.Combobox(frmPrinc, justify='left', state='readonly', font=("Arial", 14, font.BOLD), width=15)
        self.comboLevaTraz.grid(row=9, column=7, columnspan=10, pady= 10, sticky=W)
        simnao = ('SIM', 'NÃO')
        self.comboLevaTraz['values'] = simnao
        self.comboLevaTraz.current(0)

        # Entrys
        self.entryProduto = Entry(frmPrinc, width=95)
        self.entryProduto.grid(row=1, column=0, columnspan=10)

        #self.entryData = Entry(frmPrinc, width=95)
        #self.entryData.grid(row=3, column=0, columnspan=10)
        self.entryData = msk.MaskedWidget(frmPrinc, 'fixed', mask='99/99/9999 99:99', width=95)
        self.entryData.grid(row=3, column=0, columnspan=10)

        #self.entryValor = Entry(frmPrinc, width=95)
        #self.entryValor.grid(row=5, column=0, columnspan=10)
        self.entryValor = msk.MaskedWidget(frmPrinc, 'numeric', dec_sep=",", tho_sep='.', symbol="R$", width=95)
        self.entryValor.grid(row=5, column=0, columnspan=10)

        # TextBox
        self.txtObs = Text(frmPrinc, width=71, height=7)
        self.txtObs.grid(row=7, column=0, columnspan=10)
        
        self.entrysObg = [self.entryProduto, self.entryData, self.entryValor]

        # Label
        Label(frmPrinc, text="PRODUTO / SERVIÇO (*)", background='#DDD').grid(row=0, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="DATA / HORA (*)", background='#DDD').grid(row=2, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="VALOR (*)", background='#DDD').grid(row=4, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="OBS", background='#DDD').grid(row=6, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="CLIENTE", background='#DDD').grid(row=8, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="LEVA E TRAZ", background='#DDD').grid(row=8, column=7, sticky=W, columnspan=10)
        

    def criar(self):
        for ins in self.entrysObg:
            if ins.get().replace("R$", "").replace(",", "").replace(".", "").replace("/", "").replace("-", "").replace("_", "").strip() == "" or ins.get() == "__/__/____ __:__":
                messagebox.showerror('', "NÃO DEIXE OS CAMPOS OBRIGATÓRIOS (*) EM BRANCO")
                return
            
        try:
            date = dt.datetime.strptime(self.entryData.get() + ":00", '%d/%m/%Y %H:%M:%S')
        except:
            messagebox.showerror('', "DATA INVÁLIDA")
            return
        
        if self.comboLevaTraz.get() == "SIM":
            leva = 1
        else:
            leva = 0
        
        insertDate = f'{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)} {str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}:{str(date.second).zfill(2)}'
        params = ((self.comboBox.get(),))
        sqlStr = '''SELECT idcliente FROM cliente WHERE nome = ?'''
        nome = db.selectSql(sqlStr, params)[0][0]
        params = (self.entryProduto.get(), insertDate, self.entryValor.get(), self.txtObs.get(1.0, END), nome, leva)
        sqlStr = '''INSERT INTO agendamentos(produtoservico, data, valor, concluido, obsAg, idcliente, pago, leva)
                    VALUES (?, ?, ?, 0, ?, ?, 0, ?)'''
        nome = db.execSql(sqlStr, params)
        messagebox.showinfo('', "CRIADO COM SUCESSO!")
        self.sair()
        
    def carregaCombo(self):
        lista = []
        res = db.selectSql('''SELECT nome FROM cliente ORDER BY nome''')
        for index, row in enumerate(res):
            lista.insert(index, row[0])
        if len(lista) > 0:
            self.comboBox['values'] = lista
            self.comboBox.current(0)

    def sair(self):
        self.parent.firstShow()
        self.destroy()
        