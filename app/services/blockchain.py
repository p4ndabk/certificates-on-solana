"""Serviço de integração com a blockchain Solana"""

import asyncio
import secrets
import time
import json
import logging
from typing import Optional
from ..config import SOLANA_DEVNET_URL
from ..wallet_config import (
    USE_REAL_TRANSACTIONS, WALLET_PATH, RPC_URL, ACTIVE_NETWORK, 
    WALLET_CONFIGURED, REQUIRE_MANUAL_SETUP
)

logger = logging.getLogger(__name__)

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
        if REQUIRE_MANUAL_SETUP and not WALLET_CONFIGURED:
            logger.warning("Carteira não configurada - usuário deve configurar manualmente")
            return
            
        if not SOLANA_AVAILABLE:
            logger.info(f"Modo simulação completa ({self.network})")
            return
            
        logger.info(f"Conectando à Solana {self.network.upper()}")
        self.client = Client(self.rpc_url)
        
        if WALLET_CONFIGURED and WALLET_PATH.exists():
            self.keypair = self._load_wallet()
        else:
            self.keypair = Keypair()
            logger.info(f"Criando carteira temporária: {str(self.keypair.pubkey())}")
    
    def _load_wallet(self):
        """Carrega carteira existente do arquivo"""
        try:
            logger.info(f"Carregando carteira de {WALLET_PATH}")
            with open(WALLET_PATH, 'r') as f:
                keypair_data = json.load(f)
                return Keypair.from_bytes(bytes(keypair_data))
        except Exception as e:
            logger.error(f"Erro ao carregar carteira: {e}")
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
            "code": codigo_certificado,
            "name": self.mask_name(nome_participante),
            "email": self.mask_email(email_participante),
            "evento": evento,
            "timestamp": int(time.time()),
            "doc_hash": certificado_hash,
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
            
            # Envia transação
            logger.info(f"Enviando transação para Solana {self.network}...")
            response = self.client.send_transaction(transaction)
            tx_signature = str(response.value)
            
            logger.info(f"Certificado registrado - TXID: {tx_signature}")
            return tx_signature
            
        except Exception as e:
            logger.error(f"Erro no registro: {e}")

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
        
        if SOLANA_AVAILABLE:
            return {
                **base_info,
                "status": "connected",
                "biblioteca_solana": "instalada",
                "modo": "blockchain_real_gratuita",
                "airdrop_disponivel": _registry.network == "devnet"
            }
        else:
            return {
                **base_info,
                "status": "simulado",
                "biblioteca_solana": "nao_instalada",
                "modo": "simulacao",
                "instrucoes": "Execute 'pip install solana solders' para registro real GRATUITO na devnet"
            }
        
    except Exception as e:
        return {
            "network": "testnet",
            "error": str(e),
            "status": "error"
        }


# Compatibilidade com código existente
BlockchainService = SolanaCertificateRegistry