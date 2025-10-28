"""
Configurações centralizadas da aplicação
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Configuração de diretórios
BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar .env
load_dotenv(BASE_DIR / '.env')

# Informações da Aplicação
APP_NAME = "Certificates on Solana"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistema de Registro de Certificados na Blockchain Solana"

# Configuração Solana
SOLANA_NETWORK = os.getenv("SOLANA_NETWORK", "devnet")
SOLANA_URL = os.getenv("SOLANA_URL", "https://api.devnet.solana.com")

# Configuração da carteira
SOLANA_WALLET_PATH = BASE_DIR / os.getenv("SOLANA_WALLET_PATH", "wallet/certificates-wallet.json")
SOLANA_WALLET_PATH.parent.mkdir(parents=True, exist_ok=True)

# Log simplificado
print(f"\n═══ Configuração Solana ═══")
print(f"Network: {SOLANA_NETWORK}")
print(f"URL: {SOLANA_URL}")
print(f"Wallet: {SOLANA_WALLET_PATH}")
print(f"Wallet exists: {SOLANA_WALLET_PATH.exists()}\n")