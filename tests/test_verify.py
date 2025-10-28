import os
import sys
import pytest
import asyncio
from fastapi.testclient import TestClient
import time

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.main import app

client = TestClient(app)

def test_verify_valid_certificate():
    """Testa verificação com certificado válido existente"""
    
    # Certificado conhecido válido
    valid_txid = "2bV1kzbigzvtEUjh9Z27YX8HPbaKTycoRX1GNTbfvqWqjp3PWh6MhqeYnc7kt4m9JWbfA6rZfC4TCLZTviPCJnNQ"
    valid_data = {
        "event": "plythonfloripa 25/10/2025",
        "uuid": "dbd40c12-de5c-460c-aec4-adac8ef3ac88",
        "name": "david richard miranda da silva",
        "email": "davidrichard.ms@gmail.com",
        "certificate_code": "18927398127398127319",
        "time": "2025-10-28T18:28:59.886954"
    }
    
    response = client.post(f"/certificados/verify/{valid_txid}", json=valid_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "encontrado"
    assert data["validacao"]["certificado_autentico"] == True

def test_verify_invalid_certificate():
    """Testa verificação com certificado inválido"""
    
    # Mesmo certificado mas com dados alterados
    invalid_data = {
        "event": "plythonfloripa 25/10/2025",
        "uuid": "dbd40c12-de5c-460c-aec4-adac8ef3ac88",
        "name": "david richard miranda da silva",
        "email": "davidrichard.ms@gmail.com",
        "certificate_code": "18927398127398127319",
        "time": "2025-10-28T18:28:59.886954"
    }
    
    # TXID válido mas dados diferentes
    valid_txid = "42fay2bKpyTJTr5qCzkHaEjVVmQB7XeAeqW8SbzZYUPgzbNCG1TK6d9whMqBqN3aGFTnqJRPEpRwJkbhzXfdQV7a"
    response = client.post(f"/certificados/verify/{valid_txid}", json=invalid_data)
    
    data = response.json()
    assert data["status"] == "encontrado"
    assert data["validacao"]["certificado_autentico"] == False

def test_verify_nonexistent_certificate():
    """Testa verificação com TXID inexistente"""
    
    fake_txid = "FAKE" * 22
    response = client.post(f"/certificados/verify/{fake_txid}", json={
        "event": "Evento Teste",
        "uuid": "12345678-1234-5678-1234-567812345678",
        "name": "Nome Teste",
        "email": "email@teste.com",
        "certificate_code": 111111,
        "time": "2023-01-01T00:00:00"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "nao_encontrado"

def test_verify_existing_certificate():
    """Testa verificação com certificado real existente"""
    
    # TXID e dados de um certificado real conhecido
    known_txid = "2bV1kzbigzvtEUjh9Z27YX8HPbaKTycoRX1GNTbfvqWqjp3PWh6MhqeYnc7kt4m9JWbfA6rZfC4TCLZTviPCJnNQ"
    known_data = {
        "event": "plythonfloripa 25/10/2025",
        "uuid": "dbd40c12-de5c-460c-aec4-adac8ef3ac88",
        "name": "david richard miranda da silva",
        "email": "davidrichard.ms@gmail.com",
        "certificate_code": "18927398127398127319",
        "time": "2025-10-28T18:28:59.886954"
    }
    
    response = client.post(f"/certificados/verify/{known_txid}", json=known_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "encontrado"
    assert data["validacao"]["certificado_autentico"] == True
    assert data["validacao"]["hash_valido"] == True

def test_verify_modified_certificate():
    """Testa verificação com dados modificados de um certificado existente"""
    
    # Mesmo TXID mas dados alterados
    known_txid = "2bV1kzbigzvtEUjh9Z27YX8HPbaKTycoRX1GNTbfvqWqjp3PWh6MhqeYnc7kt4m9JWbfA6rZfC4TCLZTviPCJnNQ"
    modified_data = {
        "event": "plythonfloripa 25/10/2025 MODIFICADO",  # Dado alterado
        "uuid": "dbd40c12-de5c-460c-aec4-adac8ef3ac88",
        "name": "maria",
        "email": "davidrichard.ms@gmail.com",
        "certificate_code": "18927398127398127319",
        "time": "2025-10-28T18:28:59.886954"
    }
    
    response = client.post(f"/certificados/verify/{known_txid}", json=modified_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "encontrado"
    assert data["validacao"]["certificado_autentico"] == False
