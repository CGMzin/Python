import cliente, novoCliente, novoAgendamento, datetime, db, agendCliente, novoAgendCliente
import sqlite3 as sql
from tkinter import *
import tkcalendar as tkc
from tkinter import messagebox, font

class Window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("AGENDAMENTOS")
        self.resizable(0, 0)
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Arial", size=14, weight=font.BOLD)
        self.config()
        
        self.overrideredirect(1)

        self.actID = 0
        self.conc = 0
        self.showConc = 0
        self.selected = 0
        
        self.agendamentos = {}

        largura = 800
        altura = 450
        
        x = self.winfo_screenwidth() // 2 - largura // 2
        y = self.winfo_screenheight() // 2 - altura // 2

        self.geometry("%dx%d+%d+%d" % (largura,altura,x,y))

        # Frame
        frmTop = Frame(self, background='grey', pady=10, height=25)
        frmTop.pack(side='top', fill=BOTH)
        
        frmPrinc = Frame(self, width=50, background='#999')
        frmPrinc.pack(side='left', fill=BOTH)

        frmDir = Frame(self, background='#DDD', padx=15, pady=10)
        frmDir.pack(side='right', fill=BOTH, expand=True)
        

        # Buttons
        btnFiltrar = Button(frmTop, text="FILTRAR", command=self.filtraData, font=("Arial", 8, 'bold'))
        btnFiltrar.grid(row=0, column=5, padx=10)

        btnCriar = Button(frmDir, text="PAGAR", command=self.paga)
        btnCriar.grid(row=14, column=0, pady=10, padx=5, sticky=W)

        btnSalvar = Button(frmDir, text="SALVAR", command=self.salvaAgendamento)
        btnSalvar.grid(row=14, column=1, pady=10, padx=5, sticky=W)

        btnExcluir = Button(frmDir, text="EXCLUIR", command=self.excluiAgendamento)
        btnExcluir.grid(row=14, column=2, pady=10, padx=5, sticky=W)

        btnClientes = Button(frmDir, text="VOLTAR", command=self.sair)
        btnClientes.grid(row=14, column=3, pady=10, padx=5, sticky=W)


        #Scroll
        scroll = Scrollbar(frmPrinc)
        scroll.grid(row=1, column=1, sticky=NS)

        # List
        self.agenList = Listbox(frmPrinc, yscrollcommand=scroll.set, width=15, height=16, font=("Arial", 14, 'bold'), fg="red", selectbackground="red", selectforeground="white")
        self.agenList.grid(row=1, column=0)
        scroll.config(command=self.agenList.yview)
        self.agenList.bind('<<ListboxSelect>>', self.onselect)
        self.carregaLista()

        # Entrys
        now = datetime.datetime.now()
        self.entryDataIni = tkc.DateEntry(frmTop, selectmode='day', date_pattern='dd/MM/yyyy')
        self.entryDataIni.grid(row=0, column=1)
        self.entryDataIni.set_date(datetime.date.today())
        
        self.entryDataFin = tkc.DateEntry(frmTop, selectmode='day', date_pattern='dd/MM/yyyy')
        self.entryDataFin.grid(row=0, column=3)
        self.entryDataFin.set_date(datetime.date.today())
        
        self.entryCliente = Entry(frmDir, width=95, state='disabled')
        self.entryCliente.grid(row=1, column=0, columnspan=10)
        
        self.entryProduto = Entry(frmDir, width=95, state='disabled')
        self.entryProduto.grid(row=3, column=0, columnspan=10)

        self.entryData = Entry(frmDir, width=95, state='disabled')
        self.entryData.grid(row=5, column=0, columnspan=10)

        self.entryValor = Entry(frmDir, width=95, state='disabled')
        self.entryValor.grid(row=7, column=0, columnspan=10)

        # TextBox
        self.txtObs = Text(frmDir, width=71, height=7, state='disabled')
        self.txtObs.grid(row=9, column=0, columnspan=10)
        
        self.listaInputs = [self.entryProduto, self.entryData, self.entryValor, self.txtObs]

        # Label
        Label(frmTop, text="NÃO PAGOS", background='grey').grid(row=0, column=0, sticky=W, padx=35)
        Label(frmTop, text="ATÉ", background='grey').grid(row=0, column=2, sticky=W, padx=20)
        Label(frmPrinc, text="Agendamentos:", background='#999').grid(row=0, column=0, sticky=W)
        Label(frmDir, text="CLIENTE", background='#DDD').grid(row=0, column=0, sticky=W, columnspan=10)
        Label(frmDir, text="PRODUTO / SERVIÇO", background='#DDD').grid(row=2, column=0, sticky=W, columnspan=10)
        Label(frmDir, text="DATA / HORA", background='#DDD').grid(row=4, column=0, sticky=W, columnspan=10)
        Label(frmDir, text="VALOR", background='#DDD').grid(row=6, column=0, sticky=W, columnspan=10)
        Label(frmDir, text="OBS", background='#DDD').grid(row=8, column=0, sticky=W, columnspan=10)
        
        self.firstShow()
        
    def onselect(self, evt):
        w = evt.widget
        index = w.curselection()[0]
        value = w.get(index)
        val = value[:value.find("-")].strip()
        idAg = self.agendamentos[val]["idagendamento"]
        self.actID = idAg
        self.limpaCampos()
        self.entryCliente['state'] = 'normal'
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
        self.entryCliente.insert(0, res[5])
        self.selected = 1
        self.entryCliente['state'] = 'disabled'

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
        
        params = (self.entryProduto.get(), insertDate, self.entryValor.get(), self.txtObs.get(1.0, END), self.actID)
        strSql = '''UPDATE agendamentos 
                    SET produtoservico = ?, data = ?, valor = ?, concluido = 1, obsAg = ?
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
        self.entryCliente['state'] = 'normal'
        for ins in self.listaInputs:
            ins['state'] = 'normal'
        self.entryCliente.delete(0, END)
        self.entryValor.delete(0, END)
        self.entryData.delete(0, END)
        self.entryProduto.delete(0, END)
        self.txtObs.delete(1.0, END) 
        self.selected = 0
        self.entryCliente['state'] = 'disabled'
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
 
    def firstShow(self):
        self.carregaLista("0") 
        self.deiconify()
      
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

        params = (insertDateIni, insertDateFin)
        
        res = db.selectSql('''SELECT idagendamento, idcliente, data FROM agendamentos WHERE concluido = 1 AND pago = 0 AND data > ? AND data < ? ORDER BY data''', params)
        for index, row in enumerate(res):
            date = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            self.agendamentos[str(index + 1)] = {"idagendamento": row[0], "idcliente": row[1], "data": row[2]}
            self.agenList.insert(index, f"{index + 1} - {str(date.date().day).zfill(2)}/{str(date.date().month).zfill(2)} {str(date.time())[:-3]}")

    def paga(self):
        if self.selected == 0:
            messagebox.showerror('', "NENHUM AGENDAMENTO SELECIONADO")
            return
        if not messagebox.askyesno('', f'DESEJA REALIZAR O PAGAMENTO DESSE AGENDAMENTO?'):
            return
        db.execSql(f'UPDATE agendamentos SET pago = 1 WHERE idagendamento = {self.actID}' )
        self.limpaCampos()
        self.selected = 0
        self.agenList.delete(0, END)
        self.firstShow()
        messagebox.showinfo('', "PAGO COM SUCESSO!")
    
    def sair(self):
        self.parent.firstShow()
        self.destroy()
