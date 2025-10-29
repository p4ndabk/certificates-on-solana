"""
Rotas para registro de certificados na blockchain
"""

import json
import uuid
import urllib.request
import urllib.parse
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path

from ..services.hashing import gerar_hash_texto
from ..services.blockchain import registrar_hash_solana, obter_info_rede

# Importar config APÓS ela ter carregado o .env
from ..config import SOLANA_NETWORK, SOLANA_URL, SOLANA_WALLET_PATH
from ..wallet_config import USE_REAL_TRANSACTIONS, ACTIVE_NETWORK, WALLET_CONFIGURED

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/certificados", tags=["certificados"])


class CertificadoRequest(BaseModel):
    name: str
    event: str
    email: str
    certificate_code: str


class CertificadoVerificacao(BaseModel):
    event: str
    uuid: str
    name: str
    email: str
    certificate_code: str
    time: str


@router.post("/register")
async def registrar_certificado(request: CertificadoRequest):
    """
    Registra um certificado na blockchain Solana usando JSON canonizado.

    Args:
        request (CertificadoRequest): Dados do certificado

    Returns:
        dict: Dados do certificado registrado com TXID da blockchain
    """

    try:
        certificate_uuid = str(uuid.uuid4())
        current_time = datetime.now()

        certificate_data = {
            "event": request.event.lower(),
            "uuid": certificate_uuid.lower(),
            "name": request.name.lower(),
            "email": request.email.lower(),
            "certificate_code": request.certificate_code.lower(),
            "time": current_time.strftime("%Y-%m-%d %H:%M:%S")
        }

        json_canonico = json.dumps(certificate_data, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
        certificado_hash = gerar_hash_texto(json_canonico)

        txid_solana = await registrar_hash_solana(certificado_hash, request.name, request.event, request.certificate_code, request.email)
        print(f"Certificado hash: {certificado_hash}")
        
        return {
            "status": "sucesso",
            "certificado": {
                "event": request.event,
                "name": request.name,
                "email": request.email,
                "uuid": certificate_uuid,
                "time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "json_canonico": certificate_data,
                "hash_sha256": certificado_hash,
                "txid_solana": txid_solana,
                "network": SOLANA_NETWORK,
                "timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
                "timestamp_unix": int(current_time.timestamp())
            },
            "blockchain": {
                "rede": f"Solana {SOLANA_NETWORK.title()}",
                "explorer_url": f"https://explorer.solana.com/tx/{txid_solana}?cluster={SOLANA_NETWORK}",
                "verificacao_url": f"http://localhost:8000/certificados/verify/{txid_solana}",
                "memo_program": "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"
            },
            "validacao": {
                "como_validar": "Recrie o JSON canonizado e compare o hash SHA-256",
                "json_canonico_string": json_canonico,
                "hash_esperado": certificado_hash,
                "comando_validacao": f"printf '{json_canonico}' | shasum -a 256"
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao registrar certificado: {str(e)}"
        )


@router.post("/verify/{txid}")
async def verificar_certificado(txid: str, certificado_data: CertificadoVerificacao):
    """
    Verifica um certificado na blockchain Solana comparando o hash.

    Args:
        txid (str): Transaction ID da Solana
        certificado_data (CertificadoVerificacao): Dados do certificado para validação

    Returns:
        dict: Status da verificação com comparação de hash
    """

    try:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [
                txid,
                {"encoding": "json", "maxSupportedTransactionVersion": 0}
            ]
        }

        json_data = json.dumps(payload).encode('utf-8')

        req = urllib.request.Request(
            SOLANA_URL,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )

        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))

        if "result" in data and data["result"]:
            transaction_result = data["result"]

            memo_data_extraido = {} 
            blockchain_doc_hash = None
            if "meta" in transaction_result and "logMessages" in transaction_result["meta"]:
                for log_message in transaction_result["meta"]["logMessages"]:
                    if "Program log: Memo" in log_message and "doc_hash" in log_message:
                        try:
                            start = log_message.find('"{')
                            end = log_message.rfind('}"') + 2
                            if start != -1 and end != -1:
                                memo_json_str = log_message[start+1:end-1]
                                memo_json_str = memo_json_str.replace('\\"', '"')
                                memo_data = json.loads(memo_json_str)
                                blockchain_doc_hash = memo_data.get("doc_hash")

                                # extact memo metadata
                                metadata_memo = {
                                    "version": memo_data.get("version"),
                                    "tipo": memo_data.get("tipo"),
                                    "code": memo_data.get("code"),
                                    "name": memo_data.get("name"),
                                    "email": memo_data.get("email"),
                                    "evento": memo_data.get("evento"),
                                    "timestamp": memo_data.get("timestamp"),
                                    "doc_hash": memo_data.get("doc_hash"),
                                    "network": memo_data.get("network"),
                                    "emissor": memo_data.get("emissor")
                                }
                                
                                break
                        except (json.JSONDecodeError, KeyError):
                            continue
                        
            # Generate hash from provided certificate data
            certificate_dict = {
                "event": certificado_data.event.lower(),
                "uuid": certificado_data.uuid.lower(),
                "name": certificado_data.name.lower(),
                "email": certificado_data.email.lower(),
                "certificate_code": certificado_data.certificate_code.lower(),
                "time": certificado_data.time
            }

            json_canonico = json.dumps(certificate_dict, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
            generated_hash = gerar_hash_texto(json_canonico)

            hash_valido = blockchain_doc_hash == generated_hash

            return {
                "status": "encontrado",
                "txid": txid,
                "rede": f"Solana {SOLANA_NETWORK.title()}",
                "explorer_url": f"https://explorer.solana.com/tx/{txid}?cluster={SOLANA_NETWORK}",
                "metadata_memo": metadata_memo,
                "validacao": {
                    "hash_blockchain": blockchain_doc_hash,
                    "hash_gerado": generated_hash,
                    "hash_valido": hash_valido,
                    "json_canonico_usado": json_canonico,
                    "certificado_autentico": hash_valido
                },
                "certificado_dados": certificate_dict
            }
        else:
            return {
                "status": "nao_encontrado",
                "mensagem": "Transação não encontrada na blockchain",
                "txid": txid,
                "error": data.get("error", "Transação não existe")
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao verificar certificado: {str(e)}"
        )


@router.get("/wallet-info")
async def obter_informacoes_carteira():
    """
    Obtém informações sobre a carteira e saldo SOL.

    Returns:
        dict: Informações da carteira e saldo
    """

    try:
        from ..services.blockchain import _registry
        
        logger.info(f"[WALLET-INFO DEBUG] SOLANA_WALLET_PATH na rota: {SOLANA_WALLET_PATH}")
        logger.info(f"[WALLET-INFO DEBUG] WALLET_CONFIGURED: {WALLET_CONFIGURED}")
        logger.info(f"[WALLET-INFO DEBUG] _registry.keypair: {_registry.keypair}")

        if not WALLET_CONFIGURED:
            logger.warning(f"[WALLET-INFO DEBUG] Carteira não configurada")
            return {
                "status": "carteira_nao_configurada",
                "mensagem": "Você precisa configurar sua própria carteira",
                "instrucoes": {
                    "passo_1": "Crie sua carteira Solana usando: solana-keygen new",
                    "passo_2": f"Salve o arquivo JSON em: {SOLANA_WALLET_PATH}",
                    "passo_3": "Configure WALLET_CONFIGURED = True",
                    "passo_4": "Transfira SOL para sua carteira",
                    "alternativa": "Ou use o sistema em modo simulação (padrão atual)"
                },
                "configuracao_atual": {
                    "carteira_configurada": False,
                    "transacoes_reais": USE_REAL_TRANSACTIONS,
                    "rede": ACTIVE_NETWORK,
                    "modo": "simulacao_completa",
                    "wallet_path_esperado": str(SOLANA_WALLET_PATH)
                }
            }

        if not _registry.keypair:
            logger.error(f"[WALLET-INFO DEBUG] Carteira configurada mas keypair não carregado")
            return {
                "status": "erro",
                "mensagem": "Carteira configurada mas não carregada corretamente"
            }

        wallet_address = str(_registry.keypair.pubkey())
        logger.info(f"[WALLET-INFO DEBUG] Carteira carregada: {wallet_address}")

        # Get balance using direct RPC call
        balance_sol = "simulacao"
        balance_lamports = "N/A"
        
        try:
            print(f"Consultando saldo para: {wallet_address}")
            
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getBalance",
                "params": [wallet_address]
            }
            
            json_data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                SOLANA_URL,
                data=json_data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                balance_data = json.loads(response.read().decode('utf-8'))
            
            if "result" in balance_data and "value" in balance_data["result"]:
                balance_lamports = balance_data["result"]["value"]
                balance_sol = balance_lamports / 1_000_000_000
                print(f"Balance: {balance_lamports} lamports = {balance_sol} SOL")
            else:
                balance_sol = "erro_rpc_response"
                balance_lamports = "erro_rpc_response"
                
        except Exception as e:
            print(f"Erro ao consultar saldo via RPC: {str(e)}")
            balance_sol = f"erro_rpc: {str(e)}"
            balance_lamports = f"erro_rpc: {str(e)}"

        return {
            "status": "sucesso",
            "carteira": {
                "endereco": wallet_address,
                "saldo_sol": balance_sol,
                "saldo_lamports": balance_lamports,
                "rede": ACTIVE_NETWORK,
                "transacoes_reais": USE_REAL_TRANSACTIONS,
                "modo": "real" if USE_REAL_TRANSACTIONS else "simulacao",
                "debug_info": {
                    "wallet_configured": WALLET_CONFIGURED,
                    "use_real_transactions": USE_REAL_TRANSACTIONS,
                    "active_network": ACTIVE_NETWORK,
                    "wallet_path": str(SOLANA_WALLET_PATH),
                    "wallet_path_exists": Path(SOLANA_WALLET_PATH).exists()
                }
            },
            "custos": {
                "transacao_memo": "~0.000005 SOL",
                "saldo_recomendado": "0.01 SOL"
            },
            "instrucoes": {
                "obter_sol": f"Transfira SOL para: {wallet_address}" if USE_REAL_TRANSACTIONS else "Configure sua carteira primeiro"
            }
        }

    except Exception as e:
        logger.error(f"[WALLET-INFO ERROR] {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter informações da carteira: {str(e)}"
        )


@router.get("/info-rede")
async def obter_informacoes_rede():
    """
    Obtém informações sobre o status da rede Solana.

    Returns:
        dict: Informações da rede Solana
    """

    try:
        info_rede = await obter_info_rede()
        return {
            "status": "sucesso",
            "rede": info_rede
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao obter informações da rede: {str(e)}"
        )