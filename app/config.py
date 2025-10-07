"""
Configurações globais da aplicação de certificados na Solana
"""

import logging
import sys

# Configurações da Solana
# TESTNET (gratuito - para desenvolvimento)
SOLANA_TESTNET_URL = "https://api.testnet.solana.com"
# MAINNET (real - requer SOL)
SOLANA_MAINNET_URL = "https://api.mainnet-beta.solana.com"

# Escolher rede (mude para 'mainnet' para transações reais)
SOLANA_NETWORK = "testnet"  # Mude para "mainnet" quando quiser usar SOL real
SOLANA_DEVNET_URL = SOLANA_TESTNET_URL if SOLANA_NETWORK == "testnet" else SOLANA_MAINNET_URL

# Configurações do certificado
CERTIFICATE_TITLE = "Certificado de Participação"
CERTIFICATE_ISSUER = "Sistema de Certificados Blockchain"

# Configurações da aplicação
APP_NAME = "Certificados na Solana"

# Configuração de logging
def setup_logging():
    """Configura o sistema de logging da aplicação"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Reduzir verbosidade de bibliotecas externas
    logging.getLogger("solana").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

# Configurar logging quando o módulo for importado
setup_logging()
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Sistema de emissão de certificados autenticados na blockchain Solana"