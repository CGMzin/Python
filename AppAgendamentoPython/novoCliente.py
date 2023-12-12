import sqlite3 as sql
import verificaCPFCNPJ as vcc
import msk, db
from tkinter import *
from tkinter import filedialog, messagebox, font

class Window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("NOVO CLIENTE")
        self.resizable(0, 0)
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=14, weight=font.BOLD)
        self.config()
        
        self.overrideredirect(1)

        largura = 550
        altura = 550

        x = self.winfo_screenwidth() // 2 - largura // 2
        y = self.winfo_screenheight() // 2 - altura // 2

        self.geometry("%dx%d+%d+%d" % (largura,altura,x,y))

        # Frame
        frmPrinc = Frame(self, width=50, padx=30, pady=10, background='#DDD')
        frmPrinc.pack(side='left', fill=BOTH, expand=True)

        # Buttons
        self.btnCriar = Button(frmPrinc, text="CRIAR", command=self.criar)
        self.btnCriar.grid(row=16, column=9, pady=15, sticky=E)

        self.btnCriar = Button(frmPrinc, text="VOLTAR", command=self.sair)
        self.btnCriar.grid(row=16, column=0, pady=15, sticky=W)

        # Entrys
        self.entryNome = Entry(frmPrinc, width=80)
        self.entryNome.grid(row=1, column=0, columnspan=10)
        
        #self.entryTelefone = Entry(frmPrinc, width=80)
        #self.entryTelefone.grid(row=3, column=0, columnspan=10)
        self.entryTelefone = msk.MaskedWidget(frmPrinc, 'fixed', mask='(99)99999-9999', width=80)
        self.entryTelefone.grid(row=3, column=0, columnspan=10)

        self.entryCpfCnpj = Entry(frmPrinc, width=80)
        self.entryCpfCnpj.grid(row=5, column=0, columnspan=10)

        self.entryEndereco = Entry(frmPrinc, width=80)
        self.entryEndereco.grid(row=7, column=0, columnspan=10)

        self.entryBairro = Entry(frmPrinc, width=80)
        self.entryBairro.grid(row=9, column=0, columnspan=10)

        self.entryCidade = Entry(frmPrinc, width=80)
        self.entryCidade.grid(row=11, column=0, columnspan=10)

        self.entryEstado = Entry(frmPrinc, width=80)
        self.entryEstado.grid(row=13, column=0, columnspan=10)

        # TextBox
        self.txtObs = Text(frmPrinc, width=60, height=7)
        self.txtObs.grid(row=15, column=0, columnspan=10)
        
        self.listaInputs = [self.entryNome, self.entryTelefone, self.entryCpfCnpj, self.entryEndereco, self.entryBairro, self.entryCidade, self.entryEstado, self.txtObs]

        # Label
        Label(frmPrinc, text="NOME(*)", background='#DDD').grid(row=0, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="TELEFONE(*)", background='#DDD').grid(row=2, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="CPF/CNPJ", background='#DDD').grid(row=4, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="ENDEREÇO", background='#DDD').grid(row=6, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="BAIRRO", background='#DDD').grid(row=8, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="CIDADE", background='#DDD').grid(row=10, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="ESTADO", background='#DDD').grid(row=12, column=0, sticky=W, columnspan=10)
        Label(frmPrinc, text="OBS", background='#DDD').grid(row=14, column=0, sticky=W, columnspan=10)    

    def criar(self):
        tel = self.entryTelefone.get().replace('(', '').replace(')', '').replace('-', '').replace('_', '')
        for ins in self.listaInputs[:2]:
            if ins.get() == "":
                messagebox.showerror('', "NÃO DEIXE OS CAMPOS OBRIGATÓRIOS (*) EM BRANCO")
                return
        if len(tel) < 8:
            messagebox.showerror('', "TELEFONE INVÁLIDO, O NÚMERO NÃO PODE TER MENOS DE 8 DÍGITOS")            
            return
        if len(tel) < 9:
            if not messagebox.askyesno('', 'O TELEFONE INSERIDO É FIXO?'):
                messagebox.showerror('', "TELEFONE INVÁLIDO, O NÚMERO NÃO PODE TER MENOS DE 9 DÍGITOS")            
            return
        if len(tel) > 11:
            messagebox.showerror('', "TELEFONE INVÁLIDO, DEVE TER O FORMATO: \n(00)00000-0000")            
            return
        try:
            telteste = int(tel)
        except:
            messagebox.showerror('', "TELEFONE INVÁLIDO, DEVE CONTER APENAS NÚMEROS E \nDEVE TER O FORMATO: (00)00000-0000")            
            return
        if self.entryCpfCnpj.get() != "":
            if len(self.entryCpfCnpj.get()) == 11:
                cpfcnpj = vcc.validar_cpf(self.entryCpfCnpj.get())
            else:
                cpfcnpj = vcc.validar_cnpj(self.entryCpfCnpj.get())
            if not cpfcnpj:
                messagebox.showerror('', "CPF/CNPJ INVÁLIDO")            
                return
        else:
            cpfcnpj = ""
            
        sqlStr = f'SELECT nome FROM cliente ORDER BY nome'
        res = db.selectSql(sqlStr)
        if len(res) > 0:
            for nome in res:
                if nome[0].lower() == self.entryNome.get().lower():
                    messagebox.showerror('', "JÁ EXISTE UM CLIENTE COM ESSE NOME")            
                    return
            
        params = (self.entryNome.get(), self.entryTelefone.get().replace('(', '').replace(')', '').replace('-', ''), cpfcnpj, self.entryEndereco.get(), self.entryBairro.get(), self.entryCidade.get(), self.entryEstado.get(), self.txtObs.get(1.0, END))
        strSql = '''INSERT INTO cliente(nome, telefone, cpfcnpj, endereco, bairro, cidade, estado, obs) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
        db.execSql(strSql, params)
        messagebox.showinfo('', "CRIADO COM SUCESSO!")
        self.sair()

    def sair(self):
        self.parent.verClientes()
        self.destroy()