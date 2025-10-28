# Certificates on Solana

Sistema de Registro de Certificados na Blockchain Solana, usando FastAPI e Python.

## 🚀 Quick Start

### Instalação

```bash
# Clone o repositório
git clone https://github.com/yourusername/certificates-on-solana.git
cd certificates-on-solana

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Usando Docker

```bash
# Build da imagem
docker build -t certificates-solana .

# Executar o container
docker run -p 8080:8080 certificates-solana
```

### Usando Docker Compose

```bash
docker-compose up
```

## 📝 Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
PORT=8080
HOST=0.0.0.0
SOLANA_NETWORK=devnet
SOLANA_URL=https://api.devnet.solana.com
SOLANA_WALLET_PATH=wallet/certificates-wallet.json
```

## 🛠 API Endpoints

- `POST /certificados/register` - Registra um novo certificado
- `POST /certificados/verify/{txid}` - Verifica um certificado
- `GET /certificados/wallet-info` - Informações da carteira
- `GET /certificados/info-rede` - Status da rede
- `GET /health` - Health check
- `GET /docs` - Documentação OpenAPI

## 📦 Exemplo de Uso

```bash
# Registrar certificado
curl -X POST http://localhost:8080/certificados/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "event": "Python Conference 2024",
    "email": "john@example.com",
    "certificate_code": "PY24-001"
  }'
```

## 🔐 Carteira Solana

1. Crie uma carteira:
```bash
solana-keygen new -o wallet/certificates-wallet.json
```

2. Solicite SOL na devnet:
```bash
solana airdrop 1 wallet/certificates-wallet.json --url https://api.devnet.solana.com
```

## 🚀 Deploy

### Google Cloud Run

```bash
# Build e deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT/certificates-solana
gcloud run deploy certificates-solana \
  --image gcr.io/YOUR_PROJECT/certificates-solana \
  --platform managed
```

## 🛡️ Segurança

- Use HTTPS em produção
- Configure CORS apropriadamente
- Proteja sua carteira Solana
- Mantenha suas dependências atualizadas

## 📄 Licença

MIT License

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🧪 Testes

### Executando os Testes

```bash
# Instalar dependências de teste
pip install -r requirements.txt

# Executar todos os testes
pytest -v

# Executar testes específicos
pytest tests/test_verify.py -v
pytest tests/test_register.py -v
```

### Cenários de Teste

1. Verificação de certificado válido
2. Verificação com dados modificados
3. Verificação de TXID inexistente
4. Registro de novo certificado
5. Validação de payload incompleto

### Estrutura dos Testes

```
tests/
├── __init__.py
├── conftest.py          # Configurações de teste
├── test_register.py     # Testes de registro
└── test_verify.py       # Testes de verificação
```