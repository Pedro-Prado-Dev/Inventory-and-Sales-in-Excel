from app import app
from flask import render_template, request, redirect
from datetime import datetime
import pandas as pd
import os

UPLOAD_FOLDER = 'uploads'  # Diretório para salvar os arquivos enviados

# Configuração do diretório de uploads
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')

@app.route('/cadastrar_novo_produto', methods=['POST'])
def cadastrar_novo_produto():
    produto = request.form['produto']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])
    data_atual = datetime.now().strftime('%Y-%m-%d')

    try:
        arquivo_excel = request.files['excelFile']

        # Salva o arquivo Excel enviado pelo usuário
        arquivo_path = os.path.join(UPLOAD_FOLDER, f'planilha_{data_atual}.xlsx')
        arquivo_excel.save(arquivo_path)

        # Lê o arquivo Excel e identifica a planilha "Produtos"
        df = pd.read_excel(arquivo_path, sheet_name='Produtos' if 'Produtos' in pd.ExcelFile(arquivo_path).sheet_names else None)

        # Se a planilha "Produtos" não existir, cria um novo DataFrame
        if df is None:
            df = pd.DataFrame(columns=['Produto', 'Quantidade', 'Preço'])

        # Adiciona o novo produto ao DataFrame correspondente à planilha "Produtos"
        novo_produto = {'Produtos': produto, 'Quantidade': quantidade, 'Preço': preco}
        df = pd.concat([df, pd.DataFrame([novo_produto])], ignore_index=True)

        # Salva o DataFrame de volta no arquivo Excel original
        with pd.ExcelWriter(arquivo_path, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Produtos')

        return redirect('/visualizar')
    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}"
    

@app.route('/adicionar', methods=['GET', 'POST'])
def aumentar_quantidade_produto():
    if request.method == 'POST':
        produto = request.form['produto']
        quantidade = int(request.form['quantidade'])

        # Aqui você pode adicionar a lógica para aumentar a quantidade de produtos existentes no DataFrame ou no Excel

        # Exemplo de retorno após aumentar a quantidade do produto (pode ajustar conforme necessário)
        return f"Quantidade do Produto '{produto}' aumentada para {quantidade} com sucesso!"

    return render_template('aumentar_quantidade.html')

@app.route('/visualizar')
def visualizar():
    data_atual = datetime.now().strftime('%Y-%m-%d')
    try:
        arquivo_path = os.path.join(UPLOAD_FOLDER, f'planilha_{data_atual}.xlsx')

        # Lê o arquivo Excel e identifica a planilha "Produtos"
        df = pd.read_excel(arquivo_path, sheet_name='Produtos' if 'Produtos' in pd.ExcelFile(arquivo_path).sheet_names else None)

        if df is None:
            df = pd.DataFrame(columns=['Produtos', 'Quantidade', 'Preço'])

        return render_template('visualizar.html', produtos=df)
    except Exception as e:
        return f"Erro ao processar o arquivo: {str(e)}"