# 🔑 Diretório de Carteiras

Este diretório contém os arquivos de carteira Solana para o sistema de certificados.

## ⚠️ **SEGURANÇA CRÍTICA**

- **NUNCA** faça commit dos arquivos de carteira (.json)
- **SEMPRE** mantenha backup seguro das chaves privadas
- **NUNCA** compartilhe esses arquivos

## 📁 Arquivos

- `certificates-wallet.json` - Chave privada da carteira principal
- `.gitignore` - Protege contra commit acidental

## 🔍 Informações da Carteira Atual

# 🔑 Configuração de Carteira Solana

## ⚠️ **O Sistema NÃO Cria Carteiras Automaticamente**

Você deve configurar sua própria carteira para maior segurança e controle.

## 🚀 **Como Configurar Sua Carteira:**

### **Opção 1: Criar Nova Carteira**
```bash
# 1. Instalar Solana CLI
curl -sSfL https://release.solana.com/v1.18.0/install | sh

# 2. Criar nova carteira
solana-keygen new --outfile ./wallet/certificates-wallet.json

# 3. Ver seu endereço público
solana-keygen pubkey ./wallet/certificates-wallet.json
```

### **Opção 2: Usar Carteira Existente**
```bash
# Se você já tem uma carteira, copie o arquivo JSON para:
cp sua-carteira-existente.json ./wallet/certificates-wallet.json
```

### **Opção 3: Usar Phantom/Solflare**
```bash
# Exporte sua chave privada do Phantom/Solflare
# Salve como JSON em: ./wallet/certificates-wallet.json
```

## ⚙️ **Ativar Transações Reais:**

Edite `app/wallet_config.py`:
```python
USE_REAL_TRANSACTIONS = True   # Ativar transações reais
ACTIVE_NETWORK = "mainnet"     # Para usar SOL real
# ou
ACTIVE_NETWORK = "testnet"     # Para testes gratuitos
```

## 💰 **Obter SOL:**

### **Para Mainnet (SOL Real):**
1. Compre SOL na Binance
2. Transfira para seu endereço
3. Mínimo: 0.01 SOL

### **Para Testnet (SOL Grátis):**
```bash
# Obter SOL de teste
solana airdrop 1 --url testnet
```

## 🔒 **Segurança:**

- ✅ Arquivo protegido pelo `.gitignore`
- ✅ Você controla suas chaves privadas
- ✅ Nenhuma criação automática
- ⚠️ **FAÇA BACKUP** das suas chaves
- ⚠️ **NUNCA** compartilhe o arquivo JSON

## 📊 **Verificar Status:**

```bash
curl http://localhost:8000/certificados/wallet-info
```

## 🔄 **Modo Simulação:**

Sem carteira configurada, o sistema funciona em **modo simulação completa** - sem custos, sem transações reais.
- **Uso:** Transações de certificados na Solana
- **Rede:** Configurável (testnet/mainnet)

## 💰 Para usar SOL real:

1. Transfira SOL da Binance para o endereço acima
2. Configure `USE_REAL_TRANSACTIONS = True` em `wallet_config.py`
3. Configure `ACTIVE_NETWORK = "mainnet"` para rede principal

## 🔄 Regenerar Carteira

Se precisar criar uma nova carteira, delete o arquivo `certificates-wallet.json` e reinicie o sistema.