"""
Rotas para emissão e gerenciamento de certificados
"""

from fastapi import APIRouter, Form, HTTPException, Response
from fastapi.responses import JSONResponse
from typing import Optional
import asyncio

from ..services.hashing import gerar_hash_texto
from ..services.blockchain import registrar_hash_solana, verificar_transacao, obter_info_rede
from ..services.pdf_generator import gerar_certificado_pdf

router = APIRouter(prefix="/certificados", tags=["certificados"])


@router.post("/emitir")
async def emitir_certificado(
    nome_participante: str = Form(..., description="Nome do participante"),
    evento: str = Form(default="Evento Geral", description="Nome do evento/curso")
):
    """
    Emite um certificado autenticado na blockchain Solana.
    
    Args:
        nome_participante (str): Nome do participante
        evento (str): Nome do evento/curso
        
    Returns:
        Response: PDF do certificado com autenticação blockchain
    """
    
    try:
        # 1. Gerar conteúdo do certificado para hash
        conteudo_certificado = f"Certificado para {nome_participante} - {evento}"
        
        # 2. Gerar hash SHA-256 do conteúdo
        certificado_hash = gerar_hash_texto(conteudo_certificado)
        
        # 3. Registrar hash na blockchain Solana
        txid_solana = await registrar_hash_solana(certificado_hash)
        
        # 4. Gerar PDF do certificado
        pdf_bytes = gerar_certificado_pdf(
            hash_certificado=certificado_hash,
            txid_solana=txid_solana,
            nome_participante=nome_participante
        )
        
        # 5. Retornar PDF como resposta
        filename = f"certificado_{nome_participante.replace(' ', '_')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao emitir certificado: {str(e)}"
        )


@router.post("/verificar")
async def verificar_certificado(
    txid: str = Form(..., description="Transaction ID da Solana")
):
    """
    Verifica a autenticidade de um certificado usando o TXID da Solana.
    
    Args:
        txid (str): Transaction ID da transação na Solana
        
    Returns:
        dict: Informações sobre a verificação do certificado
    """
    
    try:
        # Verificar transação na blockchain
        info_transacao = await verificar_transacao(txid)
        
        if info_transacao:
            return {
                "status": "válido",
                "certificado_autenticado": True,
                "txid": txid,
                "informacoes": info_transacao,
                "mensagem": "Certificado autenticado com sucesso na blockchain Solana"
            }
        else:
            return {
                "status": "inválido",
                "certificado_autenticado": False,
                "txid": txid,
                "mensagem": "Transação não encontrada na blockchain"
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao verificar certificado: {str(e)}"
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


@router.get("/hash-exemplo")
async def gerar_hash_exemplo(
    texto: str = "Texto de exemplo para gerar hash"
):
    """
    Gera um hash SHA-256 de exemplo para demonstração.
    
    Args:
        texto (str): Texto para gerar o hash
        
    Returns:
        dict: Hash gerado e informações
    """
    
    try:
        hash_gerado = gerar_hash_texto(texto)
        
        return {
            "texto_original": texto,
            "hash_sha256": hash_gerado,
            "algoritmo": "SHA-256",
            "tamanho_hash": len(hash_gerado)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao gerar hash: {str(e)}"
        )