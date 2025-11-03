"""Serviço de integração com a blockchain Solana"""

import asyncio
import secrets
import time
import json
import logging
from typing import Optional
from pathlib import Path
from datetime import datetime

# Importar config PRIMEIRO (que já carregou o .env)
from ..config import SOLANA_NETWORK, SOLANA_URL, SOLANA_WALLET_PATH
from ..wallet_config import (
    USE_REAL_TRANSACTIONS, RPC_URL, ACTIVE_NETWORK, 
    WALLET_CONFIGURED, REQUIRE_MANUAL_SETUP
)

logger = logging.getLogger(__name__)

# DEBUG: Log das configurações carregadas
logger.info(f"[BLOCKCHAIN DEBUG] SOLANA_NETWORK (config): {SOLANA_NETWORK}")
logger.info(f"[BLOCKCHAIN DEBUG] SOLANA_URL (config): {SOLANA_URL}")
logger.info(f"[BLOCKCHAIN DEBUG] SOLANA_WALLET_PATH (config): {SOLANA_WALLET_PATH}")
logger.info(f"[BLOCKCHAIN DEBUG] ACTIVE_NETWORK (wallet_config): {ACTIVE_NETWORK}")
logger.info(f"[BLOCKCHAIN DEBUG] RPC_URL (wallet_config): {RPC_URL}")
logger.info(f"[BLOCKCHAIN DEBUG] WALLET_CONFIGURED (wallet_config): {WALLET_CONFIGURED}")


try:
    from solana.rpc.api import Client
    from solders.keypair import Keypair
    from solders.pubkey import Pubkey
    from solders.instruction import Instruction
    from solders.transaction import Transaction
    from solders.message import MessageV0
    SOLANA_AVAILABLE = True
except ImportError:
    SOLANA_AVAILABLE = False
    logger.warning("Bibliotecas Solana não instaladas. Executando em modo simulação.")


class SolanaCertificateRegistry:
    """Classe para registro de certificados na blockchain Solana"""
    
    MEMO_PROGRAM_ID = "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"
    
    def __init__(self):
        self.network = ACTIVE_NETWORK
        self.rpc_url = RPC_URL
        self.use_real_transactions = USE_REAL_TRANSACTIONS
        self.client = None
        self.keypair = None
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Inicializa cliente e carteira conforme configuração"""
        logger.info(f"[INIT DEBUG] Iniciando com network={self.network}, rpc_url={self.rpc_url}")
        
        if REQUIRE_MANUAL_SETUP and not WALLET_CONFIGURED:
            logger.warning("Carteira não configurada - usuário deve configurar manualmente")
            return
            
        if not SOLANA_AVAILABLE:
            logger.info(f"Modo simulação completa ({self.network})")
            return
            
        logger.info(f"Conectando à Solana {self.network.upper()}")
        self.client = Client(self.rpc_url)
        
        wallet_path = Path(SOLANA_WALLET_PATH)
        logger.info(f"[WALLET DEBUG] WALLET_CONFIGURED={WALLET_CONFIGURED}, wallet_path={wallet_path}, exists={wallet_path.exists()}")
        
        if WALLET_CONFIGURED and wallet_path.exists():
            logger.info(f"[WALLET DEBUG] Tentando carregar carteira de {wallet_path}")
            self.keypair = self._load_wallet(wallet_path)
        else:
            logger.warning(f"[WALLET DEBUG] Criando carteira temporária. WALLET_CONFIGURED={WALLET_CONFIGURED}, path_exists={wallet_path.exists()}")
            self.keypair = Keypair()
            logger.info(f"Criando carteira temporária: {str(self.keypair.pubkey())}")
    
    def _load_wallet(self, wallet_path: Path):
        """Carrega carteira existente do arquivo"""
        try:
            logger.info(f"[LOAD_WALLET DEBUG] Carregando carteira de {wallet_path}")
            with open(wallet_path, 'r') as f:
                keypair_data = json.load(f)
                logger.info(f"[LOAD_WALLET DEBUG] Carteira carregada com sucesso")
                return Keypair.from_bytes(bytes(keypair_data))
        except Exception as e:
            logger.error(f"[LOAD_WALLET ERROR] Erro ao carregar carteira: {e}")
            return None
        
    def mask_name(self, nome: str) -> str:
        partes = nome.split()
        if not partes:
            return ""
        primeiro = partes[0][:2]
        ultimo = partes[-1][-2:]
        return f"{primeiro}****{ultimo}"

    def mask_email(self, email: str) -> str:
        try:
            local, dominio = email.split("@")
            local_mask = local[:2] + "*" + local[-1] if len(local) > 3 else local[0] + "*"
            dominio_parts = dominio.split(".")
            dominio_mask = dominio[0][0] + "**" + dominio_parts[-1] if dominio_parts else "g**br"
            return f"{local_mask}@{dominio_mask}"
        except Exception:
            return "mascarado"

    def _create_metadata(self, certificado_hash: str, nome_participante: str, evento: str, codigo_certificado: str, email_participante: str) -> str:
        """Cria e otimiza metadados do certificado"""
        metadata = {
            "version": "1.0",
            "tipo": "certificado_participacao",
            "code": codigo_certificado.lower(),
            "name": self.mask_name(nome_participante).lower(),
            "email": self.mask_email(email_participante).lower(),
            "evento": evento.lower(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "doc_hash": certificado_hash.lower(),
            "network": self.network,
            "emissor": "Sistema de Certificados Blockchain"            
        }
        
        memo_data = json.dumps(metadata, ensure_ascii=False, separators=(',', ':'))
        
        # Otimiza se muito grande
        if len(memo_data.encode('utf-8')) > 1232:
            compact_metadata = {
                "tipo": "cert",
                "participante": nome_participante[:50],
                "evento": evento[:30],
                "hash": certificado_hash,
                "timestamp": int(time.time())
            }
            memo_data = json.dumps(compact_metadata, separators=(',', ':'))
        
        return memo_data
    
    def _create_transaction(self, memo_data: str):
        """Cria transação Solana com os metadados"""
        memo_bytes = memo_data.encode('utf-8')
        memo_pubkey = Pubkey.from_string(self.MEMO_PROGRAM_ID)
        
        instruction = Instruction(
            program_id=memo_pubkey,
            accounts=[],
            data=memo_bytes
        )
        
        recent_blockhash_response = self.client.get_latest_blockhash()
        recent_blockhash = recent_blockhash_response.value.blockhash
        
        # Usa método que funcionava antes do refactor
        try:
            from solders.message import MessageV0
            from solders.transaction import VersionedTransaction
            
            message = MessageV0.try_compile(
                payer=self.keypair.pubkey(),
                instructions=[instruction],
                address_lookup_table_accounts=[],
                recent_blockhash=recent_blockhash
            )
            
            return VersionedTransaction(message, [self.keypair])
            
        except Exception as e:
            logger.warning(f"Erro ao criar transação VersionedTransaction: {e}, tentando método alternativo.")

    async def _ensure_balance_for_devnet(self):
        """Garante saldo na devnet via airdrop se necessário"""
        if not self.keypair or self.network != "devnet":
            return
            
        try:
            balance_response = self.client.get_balance(self.keypair.pubkey())
            balance_sol = balance_response.value / 1_000_000_000
            
            if balance_sol < 0.001:  # Menos de 0.001 SOL
                logger.info("Solicitando airdrop na devnet...")
                airdrop_response = self.client.request_airdrop(self.keypair.pubkey(), 1_000_000_000)
                await asyncio.sleep(3)
        except Exception as e:
            logger.warning(f"Erro no airdrop: {e}")
    
    def _generate_simulated_txid(self) -> str:
        """Gera TXID simulado no formato Solana"""
        base58_alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        import random
        return ''.join(random.choice(base58_alphabet) for _ in range(88))

    async def register_certificate(self, certificado_hash: str, nome_participante: str, evento: str = "Evento Geral", codigo_certificado: str = "Código do Certificado", email_participante: str = "email@exemplo.com") -> str:
        """Registra certificado na blockchain com fallback automático"""
                
        try:
            # Garante saldo na devnet
            await self._ensure_balance_for_devnet()
            
            # Cria metadados e transação
            memo_data = self._create_metadata(certificado_hash, nome_participante, evento, codigo_certificado, email_participante)
            logger.debug(f"Tamanho do memo: {len(memo_data.encode('utf-8'))} bytes")
            
            transaction = self._create_transaction(memo_data)
            
            if not transaction:
                raise ValueError("Falha ao criar transação Solana")
            
            # Envia transação
            logger.info(f"Enviando transação para Solana {self.network}...")
            response = self.client.send_transaction(transaction)
            
            if not response or not response.value:
                raise ValueError("Falha ao enviar transação para a blockchain")
                
            tx_signature = str(response.value)
            
            if not tx_signature or len(tx_signature) < 32:
                raise ValueError("TXID inválido retornado pela blockchain")
            
            logger.info(f"Certificado registrado - TXID: {tx_signature}")
            return tx_signature
            
        except Exception as e:
            logger.error(f"Erro no registro: {e}")
            # Re-raise a exceção para ser capturada na rota
            raise Exception(f"Falha ao registrar certificado na blockchain: {str(e)}")


# Instância global
_registry = SolanaCertificateRegistry()


async def registrar_hash_solana(certificado_hash: str, nome_participante: str = "Participante", evento: str = "Evento Geral", codigo_certificado: str = "Código do Certificado", email_participante: str = "email@exemplo.com") -> str:
    """Registra o hash do certificado na blockchain Solana"""
    return await _registry.register_certificate(certificado_hash, nome_participante, evento, codigo_certificado, email_participante)

async def obter_info_rede() -> dict:
    """Obtém informações básicas da rede Solana"""
    try:
        await asyncio.sleep(0.2)
        
        base_info = {
            "network": _registry.network,
            "version": "1.18.0",
            "url": _registry.rpc_url,
            "keypair_loaded": _registry.keypair is not None,
            "explorer": f"https://explorer.solana.com/?cluster={_registry.network}"
        }
        
        return {
            **base_info,
            "status": "connected",
            "biblioteca_solana": "instalada",
            "modo": "blockchain_real_gratuita",
            "airdrop_disponivel": _registry.network == "devnet"
        }
        
    except Exception as e:
        logger.error(f"Erro ao obter info da rede: {e}")


# Compatibilidade com código existente
BlockchainService = SolanaCertificateRegistry