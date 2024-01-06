from app import app
from flask import render_template, request
import pandas as pd

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['excelFile']
    if uploaded_file.filename != '':
        try:
            df = pd.read_excel(uploaded_file)

            # Altere 'Produtos' para o nome correto da aba ou planilha no seu arquivo Excel
            produtos = df[df['Planilha'] == 'Produtos'] if 'Planilha' in df.columns else df

            produtos_info = produtos[['Produto', 'Quantidade']] if 'Produto' in produtos.columns else produtos
            produtos_info_html = produtos_info.to_html(index=False)
            return render_template('result.html', produtos_info=produtos_info_html)
        except Exception as e:
            return f"Erro ao processar o arquivo: {str(e)}"
    return "Nenhum arquivo selecionado!"
