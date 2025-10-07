# Configuração de Carteira Solana

## IMPORTANTE: Sistema Não Cria Carteiras Automaticamente

Por motivos de segurança, você deve configurar sua própria carteira. O sistema nunca criará ou gerenciará chaves privadas automaticamente.

## Como Configurar Sua Carteira

### Opção 1: Criar Nova Carteira

```bash
# 1. Instalar Solana CLI
curl -sSfL https://release.solana.com/v1.18.0/install | sh

# 2. Criar nova carteira
solana-keygen new --outfile ./wallet/certificates-wallet.json

# 3. Visualizar endereço público
solana-keygen pubkey ./wallet/certificates-wallet.json
```

### Opção 2: Usar Carteira Existente

```bash
# Copie sua carteira existente para o local correto
cp sua-carteira-existente.json ./wallet/certificates-wallet.json
```

### Opção 3: Exportar do Phantom/Solflare

1. Acesse as configurações da sua wallet
2. Exporte a chave privada como arquivo JSON
3. Salve o arquivo como `./wallet/certificates-wallet.json`

## Ativação de Transações Reais

Para usar transações reais na blockchain, edite `app/wallet_config.py`:

```python
USE_REAL_TRANSACTIONS = True   # Ativar transações reais
ACTIVE_NETWORK = "mainnet"     # Para SOL real
# ou
ACTIVE_NETWORK = "testnet"     # Para testes gratuitos
```

## Obter SOL

### Para Mainnet (SOL Real)
1. Compre SOL em exchanges como Binance
2. Transfira para seu endereço da carteira
3. Saldo mínimo recomendado: 0.01 SOL

### Para Testnet (SOL Gratuito)
```bash
# Obter SOL de teste gratuito
solana airdrop 1 --url testnet
```

## Requisitos de Segurança

- **Backup obrigatório**: Sempre faça backup das suas chaves privadas
- **Controle total**: Você mantém controle completo das suas chaves
- **Proteção de arquivos**: Arquivos protegidos pelo .gitignore
- **Compartilhamento proibido**: Nunca compartilhe arquivos de chave privada
- **Verificação**: Verifique sempre os endereços antes de transferir SOL

## Verificação de Status

Para verificar o status da sua carteira:

```bash
curl http://localhost:8000/certificados/wallet-info
```

## Modo Simulação

Quando nenhuma carteira está configurada, o sistema opera em **modo simulação completa**:

- Sem custos reais
- Sem transações na blockchain
- Todas as funcionalidades disponíveis para teste
- Hashes e TXIDs simulados mas válidos

## Informações Técnicas

### Custos Estimados
- Transação de memo: ~0.000005 SOL
- Saldo recomendado: 0.01 SOL para múltiplas operações

### Redes Suportadas
- **Testnet**: Gratuita, para desenvolvimento e testes
- **Mainnet**: Real, requer SOL verdadeiro

### Arquivos de Configuração
- `certificates-wallet.json`: Chave privada da carteira (não incluído no git)
- `.gitignore`: Protege arquivos de carteira contra commits acidentais

## Troubleshooting

### Carteira não carregada
1. Verifique se o arquivo existe em `./wallet/certificates-wallet.json`
2. Confirme que o arquivo JSON está bem formatado
3. Verifique permissões de leitura do arquivo

### Saldo insuficiente
1. Confirme o saldo usando `solana balance`
2. Para testnet: solicite airdrop
3. Para mainnet: transfira SOL de uma exchange

### Transações falhando
1. Verifique conectividade com a rede Solana
2. Confirme que `USE_REAL_TRANSACTIONS = True`
3. Verifique se há SOL suficiente na carteira


Teste Real
solana: https://explorer.solana.com/tx/4BCKEC12t748Laf27aVQzKFL5JsqikuvQQsXmWn3wexpQiko2MypS688apLcEc1nvNXLPmvz4DMfxVeE5d831Z16?cluster=devnet

```json
{
    "status": "sucesso",
    "certificado": {
        "event": "PlythonFloripa",
        "name": "David Richard",
        "document": "08625455956",
        "uuid": "4f126041-9c58-4e26-b641-4cb9dada81f1",
        "time": "2025-10-07T15:08:04.641753",
        "duration_hours": 5,
        "json_canonico": {
            "event": "PlythonFloripa",
            "uuid": "4f126041-9c58-4e26-b641-4cb9dada81f1",
            "name": "David Richard",
            "document": "08625455956",
            "duration_hours": 5,
            "time": "2025-10-07T15:08:04.641753"
        },
        "hash_sha256": "cf4d9e5c786ac569d11751e140b8646167285ea95c53e5897be965e1adf78f05",
        "txid_solana": "4BCKEC12t748Laf27aVQzKFL5JsqikuvQQsXmWn3wexpQiko2MypS688apLcEc1nvNXLPmvz4DMfxVeE5d831Z16",
        "network": "testnet",
        "timestamp": "2025-10-07T15:08:04.641753",
        "timestamp_unix": 1759860484
    },
    "blockchain": {
        "rede": "Solana Devnet",
        "explorer_url": "https://explorer.solana.com/tx/4BCKEC12t748Laf27aVQzKFL5JsqikuvQQsXmWn3wexpQiko2MypS688apLcEc1nvNXLPmvz4DMfxVeE5d831Z16?cluster=devnet",
        "verificacao_url": "http://localhost:8000/certificados/verificar/4BCKEC12t748Laf27aVQzKFL5JsqikuvQQsXmWn3wexpQiko2MypS688apLcEc1nvNXLPmvz4DMfxVeE5d831Z16",
        "memo_program": "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"
    },
    "validacao": {
        "como_validar": "Recrie o JSON canonizado e compare o hash SHA-256",
        "json_canonico_string": "{\"document\":\"08625455956\",\"duration_hours\":5,\"event\":\"PlythonFloripa\",\"name\":\"David Richard\",\"time\":\"2025-10-07T15:08:04.641753\",\"uuid\":\"4f126041-9c58-4e26-b641-4cb9dada81f1\"}",
        "hash_esperado": "cf4d9e5c786ac569d11751e140b8646167285ea95c53e5897be965e1adf78f05",
        "comando_validacao": "printf '{\"document\":\"08625455956\",\"duration_hours\":5,\"event\":\"PlythonFloripa\",\"name\":\"David Richard\",\"time\":\"2025-10-07T15:08:04.641753\",\"uuid\":\"4f126041-9c58-4e26-b641-4cb9dada81f1\"}' | shasum -a 256"
    }
}
```