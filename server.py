#!/usr/bin/env python3
"""
Servidor HTTP mínimo para Alo Trânsito - Versão Corrigida
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import time

PORT = int(os.environ.get("PORT", 8000))

class AloTransitoHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Ignorar favicon.ico se não existir
        if self.path == '/favicon.ico':
            if not os.path.exists(self.translate_path(self.path)):
                self.send_response(204)  # No Content
                self.end_headers()
                return
        
        # Redireciona raiz para login
        if self.path in ['/', '']:
            self.path = '/login.html'
            print(f"[→] Raiz → login.html")
        
        # Adiciona .html se necessário
        elif not self.path.endswith('.html') and os.path.exists(self.translate_path(self.path + '.html')):
            self.path += '.html'
            print(f"[+] Adicionado .html: {self.path}")
        
        # Tenta servir o arquivo
        try:
            return super().do_GET()
        except ConnectionAbortedError:
            # Cliente fechou a conexão, ignorar
            print(f"[!] Conexão fechada pelo cliente: {self.path}")
        except Exception as e:
            print(f"[✗] Erro ao servir {self.path}: {e}")
            self.send_error(404, f"Arquivo não encontrado: {self.path}")
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Log simplificado"""
        timestamp = time.strftime("%H:%M:%S")
        message = format % args if args else format
        
        if "200" in message or "304" in message:
            symbol = "✓"
            color = "\033[92m"  # Verde
        elif "404" in message:
            symbol = "✗"
            color = "\033[91m"  # Vermelho
        else:
            symbol = "●"
            color = "\033[94m"  # Azul
        
        reset = "\033[0m"
        print(f"{color}[{timestamp}] {symbol} {message}{reset}")

# Inicia servidor
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Lista arquivos HTML disponíveis
html_files = [f for f in os.listdir('.') if f.endswith('.html')]

print("\n" + "="*50)
print("🌐 SERVIDOR ALO TRÂNSITO")
print("="*50)
print(f"📂 Diretório: {os.getcwd()}")
print(f"🔗 URL: http://localhost:{PORT}")
print(f"🔗 URL externa: http://{os.getenv('COMPUTERNAME', 'localhost')}:{PORT}")

print("\n📄 PÁGINAS DISPONÍVEIS:")
for file in sorted(html_files):
    print(f"  • http://localhost:{PORT}/{file}")

print("\n" + "="*50)
print("🟢 Servidor rodando...")
print("⏹️  CTRL+C para parar")
print("="*50 + "\n")

try:
    server = HTTPServer(('0.0.0.0', PORT), AloTransitoHandler)
    server.serve_forever()
except KeyboardInterrupt:
    print("\n🛑 Servidor parado pelo usuário")
except Exception as e:
    print(f"\n❌ ERRO: {e}")