import os
import sys
import pytest
from fastapi.testclient import TestClient

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from app.main import app

client = TestClient(app)

def test_register_certificate():
    """Testa o registro de certificado com payload completo"""
    
    payload = {
        "event": "PlythonFloripa 25/10/2025",
        "name": "David Richard miranda da silva",
        "email": "davidrichard.ms@gmail.com",
        "certificate_code": "18927398127398127319"
    }

    response = client.post("/certificados/register", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "sucesso"
    assert "certificado" in data
    assert "blockchain" in data
    assert "validacao" in data
    
    cert = data["certificado"]
    assert cert["event"] == payload["event"]
    assert cert["name"] == payload["name"]
    assert cert["email"] == payload["email"]
    assert "uuid" in cert
    assert "hash_sha256" in cert
    assert "txid_solana" in cert

def test_register_certificate_invalid_payload():
    """Testa o registro com payload inválido"""
    
    payload = {
        "event": "PlythonFloripa 25/10/2025",
        "name": "David Richard"
    }

    response = client.post("/certificados/register", json=payload)
    assert response.status_code == 422
