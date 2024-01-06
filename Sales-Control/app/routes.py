from app import app
from flask import render_template
import pandas as pd

@app.route('/')
def index():
    # Lê um arquivo Excel (substitua 'nome_do_arquivo.xlsx' pelo seu arquivo Excel)
    try:
        df = pd.read_excel('nome_do_arquivo.xlsx')  # Adicione o caminho correto do seu arquivo
        # Faça algo com os dados lidos, por exemplo, mostre no terminal
        print(df.head())  # Isso imprimirá as primeiras linhas do arquivo Excel no terminal
    except FileNotFoundError:
        print("Arquivo Excel não encontrado!")  # Trate o erro se o arquivo não for encontrado
    return render_template('index.html')
