# Configuração de Carteira Solana Real
# IMPORTANTE: O usuário deve configurar sua própria carteira!

import os
from pathlib import Path

# Caminho para arquivo de carteira (dentro do projeto)
PROJECT_ROOT = Path(__file__).parent.parent  # Vai para a raiz do projeto
WALLET_PATH = PROJECT_ROOT / "wallet" / "certificates-wallet.json"

# Configurações de segurança
USE_REAL_TRANSACTIONS = False  # Usuário deve ativar manualmente
MINIMUM_SOL_BALANCE = 0.01     # Saldo mínimo em SOL para operar

# URLs de rede
NETWORKS = {
    "testnet": "https://api.testnet.solana.com",
    "mainnet": "https://api.mainnet-beta.solana.com", 
    "devnet": "https://api.devnet.solana.com"
}

# Configuração ativa
ACTIVE_NETWORK = "testnet"  # Usuário pode mudar para "mainnet"
RPC_URL = NETWORKS[ACTIVE_NETWORK]

# Custos aproximados (em SOL)
TRANSACTION_COSTS = {
    "memo_transaction": 0.000005,  # ~0.000005 SOL por transação de memo
    "recommended_balance": 0.01    # Saldo recomendado para várias transações
}

# Configuração de carteira - USUÁRIO DEVE CONFIGURAR
WALLET_CONFIGURED = WALLET_PATH.exists()  # Verifica se usuário já configurou
REQUIRE_MANUAL_SETUP = True  # Força setup manual pelo usuário