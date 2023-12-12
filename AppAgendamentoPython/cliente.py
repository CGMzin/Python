import verificaCPFCNPJ as vcc
import sqlite3 as sql
import db
from tkinter import *
from tkinter import filedialog, messagebox, font

class Window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("AGENDAMENTOS/CLIENTES")
        self.resizable(0, 0)
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=14, weight=font.BOLD)
        self.config()

        self.actID = -1
        self.selected = 0

        self.overrideredirect(1)

        largura = 800
        altura = 590

        x = self.winfo_screenwidth() // 2 - largura // 2
        y = self.winfo_screenheight() // 2 - altura // 2

        self.geometry("%dx%d+%d+%d" % (largura,altura,x,y))

        # Frame
        frmTop = Frame(self, background='grey', padx=15, pady=10, height=25)
        frmTop.pack(side='top', fill=BOTH)
        
        frmPrinc = Frame(self, width=50, background='#999')
        frmPrinc.pack(side='left', fill=Y)

        frmDir = Frame(self, background='#DDD', padx=10, pady=10)
        frmDir.pack(side='right', fill=BOTH, expand=True)

        # Buttons
        btnCriar = Button(frmDir, text="CRIAR", command=self.novoCliente)
        btnCriar.grid(row=16, column=0, pady=10, padx=5, sticky=W)

        btnSalvar = Button(frmDir, text="SALVAR", command=self.salvarCliente)
        btnSalvar.grid(row=16, column=1, pady=10, padx=5, sticky=W)

        btnExcluir = Button(frmDir, text="EXCLUIR", command=self.excluirCliente)
        btnExcluir.grid(row=16, column=2, pady=10, padx=5, sticky=W)
        
        btnAgend = Button(frmDir, text="AGENDAMENTOS", command=self.verAgend)
        btnAgend.grid(row=16, column=3, pady=10, padx=5, sticky=W)

        btnSair = Button(frmDir, text="VOLTAR", command=self.sair)
        btnSair.grid(row=16, column=4, pady=10, padx=5, sticky=W)

        #Scroll
        scroll = Scrollbar(frmPrinc)
        scroll.grid(row=1, column=1, sticky=NS)

        # List
        self.listaClientes = Listbox(frmPrinc, yscrollcommand=scroll.set, width=15, height=22)
        self.listaClientes.grid(row=1, column=0)
        scroll.config(command=self.listaClientes.yview)
        self.listaClientes.bind('<<ListboxSelect>>', self.onselect)
        self.carregaLista()

        # Entrys
        self.entryPesquisa = Entry(frmTop, width=60)
        self.entryPesquisa.grid(row=0, column=1, columnspan=5)
        self.entryPesquisa.bind("<Any-KeyRelease>", self.pesquisa)
        
        self.entryNome = Entry(frmDir, width=95, state='disabled')
        self.entryNome.grid(row=1, column=0, columnspan=10)
        
        self.entryTelefone = Entry(frmDir, width=95, state='disabled')
        self.entryTelefone.grid(row=3, column=0, columnspan=10)

        self.entryCpfCnpj = Entry(frmDir, width=95, state='disabled')
        self.entryCpfCnpj.grid(row=5, column=0, columnspan=10)

        self.entryEndereco = Entry(frmDir, width=95, state='disabled')
        self.entryEndereco.grid(row=7, column=0, columnspan=10)

        self.entryBairro = Entry(frmDir, width=95, state='disabled')
        self.entryBairro.grid(row=9, column=0, columnspan=10)

        self.entryCidade = Entry(frmDir, width=95, state='disabled')
        self.entryCidade.grid(row=11, column=0, columnspan=10)

        self.entryEstado = Entry(frmDir, width=95, state='disabled')
        self.entryEstado.grid(row=13, column=0, columnspan=10)

        # TextBox
        self.txtObs = Text(frmDir, width=71, height=7, state='disabled')
        self.txtObs.grid(row=15, column=0, columnspan=10)
        
        self.listaInputs = [self.entryNome, self.entryTelefone, self.entryCpfCnpj, self.entryEndereco, self.entryBairro, self.entryCidade, self.entryEstado, self.txtObs]

        # Label
        Label(frmTop, text="Pesquisar:", background='grey').grid(row=0, column=0, sticky=W)
        Label(frmPrinc, text="Clientes:", background='#999').grid(row=0, column=0, sticky=W)
        Label(frmDir, text="NOME(*)", background='#DDD').grid(row=0, column=0, sticky=W, padx=10, columnspan=10)
        Label(frmDir, text="TELEFONE(*)", background='#DDD').grid(row=2, column=0, sticky=W, padx=10, columnspan=10)
        Label(frmDir, text="CPF/CNPJ", background='#DDD').grid(row=4, column=0, sticky=W, padx=10, columnspan=10)
        Label(frmDir, text="ENDEREÇO", background='#DDD').grid(row=6, column=0, sticky=W, padx=10, columnspan=10)
        Label(frmDir, text="BAIRRO", background='#DDD').grid(row=8, column=0, sticky=W, padx=10, columnspan=10)
        Label(frmDir, text="CIDADE", background='#DDD').grid(row=10, column=0, sticky=W, padx=10, columnspan=10)
        Label(frmDir, text="ESTADO", background='#DDD').grid(row=12, column=0, sticky=W, padx=10, columnspan=10)
        Label(frmDir, text="OBS", background='#DDD').grid(row=14, column=0, sticky=W, padx=10, columnspan=10)
        

    def onselect(self, evt):
        w = evt.widget
        index = w.curselection()[0]
        value = w.get(index)
        self.limpaCampos()
        for ins in self.listaInputs:
            ins['state'] = 'normal'
        strSql = '''SELECT * FROM cliente WHERE nome = ?'''
        res = db.selectSql(strSql, (value, ))[0]
        self.actID = res[0]
        self.entryNome.insert(0, res[1])
        self.entryTelefone.insert(0, f'({res[2][:2]}){res[2][2:7]}-{res[2][7:]}')
        self.entryCpfCnpj.insert(0, res[3])
        self.entryEndereco.insert(0, res[4])
        self.entryBairro.insert(0, res[5])
        self.entryCidade.insert(0, res[6])
        self.entryEstado.insert(0, res[7])
        self.txtObs.insert(1.0, res[8])
        self.selected = 1
        
    def pesquisa(self, evt):
        self.listaClientes.delete(0, END)
        self.carregaLista(self.entryPesquisa.get())
    
    def carregaLista(self, nome = ""):
        if nome == "":
            sqlStr = '''SELECT nome FROM cliente ORDER BY nome'''
            res = db.selectSql(sqlStr)
        else:
            sqlStr = f'SELECT nome FROM cliente WHERE nome LIKE "%{nome}%" ORDER BY nome'
            res = db.selectSql(sqlStr)
        for index, row in enumerate(res):
            self.listaClientes.insert(index, row[0])
        
    def novoCliente(self):
        self.destroy()
        self.parent.novoCliente() 
        
    def verAgend(self):
        if self.actID == -1:
            messagebox.showerror('', "SELECIONE UM CLIENTE PRIMEIRO")            
            return
        self.destroy()
        self.parent.verAgend(self.actID)

    def salvarCliente(self):
        tel = self.entryTelefone.get().replace('(', '').replace(')', '').replace('-', '').replace('_', '')
        if self.selected == 0:
            messagebox.showerror('', "NENHUM CLIENTE SELECIONADO")
            return
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
        if not messagebox.askyesno('', 'DESEJA SALVAR AS ALTERAÇÕES?'):
            return
        params = (self.entryNome.get(), tel, self.entryCpfCnpj.get(), self.entryEndereco.get(), self.entryBairro.get(), self.entryCidade.get(), self.entryEstado.get(), self.txtObs.get(1.0, END), self.actID)
        sqlStr = '''UPDATE cliente 
                    SET nome = ?, telefone = ?, cpfcnpj = ?, endereco = ?, bairro = ?, cidade = ?, estado = ?, obs = ?
                    WHERE idcliente = ?'''
        db.execSql(sqlStr, params)
        messagebox.showinfo('', "SALVO COM SUCESSO!")

    def excluirCliente(self):
        if self.selected == 0:
            messagebox.showerror('', "NENHUM CLIENTE SELECIONADO")
            return
        
        res = db.selectSql(f'SELECT * FROM agendamentos WHERE idcliente = {self.actID}')      
        if len(res) > 0:
            messagebox.showerror('', "NÃO É POSSÍVEL EXCLUIR CLIENTES COM AGENDAMENTOS EM ABERTO")
            return
        
        if not messagebox.askyesno('', f'DESEJA EXCLUIR O CLIENTE {self.entryNome.get()}?'):
            return
        sqlStr = f'DELETE FROM cliente WHERE idcliente = {self.actID}' 
        db.execSql(sqlStr)
        self.limpaCampos()
        self.listaClientes.delete(0, END)
        self.actID = -1
        self.carregaLista()
        
        messagebox.showinfo('', "EXCLUÍDO COM SUCESSO!")
    
    def limpaCampos(self):
        for ins in self.listaInputs:
            ins['state'] = 'normal'
        self.entryBairro.delete(0, END)
        self.entryCidade.delete(0, END)
        self.entryCpfCnpj.delete(0, END)
        self.entryEndereco.delete(0, END)
        self.entryEstado.delete(0, END)
        self.entryNome.delete(0, END)
        self.entryTelefone.delete(0, END)
        self.txtObs.delete(1.0, END) 
        for ins in self.listaInputs:
            ins['state'] = 'disabled'
        self.selected = 0
    
    def sair(self):
        self.parent.firstShow()
        self.destroy()