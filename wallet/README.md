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