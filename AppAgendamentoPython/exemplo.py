from tkinter import *
from tkinter import filedialog, messagebox, font
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time, json

IMPLICT_WAIT = 1

def create_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.headless = True

    driver = webdriver.Chrome() 
    
    driver.implicitly_wait(IMPLICT_WAIT) 

    return driver

def inserir_linha(idx, df, df_inserir):
    dfA = df.iloc[:idx, ]
    dfB = df.iloc[idx:, ]

    df = dfA.append(df_inserir).append(dfB).reset_index(drop = True)

    return df

def ler_arquivo():
    arquivo = filedialog.askopenfilename(initialdir="/Desktop", title="Selecione um arquivo", filetypes=[("Excel files", "*.xlsx")])
    entry_arquivo.insert(0, arquivo)

def search():
    index_cpf = -1

    if entry_arquivo.get() == "" or entry_login.get() == "" or entry_senha.get() == "" or entry_usuario.get() == "":
        messagebox.showerror(title="Verifique os campos", message="Antes de realizar a busca, verifique se todos os campos foram preenchidos corretamente")
        return

    new_data = pd.DataFrame({"CPF":{}, "NÚMERO-BENEFÍCIO":{}, "NOME-BENEFÍCIO":{}})
    data = pd.read_excel(entry_arquivo.get(), sheet_name="Plan1")
    data_dict = data.to_dict()

    new_info = {
        'usuario': entry_usuario.get(),
        'senha': entry_senha.get(),
        'login': entry_login.get()
    }

    with open(file="data\info.json", mode="w") as file:
                json.dump(new_info, file, indent=4)

    try:
        for index in data_dict["cpf"]:
            data_dict["cpf"][index] = str(data_dict["cpf"][index]).zfill(11)
    except:
        messagebox.showerror(title="Escolha um arquivo", message="Antes de realizar a busca, escolha um arquivo válido")
        return


    driver = create_driver()
    wait = WebDriverWait(driver, 3)

    driver.get("https://gestao.sistemacorban.com.br/index.php/auth/login")

    user = driver.find_element(By.ID, "exten")
    user.send_keys(entry_usuario.get())

    passwd = driver.find_element(By.NAME, "password")
    passwd.send_keys(entry_senha.get())

    btn_login = driver.find_element(By.XPATH, "/html/body/main/form/div[4]/button")
    btn_login.click()

    try:
        alert = wait.until(EC.alert_is_present())
        alert.accept()
    except:
        pass

    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/div[2]/div/div[3]/div/div/div[2]/div[1]/div[3]/a")))
    btn_receptivo = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div/div[3]/div/div/div[2]/div[1]/div[3]/a")
    btn_receptivo.click()

    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[3]/div[2]/div/div[4]/div[1]/a")))
    btn_inss = driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div/div[4]/div[1]/a")
    btn_inss.click()

    wait.until(EC.element_to_be_clickable((By.ID, "CLI_CPF2")))
   
    for cpf in data_dict["cpf"].values():
        wait.until(EC.element_to_be_clickable((By.ID, "CLI_CPF2")))
        driver.find_element(By.ID, "CLI_CPF2").send_keys(cpf)
        driver.find_element(By.ID, "btn_buscaCpf").click()

        time.sleep(1)
        try:
            btn_beneficios = driver.find_elements(By.XPATH, "/html/body/div/div[3]/div[2]/div/div[4]/div/div/div") 
        except:
            time.sleep(1.5)
            btn_beneficios = driver.find_elements(By.XPATH, "/html/body/div/div[3]/div[2]/div/div[4]/div/div/div") 

        for _ in range(len(btn_beneficios)):
            beneficio = ""
            index_cpf += 1
            time.sleep(1.5)
            if len(btn_beneficios) - 1 == 0:
                beneficio = driver.find_element(By.XPATH, f"/html/body/div/div[3]/div[2]/div/div[4]/div/div/div/a").text
                driver.find_element(By.XPATH, f"/html/body/div/div[3]/div[2]/div/div[4]/div/div/div/a").click()
            else:
                beneficio = driver.find_element(By.XPATH, f"/html/body/div/div[3]/div[2]/div/div[4]/div/div/div[{len(btn_beneficios)}]/a").text
                driver.find_element(By.XPATH, f"/html/body/div/div[3]/div[2]/div/div[4]/div/div/div[{len(btn_beneficios)}]/a").click()

            wait.until(EC.element_to_be_clickable((By.ID, "btnOcultar")))
            try:
                time.sleep(0.5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div/div[4]/div[4]/div/div/a[10]/div").click()
            except:
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.find_element(By.XPATH, "/html/body/div/div[3]/div[2]/div/div[4]/div[5]/div/div/a[10]/div").click()
            time.sleep(1)
            try:
                driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div/div[8]/div/div/div[2]/div[1]/table/tbody/tr")
                driver.find_element(By.NAME, "reenviar").click()
                try:
                    alert = wait.until(EC.alert_is_present())
                    alert.accept()
                except:
                    pass
            except:
                select = Select(driver.find_element(By.ID, "idSenha"))
                select.select_by_value(entry_login.get())
                driver.find_element(By.NAME, "btnAtualizarIn100").click()
                try:
                    alert = wait.until(EC.alert_is_present())
                    alert.accept()
                except:
                    pass
            finally:
                driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[2]/div/div[8]/div/div/div[3]/button").click()
                time.sleep(1)
                driver.execute_script("window.scrollTo(0, 1);")
                time.sleep(0.5)
                driver.find_element(By.ID, "CLI_CPF2").send_keys(cpf)
                driver.find_element(By.ID, "btn_buscaCpf").click()
                btn_beneficios.pop(0)
                new_data = pd.concat([new_data, pd.DataFrame({'CPF': f'{cpf}', 'NÚMERO-BENEFÍCIO': f'{beneficio[:beneficio.find(":")]}', 'NOME-BENEFÍCIO': f'{beneficio[beneficio.find(":") + 1:]}'}, columns=new_data.columns, index=[0])], ignore_index=True)
    
    new_data.to_excel("data/novalistainss.xlsx", sheet_name="Nova Lista", index=False)

    driver.quit()
    driver.stop_client()

window = Tk("main")
window.title("Consultar Dados")
window.resizable(0, 0)
default_font = font.nametofont("TkDefaultFont")
default_font.configure(family="Arial", size=14, weight=font.BOLD)
window.config()

largura = 800
altura = 300

largura_tela = window.winfo_screenwidth()
altura_tela =  window.winfo_screenmmheight()

posix = largura_tela/2 - largura / 2
posiy = altura_tela/2 

window.geometry("%dx%d+%d+%d" % (largura,altura,posix,posiy))

#Frames ---------------
frame_top = Frame(window, bg="lightgray", padx=120, pady=15)
frame_top.pack(fill=BOTH)

frame_main = Frame(window, padx=100, pady=25)
frame_main.pack(fill=BOTH)

#Labels ---------------
lbl_msg = Label(frame_top, text="Consultar Dados Corban", font=("Arial", 35, "bold"), bg="lightgray")
lbl_msg.grid(row=0, column=0, columnspan=5)

lbl_planilha = Label(frame_main, text="Planilha:")
lbl_planilha.grid(row=0, column=0)

lbl_usuario = Label(frame_main, text="Usuário:")
lbl_usuario.grid(row=1, column=0)

lbl_senha = Label(frame_main, text="Senha:")
lbl_senha.grid(row=2, column=0)

lbl_login = Label(frame_main, text="Valor do login:")
lbl_login.grid(row=3, column=0)

#Entrys -------------------
entry_arquivo = Entry(frame_main, width=40)
entry_arquivo.grid(row=0, column=1)

entry_usuario = Entry(frame_main, width=40)
entry_usuario.grid(row=1, column=1)

entry_senha = Entry(frame_main, width=40)
entry_senha.grid(row=2, column=1)

entry_login = Entry(frame_main, width=40)
entry_login.grid(row=3, column=1)

#Buttons -------------------
btn_arquivo_arquivo = Button(frame_main, text="Escolher", width=15, font=("Arial", 10, "bold"), command=ler_arquivo)
btn_arquivo_arquivo.grid(row=0, column=2, padx=10)

btn_buscar = Button(frame_main, text="Buscar", width=15, font=("Arial", 10, "bold"), command=search)
btn_buscar.grid(row=4, column=1, pady=5)

#Preencher dados -------------------------
try:    
    with open(file="data\info.json", mode="r") as file:
        info = json.load(file)
        entry_usuario.insert(0, info["usuario"])
        entry_senha.insert(0, info["senha"])
        entry_login.insert(0, info["login"])
except:
    pass


window.mainloop()