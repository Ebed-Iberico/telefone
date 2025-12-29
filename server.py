#!/usr/bin/env python3
"""
SERVIDOR HTTP para Sistema Alo Trânsito
Versão corrigida para Python 3.14
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket
import os
import sys
import urllib.parse
from datetime import datetime

class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Handler com CORS e tratamento especial para arquivos"""
    
    def do_GET(self):
        # Analisar o caminho da URL
        parsed_path = urllib.parse.urlparse(self.path)
        request_path = parsed_path.path
        
        # Se acessar a raiz, redireciona para index.html
        if request_path == '/' or request_path == '':
            self.path = '/index.html'
            print(f"[INFO] Redirecionando para index.html")
        
        # Verificar se o arquivo existe
        file_path = self.translate_path(self.path)
        
        # Se não existir, tentar adicionar .html
        if not os.path.exists(file_path) and not self.path.endswith('.html'):
            if os.path.exists(file_path + '.html'):
                self.path += '.html'
                file_path += '.html'
                print(f"[INFO] Adicionando .html: {self.path}")
        
        # Se ainda não existir, mostrar 404 personalizado
        if not os.path.exists(file_path):
            print(f"[ERRO 404] Arquivo não encontrado: {self.path}")
            self.send_error(404, f"Arquivo não encontrado: {self.path}")
            return
        
        print(f"[OK 200] Servindo: {self.path}")
        return super().do_GET()
    
    def end_headers(self):
        # Adiciona headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Corrigido: Log formatado corretamente"""
        try:
            # Formato padrão de log do HTTP server
            sys.stderr.write("%s - - [%s] %s\n" %
                            (self.address_string(),
                             self.log_date_time_string(),
                             format % args if args else format))
        except:
            # Fallback simples
            timestamp = datetime.now().strftime("%d/%b/%Y %H:%M:%S")
            sys.stderr.write(f"{self.client_address[0]} - - [{timestamp}] {format}\n")

def get_port():
    """Obtém a porta do ambiente Render ou usa padrão"""
    return int(os.environ.get("PORT", 8000))

def check_html_files():
    """Verifica se existem arquivos HTML"""
    html_files = [f for f in os.listdir('.') if f.lower().endswith('.html')]
    if not html_files:
        print("❌ ERRO: Nenhum arquivo HTML encontrado!")
        return False
    
    # Verifica se precisa renomear para index.html
    if 'index.html' not in html_files and html_files:
        print(f"⚠️  index.html não encontrado. Usando {html_files[0]} como principal")
        # Não renomeia automaticamente, apenas avisa
    return True

def main():
    """Função principal do servidor"""
    PORT = get_port()
    HOST = "0.0.0.0"
    
    # Muda para diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Verifica arquivos HTML
    if not check_html_files():
        print("❌ Não é possível iniciar sem arquivos HTML")
        sys.exit(1)
    
    # Configura e inicia servidor
    try:
        server_address = (HOST, PORT)
        httpd = HTTPServer(server_address, CORSHTTPRequestHandler)
        httpd.allow_reuse_address = True
        
        print("\n" + "="*60)
        print("🚀 SERVIDOR HTTP INICIADO")
        print("="*60)
        print(f"📁 Diretório: {os.getcwd()}")
        print(f"🌐 URL: http://localhost:{PORT}")
        print(f"📄 Arquivos HTML: {[f for f in os.listdir('.') if f.endswith('.html')]}")
        print("="*60)
        print("⏹️  Pressione CTRL+C para parar")
        print("="*60 + "\n")
        
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Servidor interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"❌ ERRO: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()