"""
Configurações centralizadas da aplicação
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
env_file = BASE_DIR / '.env'

if env_file.exists():
    load_dotenv(env_file)
    print(f".env carregado de: {env_file}")
else:
    print(f".env não encontrado em: {env_file}")

# Criar diretório de wallet
WALLET_DIR = BASE_DIR / "wallet"
WALLET_DIR.mkdir(exist_ok=True)

# Informações da Aplicação
APP_NAME = "Certificates on Solana"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistema de Registro de Certificados na Blockchain Solana"

# Configuração Solana - Lendo do .env
SOLANA_NETWORK = os.getenv("SOLANA_NETWORK", "devnet")
SOLANA_URL = os.getenv("SOLANA_URL", "https://api.devnet.solana.com")
SOLANA_WALLET_PATH = Path(os.getenv("SOLANA_WALLET_PATH", str(WALLET_DIR / "certificates_wallet.json")))

print(f"\n═══════════════════════════════════════════════════════")
print(f"✓ SOLANA_NETWORK: {SOLANA_NETWORK}")
print(f"✓ SOLANA_URL: {SOLANA_URL}")
print(f"✓ SOLANA_WALLET_PATH: {SOLANA_WALLET_PATH}")
print(f"═══════════════════════════════════════════════════════\n")