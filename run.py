#!/usr/bin/env python3
"""
Script de inicialização do servidor de Certificados na Solana
Executa a partir da raiz do projeto
"""

import os
from pathlib import Path

def load_env_file():
    """Carrega variáveis do arquivo .env"""
    env_file = Path(__file__).parent / ".env"
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

if __name__ == "__main__":
    import uvicorn
    
    # Carregar variáveis do .env
    load_env_file()
    
    # Configurações do servidor
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    log_level = os.getenv('LOG_LEVEL', 'info')
    reload = os.getenv('RELOAD', 'true').lower() == 'true'
    
    print("Iniciando Certificados na Solana...")
    print(f"Documentação: http://localhost:{port}/docs")
    print(f"Interface: http://localhost:{port}")
    print("Solana Explorer: https://explorer.solana.com/?cluster=testnet")
    print("=" * 50)
    
    # Executar servidor
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload,
        log_level=log_level
    )