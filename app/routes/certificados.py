"""
Rotas para registro de certificados na blockchain
"""

import json
import uuid
import urllib.request
import urllib.parse
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime

from ..services.hashing import gerar_hash_texto
from ..services.blockchain import registrar_hash_solana, verificar_transacao, obter_info_rede

router = APIRouter(prefix="/certificados", tags=["certificados"])


class CertificadoRequest(BaseModel):
    name: str
    event: str
    document: str  # CPF ou documento de identificação
    duration_hours: int  # Horas de duração do evento/curso


class CertificadoVerificacao(BaseModel):
    event: str
    uuid: str
    name: str
    document: str
    duration_hours: int
    time: str


@router.post("/registrar")
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
            "event": request.event,
            "uuid": certificate_uuid,
            "name": request.name,
            "document": request.document,
            "duration_hours": request.duration_hours,
            "time": current_time.isoformat()
        }

        json_canonico = json.dumps(certificate_data, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
        certificado_hash = gerar_hash_texto(json_canonico)

        txid_solana = await registrar_hash_solana(certificado_hash, request.name, request.event)
        print(f"Certificado hash: {certificado_hash}")
        return {
            "status": "sucesso",
            "certificado": {
                "event": request.event,
                "name": request.name,
                "document": request.document,
                "uuid": certificate_uuid,
                "time": current_time.isoformat(),
                "duration_hours": request.duration_hours,  # Horas de duração do evento
                "json_canonico": certificate_data,
                "hash_sha256": certificado_hash,
                "txid_solana": txid_solana,
                "network": "testnet",
                "timestamp": current_time.isoformat(),
                "timestamp_unix": int(current_time.timestamp())
            },
            "blockchain": {
                "rede": "Solana Devnet",
                "explorer_url": f"https://explorer.solana.com/tx/{txid_solana}?cluster=devnet",
                "verificacao_url": f"http://localhost:8000/certificados/verificar/{txid_solana}",
                "memo_program": "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"
            },
            "validacao": {
                "como_validar": "Recrie o JSON canonizado e compare o hash SHA-256",
                "json_canonico_string": json_canonico,  # String para validação manual
                "hash_esperado": certificado_hash,
                "comando_validacao": f"printf '{json_canonico}' | shasum -a 256"
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao registrar certificado: {str(e)}"
        )


@router.post("/verificar/{txid}")
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
        RPC_URL = "https://api.devnet.solana.com"

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getTransaction",
            "params": [
                txid,
                {"encoding": "json", "maxSupportedTransactionVersion": 0}
            ]
        }

        # Convert payload to JSON and encode
        json_data = json.dumps(payload).encode('utf-8')

        # Create request
        req = urllib.request.Request(
            RPC_URL,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )

        # Make request
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))

        if "result" in data and data["result"]:
            transaction_result = data["result"]

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
                                break
                        except (json.JSONDecodeError, KeyError):
                            continue

            # Generate hash from provided certificate data
            certificate_dict = {
                "event": certificado_data.event,
                "uuid": certificado_data.uuid,
                "name": certificado_data.name,
                "document": certificado_data.document,
                "duration_hours": certificado_data.duration_hours,
                "time": certificado_data.time
            }

            json_canonico = json.dumps(certificate_dict, ensure_ascii=False, separators=(',', ':'), sort_keys=True)
            generated_hash = gerar_hash_texto(json_canonico)

            # Compare hashes
            hash_valido = blockchain_doc_hash == generated_hash

            return {
                "status": "encontrado",
                "transacao": transaction_result,
                "txid": txid,
                "rede": "Solana Devnet",
                "explorer_url": f"https://explorer.solana.com/tx/{txid}?cluster=devnet",
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
        from ..wallet_config import USE_REAL_TRANSACTIONS, ACTIVE_NETWORK, WALLET_CONFIGURED, WALLET_PATH

        if not WALLET_CONFIGURED:
            return {
                "status": "carteira_nao_configurada",
                "mensagem": "Você precisa configurar sua própria carteira",
                "instrucoes": {
                    "passo_1": "Crie sua carteira Solana usando: solana-keygen new",
                    "passo_2": f"Salve o arquivo JSON em: {WALLET_PATH}",
                    "passo_3": "Configure USE_REAL_TRANSACTIONS = True",
                    "passo_4": "Transfira SOL para sua carteira se quiser usar mainnet",
                    "alternativa": "Ou use o sistema em modo simulação (padrão atual)"
                },
                "configuracao_atual": {
                    "carteira_configurada": False,
                    "transacoes_reais": USE_REAL_TRANSACTIONS,
                    "rede": ACTIVE_NETWORK,
                    "modo": "simulacao_completa"
                }
            }

        if not _registry.keypair:
            return {
                "status": "erro",
                "mensagem": "Carteira configurada mas não carregada corretamente"
            }

        wallet_address = str(_registry.keypair.pubkey())

        if USE_REAL_TRANSACTIONS and _registry.client:
            try:
                balance_response = _registry.client.get_balance(_registry.keypair.pubkey())
                balance_sol = balance_response.value / 1_000_000_000  # Converter de lamports para SOL
            except Exception as e:
                balance_sol = f"erro_ao_consultar: {str(e)}"
        else:
            balance_sol = "simulacao"

        return {
            "status": "sucesso",
            "carteira": {
                "endereco": wallet_address,
                "saldo_sol": balance_sol,
                "rede": ACTIVE_NETWORK,
                "transacoes_reais": USE_REAL_TRANSACTIONS,
                "modo": "real" if USE_REAL_TRANSACTIONS else "simulacao"
            },
            "custos": {
                "transacao_memo": "~0.000005 SOL",
                "saldo_recomendado": "0.01 SOL"
            },
            "instrucoes": {
                "obter_sol": f"Transfira SOL da Binance para: {wallet_address}" if USE_REAL_TRANSACTIONS else "Configure sua carteira primeiro"
            }
        }

    except Exception as e:
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