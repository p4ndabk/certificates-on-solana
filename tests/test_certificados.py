import os
import sys
import pytest
import asyncio
from fastapi.testclient import TestClient
import time

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.main import app

client = TestClient(app)

def test_register_certificate():
    """Testa o registro de certificado com payload completo"""
    
    # Payload de teste
    payload = {
        "event": "PlythonFloripa 25/10/2025",
        "name": "David Richard miranda da silva",
        "email": "davidrichard.ms@gmail.com",
        "certificate_code": "18927398127398127319"
    }

    # Faz a requisição
    response = client.post("/certificados/register", json=payload)
    
    # Verifica status code
    assert response.status_code == 200
    
    # Verifica estrutura da resposta
    data = response.json()
    assert data["status"] == "sucesso"
    assert "certificado" in data
    assert "blockchain" in data
    assert "validacao" in data
    
    # Verifica dados do certificado
    cert = data["certificado"]
    assert cert["event"] == payload["event"]
    assert cert["name"] == payload["name"]
    assert cert["email"] == payload["email"]
    assert "uuid" in cert
    assert "hash_sha256" in cert
    assert "txid_solana" in cert
    
    # Verifica dados da blockchain
    blockchain = data["blockchain"]
    assert "explorer_url" in blockchain
    assert blockchain["rede"].startswith("Solana")
    
    # Verifica dados de validação
    validacao = data["validacao"]
    assert "hash_esperado" in validacao
    assert "json_canonico_string" in validacao

def test_register_certificate_invalid_payload():
    """Testa o registro com payload inválido"""
    
    # Payload incompleto
    payload = {
        "event": "PlythonFloripa 25/10/2025",
        "name": "David Richard"
        # Faltando email e certificate_code
    }

    response = client.post("/certificados/register", json=payload)
    assert response.status_code == 422  # Validation Error

def test_verify_certificate():
    """Testa a verificação de certificado válido"""
    
    # Primeiro registra um certificado
    payload = {
        "event": "PlythonFloripa 25/10/2025",
        "name": "David Richard miranda da silva",
        "email": "davidrichard.ms@gmail.com",
        "certificate_code": "18927398127398127319"
    }
    
    register_response = client.post("/certificados/register", json=payload)
    assert register_response.status_code == 200
    register_data = register_response.json()
    
    # Pega dados necessários para verificação
    txid = register_data["certificado"]["txid_solana"]
    certificate_data = {
        "event": payload["event"],
        "name": payload["name"],
        "email": payload["email"],
        "certificate_code": payload["certificate_code"],
        "uuid": register_data["certificado"]["uuid"],
        "time": register_data["certificado"]["time"]
    }
    
    # Tenta verificar o certificado
    verify_response = client.post(f"/certificados/verify/{txid}", json=certificate_data)
    assert verify_response.status_code == 200
    
    # Verifica resultado
    verify_data = verify_response.json()
    assert verify_data["status"] == "encontrado"
    assert verify_data["validacao"]["hash_valido"] == True
    assert verify_data["validacao"]["certificado_autentico"] == True

def test_verify_invalid_certificate():
    """Testa a verificação de certificado inválido"""
    
    # Dados inválidos para verificação
    invalid_data = {
        "event": "Evento Falso",
        "name": "Nome Falso",
        "email": "fake@email.com",
        "certificate_code": "FAKE-123",
        "uuid": "12345678-1234-5678-1234-567812345678",
        "time": "2023-01-01T00:00:00"
    }
    
    # Tenta verificar com TXID inválido
    fake_txid = "FAKE" * 22  # Simula um TXID inválido
    response = client.post(f"/certificados/verify/{fake_txid}", json=invalid_data)
    
    # Deve retornar 200 mas com status "nao_encontrado"
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "nao_encontrado"
    assert "error" in data

@pytest.mark.real
@pytest.mark.asyncio
async def test_real_certificate_flow():
    """Testa o fluxo completo com blockchain real"""
    
    # Registro
    payload = {
        "event": f"Python Test Event {int(time.time())}",  # Evento único
        "name": "Test User Real",
        "email": "test.real@example.com",
        "certificate_code": f"TEST-{int(time.time())}"  # Código único
    }

    response = client.post("/certificados/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    # Espera confirmação na blockchain
    await asyncio.sleep(5)
    
    # Verificação
    txid = data["certificado"]["txid_solana"]
    verify_data = {
        "event": payload["event"],
        "name": payload["name"],
        "email": payload["email"],
        "certificate_code": payload["certificate_code"],
        "uuid": data["certificado"]["uuid"],
        "time": data["certificado"]["time"]
    }
    
    verify_response = client.post(f"/certificados/verify/{txid}", json=verify_data)
    assert verify_response.status_code == 200
    verify_result = verify_response.json()
    
    assert verify_result["status"] == "encontrado"
    assert verify_result["validacao"]["certificado_autentico"]

@pytest.mark.real
def test_real_wallet_info():
    """Testa informações reais da carteira"""
    
    response = client.get("/certificados/wallet-info")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "sucesso"
    assert isinstance(data["carteira"]["saldo_sol"], (int, float))
    assert data["carteira"]["rede"] == "devnet"
