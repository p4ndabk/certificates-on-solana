"""
Configurações de carteira e blockchain
"""

from pathlib import Path

# Importar DEPOIS que config.py carregou o .env
from .config import (
    SOLANA_NETWORK,
    SOLANA_URL,
    SOLANA_WALLET_PATH
)

# Mapeamento direto
ACTIVE_NETWORK = SOLANA_NETWORK
RPC_URL = SOLANA_URL
WALLET_PATH = SOLANA_WALLET_PATH

# Configurações padrão
USE_REAL_TRANSACTIONS = True
WALLET_CONFIGURED = True
REQUIRE_MANUAL_SETUP = True