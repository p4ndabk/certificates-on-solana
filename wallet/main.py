import json
import base58
import os
from pathlib import Path
from solders.keypair import Keypair

if __name__ == "__main__":
    try:
        script_dir = Path(__file__).parent
        wallet_file = script_dir / "certificates-wallet.json"
        
        if not wallet_file.exists():
            print(f"Arquivo não encontrado em: {wallet_file}")
            print(f"Diretório atual: {script_dir}")
            print("Arquivos disponíveis:")
            exit(1)
        
        with open(wallet_file, "r") as f:
            arr = json.load(f)
        
        print(f"Array carregado: {len(arr)} elementos")
        
        b = bytes(arr)
        
        kp = Keypair.from_bytes(b)
        
        print("INFORMAÇÕES DA CARTEIRA")
        print("=" * 40)
        print(f"Chave pública: {str(kp.pubkey())}")
        print(f"Últimos 32 bytes (Base58): {base58.b58encode(b[32:64]).decode()}")
        print(f"Tamanho total: {len(b)} bytes")
        
        public_from_keypair = str(kp.pubkey())
        public_from_bytes = base58.b58encode(b[32:64]).decode()
        
        
        print(f"\DETALHES:")
        print(f"Secret key (primeiros 8 bytes): {b[:8].hex()}")
        print(f"Public key (últimos 8 bytes): {b[56:64].hex()}")
        
    except Exception as e:
        print(f"Erro: {e}")
        print(f"Tipo do erro: {type(e).__name__}")