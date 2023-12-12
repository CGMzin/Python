import sqlite3 as sql

def create():  
    con = sql.connect("DBTeste.db")
    cur = con.cursor()
    cur.executescript('''
                CREATE TABLE IF NOT EXISTS usuario(
                    idusuario INTEGER NOT NULL,
                    nome TEXT NOT NULL, 
                    senha TEXT NOT NULL, 
                    tipo INTEGER NOT NULL,
                    PRIMARY KEY(idusuario)
                );
                    
                CREATE TABLE IF NOT EXISTS cliente(
                    idcliente INTEGER NOT NULL,
                    nome TEXT NOT NULL,
                    telefone TEXT NOT NULL, 
                    cpfcnpj TEXT,
                    endereco TEXT, 
                    bairro TEXT, 
                    cidade TEXT, 
                    estado TEXT, 
                    obs TEXT, 
                    PRIMARY KEY(idcliente)
                ); 
                
                CREATE TABLE IF NOT EXISTS agendamentos(
                    idagendamento INTEGER NOT NULL,
                    produtoservico TEXT NOT NULL, 
                    data timestamp NOT NULL,
                    valor REAL NOT NULL,
                    concluido INTEGER NOT NULL,
                    leva INTEGER NOT NULL,
                    obsAg TEXT,
                    idcliente INTEGER, 
                    pago INTEGER NOT NULL,
                    FOREIGN KEY(idcliente) REFERENCES cliente(idcliente),
                    PRIMARY KEY(idagendamento)
                );
                
                CREATE TABLE IF NOT EXISTS produto(
                    idproduto INTEGER NOT NULL,
                    descricao TEXT NOT NULL,
                    qtd TEXT NOT NULL, 
                    codbarras TEXT,
                    valorcusto TEXT, 
                    valorunitario TEXT, 
                    margemganho TEXT, 
                    PRIMARY KEY(idproduto)
                );
                
                CREATE TABLE IF NOT EXISTS osVenda(
                    idlinha INTEGER NOT NULL,
                    numOs INTEGER NOT NULL,
                    idproduto INTEGER NOT NULL,
                    descricao TEXT NOT NULL,
                    qtd REAL NOT NULL, 
                    codbarras TEXT,
                    valorunitario REAL NOT NULL, 
                    valortotal REAL NOT NULL,                 
                    FOREIGN KEY(idproduto) REFERENCES produto(idproduto),
                    PRIMARY KEY(idlinha)
                );
                
                CREATE TABLE IF NOT EXISTS preVenda(
                    idlinha INTEGER NOT NULL,
                    idproduto INTEGER NOT NULL,
                    descricao TEXT NOT NULL,
                    qtd REAL NOT NULL, 
                    codbarras TEXT,
                    valorunitario REAL NOT NULL, 
                    valortotal REAL NOT NULL,
                    FOREIGN KEY(idproduto) REFERENCES produto(idproduto),
                    PRIMARY KEY(idlinha)
                );''')
    con.close()

def execSql(sqlStr:str, params:tuple = ()) -> None:
    con = sql.connect("DBTeste.db")
    cur = con.cursor()
    if params == ():
        cur.execute(sqlStr)
        con.commit()
    else:        
        cur.execute(sqlStr, params)
        con.commit()
    con.close()
    
def selectSql(sqlStr:str, params:tuple = ()) -> list:
    con = sql.connect("DBTeste.db")
    cur = con.cursor()
    if params == ():
        cur.execute(sqlStr)
        res = cur.fetchall()
        con.commit()
    else:        
        cur.execute(sqlStr, params)
        res = cur.fetchall()
        con.commit()
    con.close()
    return res