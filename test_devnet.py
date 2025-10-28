#!/usr/bin/env python3
"""
Teste direto da devnet Solana
"""

import asyncio
import json
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solders.message import MessageV0
from solders.transaction import Transaction

async def test_devnet():
    try:
        # Conectar à devnet
        client = Client("https://api.devnet.solana.com")
        print("✅ Conectado à devnet")
        
        # Criar keypair
        keypair = Keypair()
        print(f"✅ Carteira criada: {str(keypair.pubkey())}")
        
        # Solicitar airdrop
        print("Solicitando airdrop...")
        airdrop_response = client.request_airdrop(keypair.pubkey(), 1_000_000_000)
        print(f"✅ Airdrop solicitado: {airdrop_response.value}")
        
        # Aguardar
        await asyncio.sleep(5)
        
        # Verificar saldo
        balance_response = client.get_balance(keypair.pubkey())
        balance_sol = balance_response.value / 1_000_000_000
        print(f"✅ Saldo: {balance_sol} SOL")
        
        if balance_sol > 0:
            # Criar memo
            memo_data = '{"teste": "devnet", "timestamp": 1728291036}'
            memo_bytes = memo_data.encode('utf-8')
            memo_pubkey = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")
            
            instruction = Instruction(
                program_id=memo_pubkey,
                accounts=[],
                data=memo_bytes
            )
            
            # Obter blockhash
            recent_blockhash_response = client.get_latest_blockhash()
            recent_blockhash = recent_blockhash_response.value.blockhash
            
            # Criar transação
            message = MessageV0.try_compile(
                payer=keypair.pubkey(),
                instructions=[instruction],
                address_lookup_table_accounts=[],
                recent_blockhash=recent_blockhash
            )
            
            transaction = Transaction([keypair], message)
            
            # Enviar
            print("Enviando transação...")
            response = client.send_transaction(transaction)
            tx_signature = str(response.value)
            
            print(f"🎉 SUCESSO! TXID real: {tx_signature}")
            print(f"🔗 Explorer: https://explorer.solana.com/tx/{tx_signature}?cluster=devnet")
            
        else:
            print("❌ Airdrop falhou ou ainda processando")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(test_devnet())