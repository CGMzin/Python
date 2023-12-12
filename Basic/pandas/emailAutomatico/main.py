import pandas, random

data = pandas.read_csv("./input/nomes_masculinos.csv")
lista_nomes = data.nome.to_list()

print(data[data.nome == "P"])
""" for _ in range(10):
    nome = random.choice(lista_nomes)
    with open("./input/texto_base.txt") as base:
        with open(f"./output/email_para_{nome}.txt", mode="w") as final:
            texto_base = base.read()
            texto_final = texto_base.replace("[nome]", nome)
            final.write(texto_final) """
