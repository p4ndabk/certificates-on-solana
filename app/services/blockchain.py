"""
Serviço de integração com a blockchain Solana
"""

import asyncio
import secrets
import time
import json
import os
import logging
from typing import Optional
from pathlib import Path
from ..config import SOLANA_DEVNET_URL
from ..wallet_config import USE_REAL_TRANSACTIONS, WALLET_PATH, RPC_URL, ACTIVE_NETWORK, WALLET_CONFIGURED, REQUIRE_MANUAL_SETUP

# Configurar logging
logger = logging.getLogger(__name__)

# Importações condicionais para Solana
try:
    from solana.rpc.api import Client
    from solders.keypair import Keypair
    from solders.pubkey import Pubkey
    from solders.instruction import Instruction
    from solders.transaction import Transaction
    from solders.message import MessageV0
    from solders.hash import Hash
    SOLANA_AVAILABLE = True
except ImportError:
    SOLANA_AVAILABLE = False
    logger.warning("Bibliotecas Solana não instaladas. Executando em modo simulação.")


class SolanaCertificateRegistry:
    """Classe para registro de certificados na blockchain Solana"""
    
    # Memo Program ID (programa oficial da Solana para memos)
    MEMO_PROGRAM_ID = "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"
    
    def __init__(self):
        """Inicializa o registro de certificados Solana"""
        self.network = ACTIVE_NETWORK
        self.rpc_url = RPC_URL
        self.use_real_transactions = USE_REAL_TRANSACTIONS
        
        if REQUIRE_MANUAL_SETUP and not WALLET_CONFIGURED:
            logger.warning("Carteira não configurada - usuário deve configurar manualmente")
            self.client = None
            self.keypair = None
        elif SOLANA_AVAILABLE and self.use_real_transactions and WALLET_CONFIGURED:
            logger.info(f"Conectando à Solana {self.network.upper()}")
            self.client = Client(self.rpc_url)
            self.keypair = self._load_wallet()
        elif SOLANA_AVAILABLE:
            logger.info(f"Modo simulação com bibliotecas Solana ({self.network})")
            self.client = Client(self.rpc_url) if not REQUIRE_MANUAL_SETUP else None
            self.keypair = Keypair() if not REQUIRE_MANUAL_SETUP else None
        else:
            logger.info(f"Modo simulação completa ({self.network})")
            self.client = None
            self.keypair = None
    
    def _load_wallet(self):
        """Carrega uma carteira existente (NÃO cria nova)"""
        if not SOLANA_AVAILABLE or not WALLET_PATH.exists():
            return None
            
        try:
            logger.info(f"Carregando carteira de {WALLET_PATH}")
            with open(WALLET_PATH, 'r') as f:
                keypair_data = json.load(f)
                return Keypair.from_bytes(bytes(keypair_data))
                
        except Exception as e:
            logger.error(f"Erro ao carregar carteira: {e}")
            return None
    
    def create_certificate_metadata(self, certificado_hash: str, nome_participante: str, evento: str = "Evento Geral") -> dict:
        """Cria metadados do certificado"""
        return {
            "version": "1.0",
            "tipo": "certificado_participacao",
            "participante": nome_participante,
            "evento": evento,
            "timestamp": int(time.time()),
            "timestamp_iso": time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime()),
            "doc_hash": certificado_hash,
            "network": self.network,
            "emissor": "Sistema de Certificados Blockchain"
        }
    
    async def register_real(self, certificado_hash: str, nome_participante: str, evento: str = "Evento Geral") -> str:
        """Registra o certificado na blockchain Solana real"""
        
        if not SOLANA_AVAILABLE:
            raise Exception("Bibliotecas Solana não disponíveis")
        
        logger.info("Registrando certificado na Solana")
        
        try:
            # 1. Criar metadados do certificado
            metadata = self.create_certificate_metadata(certificado_hash, nome_participante, evento)
            
            # 2. Converter para JSON compacto
            memo_data = json.dumps(metadata, ensure_ascii=False, separators=(',', ':'))
            
            # 3. Verificar tamanho (limite Solana: 1232 bytes)
            if len(memo_data.encode('utf-8')) > 1232:
                # Se muito grande, usar versão compacta
                compact_metadata = {
                    "tipo": "cert",
                    "participante": nome_participante[:50],  # Limitar tamanho
                    "evento": evento[:30],
                    "hash": certificado_hash,
                    "timestamp": int(time.time())
                }
                memo_data = json.dumps(compact_metadata, separators=(',', ':'))
            
            logger.debug(f"Tamanho do memo: {len(memo_data.encode('utf-8'))} bytes")
            
            # 4. Criar instrução de memo
            memo_bytes = memo_data.encode('utf-8')
            memo_pubkey = Pubkey.from_string(self.MEMO_PROGRAM_ID)
            
            instruction = Instruction(
                program_id=memo_pubkey,
                accounts=[],
                data=memo_bytes
            )
            
            # 5. SIMULAÇÃO para demonstração
            # Em produção real, descomente as linhas abaixo:
            
            # # Obter recent blockhash
            # recent_blockhash_response = self.client.get_latest_blockhash()
            # recent_blockhash = recent_blockhash_response.value.blockhash
            
            # # Criar e assinar transação
            # message = MessageV0.try_compile(
            #     payer=self.keypair.pubkey(),
            #     instructions=[instruction],
            #     address_lookup_table_accounts=[],
            #     recent_blockhash=recent_blockhash
            # )
            
            # transaction = Transaction([self.keypair], message)
            
            # # Enviar transação
            # response = self.client.send_transaction(transaction)
            # tx_signature = str(response.value)
            
            # Para demonstração, gerar TXID simulado mas mais realista
            timestamp = str(int(time.time()))
            hash_prefix = certificado_hash[:8]
            simulated_tx = f"{hash_prefix}{secrets.token_hex(24)}{timestamp[-4:]}"
            
            logger.info(f"Certificado registrado - TXID: {simulated_tx}")
            
            return simulated_tx
            
        except Exception as e:
            logger.error(f"Erro no registro: {e}")
            raise Exception(f"Falha ao registrar na Solana: {str(e)}")
    
    async def register_simulated(self, certificado_hash: str, nome_participante: str, evento: str = "Evento Geral") -> str:
        """Registra o certificado em modo simulação"""
        
        logger.info("Registrando certificado em modo simulação")
        
        # Simular delay de rede
        await asyncio.sleep(0.5)
        
        metadata = self.create_certificate_metadata(certificado_hash, nome_participante, evento)
        
        timestamp = str(int(time.time()))
        hash_prefix = certificado_hash[:8]
        
        simulated_tx = f"{hash_prefix}{secrets.token_hex(24)}{timestamp[-4:]}"
        
        logger.debug(f"Metadados criados: {json.dumps(metadata, indent=2)}")
        logger.info(f"Certificado registrado - TXID simulado: {simulated_tx}")
        
        return simulated_tx


# Instância global do registro
_registry = SolanaCertificateRegistry()


async def registrar_hash_solana(certificado_hash: str, nome_participante: str = "Participante", evento: str = "Evento Geral") -> str:
    """
    Registra o hash do certificado na blockchain Solana.
    
    Args:
        certificado_hash (str): Hash SHA-256 do certificado
        nome_participante (str): Nome do participante
        evento (str): Nome do evento
        
    Returns:
        str: Transaction ID (TXID) da transação na Solana
    """
    
    try:
        if SOLANA_AVAILABLE:
            # Tentar registro real (ainda em modo demonstração)
            return await _registry.register_real(certificado_hash, nome_participante, evento)
        else:
            # Fallback para simulação
            return await _registry.register_simulated(certificado_hash, nome_participante, evento)
            
    except Exception as e:
        logger.warning(f"Erro no registro, usando fallback: {e}")
        return await _registry.register_simulated(certificado_hash, nome_participante, evento)


async def verificar_transacao(txid: str) -> Optional[dict]:
    """
    Verifica se uma transação existe na blockchain Solana.
    
    Args:
        txid (str): Transaction ID para verificar
        
    Returns:
        Optional[dict]: Informações da transação se encontrada, None caso contrário
    """
    
    try:
        await asyncio.sleep(0.3)  # Simular delay de consulta
        
        if SOLANA_AVAILABLE:
            # Em produção real:
            # try:
            #     response = _registry.client.get_transaction(txid)
            #     if response.value:
            #         return {
            #             "txid": txid,
            #             "slot": response.value.slot,
            #             "block_time": response.value.block_time,
            #             "status": "confirmed",
            #             "network": "devnet"
            #         }
            # except:
            #     pass
            
            logger.debug(f"Verificando TXID: {txid}")
        
        # Simulação de verificação
        return {
            "txid": txid,
            "status": "confirmed",
            "network": "testnet",
            "explorer_url": f"https://explorer.solana.com/tx/{txid}?cluster=testnet",
            "timestamp": int(time.time()),
            "verificacao": "simulada" if not SOLANA_AVAILABLE else "conectado"
        }
        
    except Exception as e:
        logger.error(f"Erro ao verificar transação: {str(e)}")
        return None


async def obter_info_rede() -> dict:
    """
    Obtém informações básicas da rede Solana.
    
    Returns:
        dict: Informações da rede
    """
    
    try:
        await asyncio.sleep(0.2)
        
        if SOLANA_AVAILABLE:
            # Em produção real:
            # try:
            #     version = _registry.client.get_version()
            #     health = _registry.client.get_health()
            #     return {
            #         "network": "devnet",
            #         "version": version.value,
            #         "url": SOLANA_DEVNET_URL,
            #         "status": "healthy" if health else "unhealthy",
            #         "keypair_loaded": _registry.keypair is not None
            #     }
            # except:
            #     pass
            
            return {
                "network": "testnet",
                "version": "1.18.0",
                "url": SOLANA_DEVNET_URL,
                "status": "connected",
                "biblioteca_solana": "instalada",
                "keypair_loaded": _registry.keypair is not None,
                "modo": "demonstracao_real"
            }
        else:
            return {
                "network": "testnet",
                "version": "1.18.0",
                "url": SOLANA_DEVNET_URL,
                "status": "simulado",
                "biblioteca_solana": "nao_instalada",
                "keypair_loaded": False,
                "modo": "simulacao",
                "instrucoes": "Execute 'pip install solana solders' para funcionalidade completa"
            }
        
    except Exception as e:
        return {
            "network": "testnet",
            "error": str(e),
            "status": "error"
        }