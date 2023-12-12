import novoAgendCliente, datetime, db, finaliza
import sqlite3 as sql
from tkinter import *
import tkcalendar as tkc
from tkinter import messagebox, font

class Window(Toplevel):
    def __init__(self, parent, cliente):
        super().__init__(parent)
        self.parent = parent

        self.title("AGENDAMENTOS/CLIENTES")
        self.resizable(0, 0)
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=14, weight=font.BOLD)
        self.config()
        
        self.overrideredirect(1)

        self.actID = 0
        self.conc = 0
        self.showConc = 0
        self.showLeva = 0
        self.selected = 0
        self.cliente = cliente
        
        res = db.selectSql(f'SELECT nome FROM cliente WHERE idcliente = {self.cliente}')
        self.nomeCliente = res[0][0]
        
        self.agendamentos = {}

        largura = 820
        altura = 400
        
        x = self.winfo_screenwidth() // 2 - largura // 2
        y = self.winfo_screenheight() // 2 - altura // 2

        self.geometry("%dx%d+%d+%d" % (largura,altura,x,y))

        # Frame
        frmTop = Frame(self, background='grey', padx=15, pady=10, height=25)
        frmTop.pack(side='top', fill=BOTH)
        
        frmPrinc = Frame(self, width=50, background='#999')
        frmPrinc.pack(side='left', fill=BOTH)

        frmDir = Frame(self, background='#DDD', padx=30, pady=10)
        frmDir.pack(side='right', fill=BOTH, expand=True)
        

        # Buttons
        btnFiltrar = Button(frmTop, text="FILTRAR", command=self.filtraData, font=("Arial", 8, 'bold'))
        btnFiltrar.grid(row=0, column=5, padx=10)
        
        self.btnConcl = Button(frmTop, text="VER AGENDAMENTOS CONCLUÍDOS", command=self.verConcluidos, font=("Arial", 8, 'bold'))
        self.btnConcl.grid(row=0, column=6)
        
        self.btnLevaTraz = Button(frmTop, text="LEVA E TRAZ", command=self.LevaTraz, font=("Arial", 8, 'bold'))
        self.btnLevaTraz.grid(row=0, column=7, padx=10)

        btnCriar = Button(frmDir, text="CRIAR", command=self.criaAgendamento)
        btnCriar.grid(row=14, column=0, pady=10, padx=5, sticky=W)

        btnSalvar = Button(frmDir, text="SALVAR", command=self.salvaAgendamento)
        btnSalvar.grid(row=14, column=1, pady=10, padx=5, sticky=W)

        btnExcluir = Button(frmDir, text="EXCLUIR", command=self.excluiAgendamento)
        btnExcluir.grid(row=14, column=2, pady=10, padx=5, sticky=W)

        btnFinaliza = Button(frmDir, text="CONCLUIR", command=self.pergunta)
        btnFinaliza.grid(row=14, column=4, pady=10, padx=5, sticky=W)

        btnClientes = Button(frmDir, text="VOLTAR", command=self.sair)
        btnClientes.grid(row=14, column=3, pady=10, padx=5, sticky=W)

        #Scroll
        scroll = Scrollbar(frmPrinc)
        scroll.grid(row=1, column=1, sticky=NS)

        # List
        self.agenList = Listbox(frmPrinc, yscrollcommand=scroll.set, width=15, height=14)
        self.agenList.grid(row=1, column=0)
        scroll.config(command=self.agenList.yview)
        self.agenList.bind('<<ListboxSelect>>', self.onselect)
        self.carregaLista('0')

        # Entrys
        now = datetime.datetime.now()
        self.entryDataIni = tkc.DateEntry(frmTop, selectmode='day', date_pattern='dd/MM/yyyy')
        self.entryDataIni.grid(row=0, column=1)
        self.entryDataIni.set_date(datetime.date.today())
        
        self.entryDataFin = tkc.DateEntry(frmTop, selectmode='day', date_pattern='dd/MM/yyyy')
        self.entryDataFin.grid(row=0, column=3)
        self.entryDataFin.set_date(datetime.date.today())
        
        self.entryProduto = Entry(frmDir, width=95, state='disabled')
        self.entryProduto.grid(row=1, column=0, columnspan=10)

        self.entryData = Entry(frmDir, width=95, state='disabled')
        self.entryData.grid(row=3, column=0, columnspan=10)

        self.entryValor = Entry(frmDir, width=95, state='disabled')
        self.entryValor.grid(row=5, column=0, columnspan=10)

        # TextBox
        self.txtObs = Text(frmDir, width=71, height=7, state='disabled')
        self.txtObs.grid(row=7, column=0, columnspan=10)
        
        self.listaInputs = [self.entryProduto, self.entryData, self.entryValor, self.txtObs]

        # Label
        Label(frmTop, text="ATÉ", background='grey').grid(row=0, column=2, sticky=W, padx=20)
        if len(self.nomeCliente) > 10:
            lbl_txt = f"CLIENTE: {self.nomeCliente[:10]}..."
        else:
            lbl_txt = f"CLIENTE: {self.nomeCliente}"
        Label(frmTop, text=lbl_txt, background='grey', font=("Arial", 12, 'bold')).grid(row=0, column=0, sticky=W, padx=10)
        self.lblAgend = Label(frmPrinc, text="Agendamentos:", background='#999')
        self.lblAgend.grid(row=0, column=0, sticky=W)
        Label(frmDir, text="PRODUTO / SERVIÇO", background='#DDD').grid(row=0, column=0, sticky=W, columnspan=10)
        Label(frmDir, text="DATA / HORA", background='#DDD').grid(row=2, column=0, sticky=W, columnspan=10)
        Label(frmDir, text="VALOR", background='#DDD').grid(row=4, column=0, sticky=W, columnspan=10)
        Label(frmDir, text="OBS", background='#DDD').grid(row=6, column=0, sticky=W, columnspan=10)
        
    def onselect(self, evt):
        w = evt.widget
        index = w.curselection()[0]
        value = w.get(index)
        val = value[:value.find("-")].strip()
        idAg = self.agendamentos[val]["idagendamento"]
        self.actID = idAg
        self.limpaCampos()
        for ins in self.listaInputs:
            ins['state'] = 'normal'
        strSql = '''SELECT produtoservico, data, valor, concluido, obsAg, nome
                          FROM agendamentos 
                          INNER JOIN cliente
                          ON agendamentos.idcliente = cliente.idcliente
                          WHERE idagendamento = ?'''
        
        res = db.selectSql(strSql, (idAg,))[0]
        self.entryProduto.insert(0, res[0])
        date = datetime.datetime.strptime(res[1], '%Y-%m-%d %H:%M:%S')
        strData = f'{str(date.day).zfill(2)}/{str(date.month).zfill(2)}/{str(date.year)} {str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}'
        self.entryData.insert(0, strData)
        self.entryValor.insert(0, res[2])
        self.conc = res[3]
        self.txtObs.insert(1.0, res[4])
        self.selected = 1
        
    def criaAgendamento(self):
        self.parent.novoAgendCli(self.cliente)
        self.destroy()

    def salvaAgendamento(self):
        if self.selected == 0:
            messagebox.showerror('', "NENHUM AGENDAMENTO SELECIONADO")
            return
        for ins in self.listaInputs[:-1]:
            if ins.get().replace("R$", "").replace(",", "").replace(".", "").replace("/", "").replace("-", "").replace("_", "").strip() == "" or ins.get() == "__/__/____ __:__":
                messagebox.showerror('', "NÃO DEIXE CAMPOS EM BRANCO")
                return
        try:
            date = datetime.datetime.strptime(self.entryData.get() + ":00", '%d/%m/%Y %H:%M:%S')
        except:
            messagebox.showerror('', "DATA INVÁLIDA")
            return
        if not messagebox.askyesno('', 'DESEJA SALVAR AS ALTERAÇÕES?'):
            return
            
        insertDate = f'{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)} {str(date.hour).zfill(2)}:{str(date.minute).zfill(2)}:{str(date.second).zfill(2)}'
            
        params = (self.entryProduto.get(), insertDate, self.entryValor.get(), self.conc, self.txtObs.get(1.0, END), self.actID)
        strSql = '''UPDATE agendamentos 
                    SET produtoservico = ?, data = ?, valor = ?, concluido = ?, obsAg = ?
                    WHERE idagendamento = ?'''
        db.execSql(strSql, params)
        messagebox.showinfo('', "SALVO COM SUCESSO!")

    def excluiAgendamento(self):
        if self.selected == 0:
            messagebox.showerror('', "NENHUM AGENDAMENTO SELECIONADO")
            return
        res = db.selectSql(f'SELECT concluido FROM agendamentos WHERE idagendamento = {self.actID}')
        if not messagebox.askyesno('', f'DESEJA EXCLUIR ESSE AGENDAMENTO?'):
            return
        db.execSql(f'DELETE FROM agendamentos WHERE idagendamento = {self.actID}')        
        self.limpaCampos()
        self.agenList.delete(0, END)
        self.filtraData()
        messagebox.showinfo('', "EXCLUÍDO COM SUCESSO!")
        
    def limpaCampos(self):
        for ins in self.listaInputs:
            ins['state'] = 'normal'
        self.entryValor.delete(0, END)
        self.entryData.delete(0, END)
        self.entryProduto.delete(0, END)
        self.txtObs.delete(1.0, END) 
        self.selected = 0
        for ins in self.listaInputs:
            ins['state'] = 'disabled'
        
    def filtraData(self):
        try:
            dataIni = datetime.datetime.strptime(self.entryDataIni.get(), '%d/%m/%Y').date()
            dataFin = datetime.datetime.strptime(self.entryDataFin.get(), '%d/%m/%Y').date()
            
            if dataIni > dataFin:
                messagebox.showerror('', 'DATA INICIAL NÃO PODE SER MAIOR QUE A FINAL')

            self.carregaLista(self.entryDataIni.get(), self.entryDataFin.get())      
            self.limpaCampos()     
        except:
            messagebox.showerror('', 'DATA INVÁLIDA')
            return       
          
    def verConcluidos(self):
        if self.showConc == 0:
            self.showConc = 1
        else:
            self.showConc = 0
        
        self.filtraData()
        
    def carregaLista(self, dIni = f'{str(datetime.datetime.now().day).zfill(2)}/{str(datetime.datetime.now().month).zfill(2)}/{datetime.datetime.now().year}', dFin = f'{str(datetime.datetime.now().day).zfill(2)}/{str(datetime.datetime.now().month).zfill(2)}/{datetime.datetime.now().year}'):
        self.agenList.delete(0, END)
        if dIni == '0':
            diaInicial = '01/01/1993 00:00:00'
        else: 
            diaInicial = dIni + ' 00:00:01'
            
        diaFinal = dFin + ' 23:59:59'
        
        try:
            dateIni = datetime.datetime.strptime(diaInicial, '%d/%m/%Y %H:%M:%S')
            dateFin = datetime.datetime.strptime(diaFinal, '%d/%m/%Y %H:%M:%S')
        except:
            messagebox.showerror('', "DATA INVÁLIDA")
            return
        
        
        insertDateIni = f'{dateIni.year}-{str(dateIni.month).zfill(2)}-{str(dateIni.day).zfill(2)} {str(dateIni.hour).zfill(2)}:{str(dateIni.minute).zfill(2)}:{str(dateIni.second).zfill(2)}'
        insertDateFin = f'{dateFin.year}-{str(dateFin.month).zfill(2)}-{str(dateFin.day).zfill(2)} {str(dateFin.hour).zfill(2)}:{str(dateFin.minute).zfill(2)}:{str(dateFin.second).zfill(2)}'
        
        if self.showConc == 0:
            self.btnConcl.configure(text="VER AGENDAMENTOS EM ABERTO")
            conc = 0
        else:
            self.btnConcl.configure(text="VER AGENDAMENTOS CONCLUÍDOS")
            conc = 1
            
        if self.showLeva == 0:
            try:
                self.lblAgend.config(text="Agendamentos:")
                self.btnLevaTraz.configure(text="LEVA E TRAZ")
            except:
                pass
            
            leva = 0
        else:
            try:
                self.lblAgend.config(text="Leva e Traz:")
                self.btnLevaTraz.configure(text="NORMAIS")
            except:
                pass
        
            leva = 1 
            
        params = (conc, insertDateIni, insertDateFin, leva)
        
        res = db.selectSql('''SELECT idagendamento, idcliente, data FROM agendamentos WHERE concluido = ? AND data > ? AND data < ? AND leva = ? ORDER BY data''', params)
        for index, row in enumerate(res):
            date = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            self.agendamentos[str(index + 1)] = {"idagendamento": row[0], "idcliente": row[1], "data": row[2]}
            self.agenList.insert(index, f"{index + 1} - {str(date.date().day).zfill(2)}/{str(date.date().month).zfill(2)} {str(date.time())[:-3]}")
            
    def pergunta(self):
        if self.selected == 0:
            messagebox.showerror('', "NENHUM AGENDAMENTO SELECIONADO")
            return
        res = db.selectSql(f'SELECT concluido FROM agendamentos WHERE idagendamento = {self.actID}')
        if res[0][0] == 1:
            messagebox.showerror('', "AGENDAMENTO JÁ FOI CONCLUÍDO")
            return
        if not messagebox.askyesno('', f'DESEJA FINALIZAR ESSE AGENDAMENTO?'):
            return
        ws = finaliza.Window(self)
        ws.grab_set()
        self.limpaCampos()

    def finaliza(self, pago):
        if pago == 0:
            db.execSql(f'UPDATE agendamentos SET concluido = 1, pago = 0 WHERE idagendamento = {self.actID}' )
        else: 
            db.execSql(f'UPDATE agendamentos SET concluido = 1, pago = 1 WHERE idagendamento = {self.actID}' )
        messagebox.showinfo('', "CONCLUÍDO COM SUCESSO!")
        self.limpaCampos()
        self.selected = 0
        self.agenList.delete(0, END)
        self.carregaLista()
      
    def LevaTraz(self):
        if self.showLeva == 0:
            self.showLeva = 1
            self.carregaLista()
        else:
            self.showLeva = 0
            self.carregaLista()
      
    def sair(self):
        self.parent.verClientes()
        self.destroy()