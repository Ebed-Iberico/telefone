#!/usr/bin/env python3
"""
SERVIDOR HTTP para Sistema Alo Trânsito
Servir arquivos HTML na rede local
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket
import os
import sys
import urllib.parse

class CORSHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Handler com CORS e tratamento especial para arquivos"""
    
    def do_GET(self):
        # Analisar o caminho da URL
        parsed_path = urllib.parse.urlparse(self.path)
        request_path = parsed_path.path
        
        # Se acessar a raiz, redireciona para index.html
        if request_path == '/' or request_path == '':
            self.path = '/index.html'
            print(f"[INFO] Acesso à raiz -> redirecionando para index.html")
        
        # Verificar se o arquivo existe
        file_path = self.translate_path(self.path)
        
        # Se não existir, tentar adicionar .html
        if not os.path.exists(file_path) and not self.path.endswith('.html'):
            if os.path.exists(file_path + '.html'):
                self.path += '.html'
                file_path += '.html'
                print(f"[INFO] Arquivo não encontrado -> tentando {self.path}")
        
        # Se ainda não existir, mostrar 404 personalizado
        if not os.path.exists(file_path):
            print(f"[ERRO] Arquivo não encontrado: {self.path}")
            self.send_error(404, f"Arquivo não encontrado: {self.path}")
            return
        
        print(f"[OK] Servindo arquivo: {self.path}")
        return super().do_GET()
    
    def end_headers(self):
        # Adiciona headers CORS para desenvolvimento
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        """Personaliza logs do servidor"""
        # Não mostrar logs de requisições normais (opcional)
        # Para ver todos os logs, remova ou modifique esta função
        pass

def get_local_ip():
    """Obtém o IP local da máquina"""
    try:
        # Método 1: Usando socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        try:
            # Método 2: Usando hostname
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            if ip.startswith('127.'):
                return "127.0.0.1"
            return ip
        except:
            return "127.0.0.1"

def show_banner(ip, port):
    """Mostra banner informativo"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("\n" + "="*70)
    print("🌐 SERVIDOR HTTP - SISTEMA ALO TRÂNSITO")
    print("="*70)
    print(f"\n📁 Diretório atual: {os.getcwd()}")
    print(f"🚪 Porta: {port}")
    print(f"🏠 Host: 0.0.0.0 (acessível na rede)")
    print("\n" + "-"*70)

def list_html_files():
    """Lista todos os arquivos HTML na pasta"""
    html_files = []
    for file in os.listdir('.'):
        if file.lower().endswith('.html'):
            html_files.append(file)
    return html_files

def check_and_rename_html():
    """Verifica e renomeia arquivos HTML se necessário"""
    html_files = list_html_files()
    
    if not html_files:
        print("❌ ERRO CRÍTICO: Nenhum arquivo HTML encontrado!")
        print("\n📁 Conteúdo da pasta:")
        for item in os.listdir('.'):
            print(f"   📄 {item}")
        return False
    
    # Verifica se existe index.html
    if 'index.html' in html_files:
        return True
    
    # Se não tem index.html, oferece para renomear
    print(f"\n⚠️  Arquivo 'index.html' não encontrado!")
    print(f"📄 Arquivos HTML disponíveis:")
    for i, html in enumerate(html_files, 1):
        print(f"   {i}. {html}")
    
    try:
        choice = input(f"\n👉 Renomear '{html_files[0]}' para 'index.html'? (s/n): ")
        if choice.lower() == 's':
            os.rename(html_files[0], 'index.html')
            print(f"✅ Renomeado: {html_files[0]} → index.html")
            return True
        else:
            print(f"\nℹ️  Acesse os arquivos diretamente:")
            return False
    except:
        return False

def main():
    """Função principal do servidor"""
    PORT = int(os.environ.get("PORT", 8000))
    HOST = "0.0.0.0"  # CRÍTICO: Permite acesso na rede
    
    # Muda para diretório do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Verifica arquivos HTML
    if not check_and_rename_html():
        print("\n❌ Não é possível iniciar o servidor sem arquivos HTML.")
        input("Pressione Enter para sair...")
        sys.exit(1)
    
    # Obtém IP local
    local_ip = get_local_ip()
    
    # Mostra banner
    show_banner(local_ip, PORT)
    
    # Lista arquivos disponíveis
    html_files = list_html_files()
    
    print(f"\n✅ SERVIDOR INICIADO COM SUCESSO!")
    print("\n🔗 URLS DE ACESSO:")
    print(f"   📱 NO CELULAR (na mesma rede Wi-Fi):")
    print(f"      → http://{local_ip}:{PORT}/")
    print(f"   💻 NO COMPUTADOR:")
    print(f"      → http://localhost:{PORT}/")
    print(f"      → http://127.0.0.1:{PORT}/")
    
    print(f"\n📄 ARQUIVOS DISPONÍVEIS:")
    for html_file in html_files:
        if html_file == 'index.html':
            print(f"   ★ {html_file} (página principal)")
        else:
            print(f"   📄 {html_file}")
    
    print(f"\n🔧 CONFIGURAÇÃO DA API:")
    print(f"   No seu código HTML, certifique-se que:")
    print(f"   const API_BASE_URL = 'http://{local_ip}:3000'")
    print(f"   (ou o IP correto da sua API)")
    
    print(f"\n⚠️  IMPORTANTE:")
    print(f"   1. Celular e computador DEVEM estar na MESMA rede Wi-Fi")
    print(f"   2. Firewall pode bloquear - verifique configurações")
    print(f"   3. API deve estar rodando no IP correto")
    
    print(f"\n🔄 LOGS DO SERVIDOR:")
    print(f"   [As requisições serão mostradas aqui]")
    print("\n" + "="*70)
    print("⏹️  Para parar o servidor: Pressione CTRL+C")
    print("="*70 + "\n")
    
    # Configura e inicia servidor
    try:
        server_address = (HOST, PORT)
        httpd = HTTPServer(server_address, CORSHTTPRequestHandler)
        
        # Habilitar reutilização de porta
        httpd.allow_reuse_address = True
        
        print(f"🔄 Aguardando conexões na porta {PORT}...")
        httpd.serve_forever()
        
    except OSError as e:
        if e.errno == 98 or "Address already in use" in str(e):
            print(f"\n❌ ERRO: Porta {PORT} já está em uso!")
            print(f"   Soluções:")
            print(f"   1. Execute: netstat -ano | findstr :{PORT} (Windows)")
            print(f"   2. Execute: lsof -i :{PORT} (Mac/Linux)")
            print(f"   3. Mude a porta no código: PORT = 8001")
        else:
            print(f"\n❌ ERRO ao iniciar servidor: {e}")
        input("\nPressione Enter para sair...")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print(f"\n\n🛑 Servidor interrompido pelo usuário")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ ERRO inesperado: {e}")
        input("\nPressione Enter para sair...")
        sys.exit(1)

if __name__ == "__main__":
    main()