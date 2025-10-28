import pytest
import os
import json
from pathlib import Path
import asyncio

@pytest.fixture(scope="session")
def test_wallet():
    """Configure test wallet"""
    wallet_path = Path(__file__).parent / "test_wallet/certificates-wallet.json"
    wallet_path.parent.mkdir(parents=True, exist_ok=True)
    
    if not wallet_path.exists():
        import subprocess
        subprocess.run(["solana-keygen", "new", "--no-bip39-passphrase", "-o", str(wallet_path)])
        subprocess.run(["solana", "airdrop", "1", "-k", str(wallet_path), "--url", "https://api.devnet.solana.com"])
    
    return wallet_path

@pytest.fixture(autouse=True)
def setup_test_env():
    """Configure test environment"""
    os.environ.update({
        "SOLANA_NETWORK": "devnet",
        "SOLANA_URL": "https://api.devnet.solana.com",
        "WALLET_CONFIGURED": "true",
        "USE_REAL_TRANSACTIONS": "true"
    })

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def mock_blockchain_response():
    """Mock para respostas da blockchain"""
    return {
        "jsonrpc": "2.0",
        "result": {
            "meta": {
                "logMessages": [
                    'Program log: Memo ({"version":"1.0","tipo":"certificado_participacao","code":"TEST-123","name":"Test Name","email":"test@test.com","evento":"Test Event","timestamp":1234567890,"doc_hash":"test_hash","network":"devnet"})'
                ]
            }
        },
        "id": 1
    }
