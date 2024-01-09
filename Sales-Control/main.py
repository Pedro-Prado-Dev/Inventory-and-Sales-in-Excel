import webview
from app import app

def start_flask():
    app.run()

if __name__ == '__main__':
    webview.create_window("Sistema de Controle", "http://127.0.0.1:5000/")
    webview.start(start_flask)

