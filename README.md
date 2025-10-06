# 🎓 Certificados na Solana

Sistema de emissão de certificados autenticados na blockchain Solana. Este MVP (Mínimo Produto Viável) demonstra como registrar a autenticidade de certificados PDF na blockchain de teste (Devnet) da Solana.

## 🚀 Características

- ✅ Emissão de certificados em PDF
- ✅ Autenticação via blockchain Solana (Devnet)
- ✅ Hash SHA-256 para integridade
- ✅ API REST com FastAPI
- ✅ Interface web interativa
- ✅ Verificação de autenticidade
- ✅ Documentação automática (Swagger UI)

## 🏗️ Arquitetura

```
certificates-on-solana/
├── app/
│   ├── __init__.py
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── config.py            # Configurações globais
│   ├── routes/
│   │   ├── __init__.py
│   │   └── certificados.py  # Rotas relacionadas aos certificados
│   └── services/
│       ├── __init__.py
│       ├── blockchain.py    # Integração com Solana
│       ├── pdf_generator.py # Geração de PDFs
│       └── hashing.py       # Funções de hashing SHA-256
├── requirements.txt
├── README.md
└── promp/
    └── referencia.md        # Especificação original
```

## 🛠️ Tecnologias Utilizadas

- **Framework**: FastAPI
- **Blockchain**: Solana (Devnet)
- **Hashing**: SHA-256 (hashlib nativo)
- **PDF**: fpdf2
- **Servidor**: Uvicorn

## 📦 Instalação

### 1. Clonar o repositório

```bash
git clone <url-do-repositorio>
cd certificates-on-solana
```

### 2. Criar ambiente virtual (recomendado)

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\\Scripts\\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

```bash
# Executar a partir da raiz do projeto
python -m app.main

# Ou usando uvicorn diretamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🌐 Uso da API

### Interface Web
Acesse: `http://localhost:8000`

### Documentação Interativa
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Endpoints Principais

#### 1. Emitir Certificado
```bash
POST /certificados/emitir
```

**Parâmetros** (form-data):
- `nome_participante` (obrigatório): Nome do participante
- `evento` (opcional): Nome do evento/curso

**Exemplo com curl**:
```bash
curl -X POST "http://localhost:8000/certificados/emitir" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "nome_participante=João Silva&evento=Workshop Blockchain" \
     --output certificado.pdf
```

#### 2. Verificar Certificado
```bash
POST /certificados/verificar
```

**Parâmetros** (form-data):
- `txid` (obrigatório): Transaction ID da Solana

**Exemplo**:
```bash
curl -X POST "http://localhost:8000/certificados/verificar" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "txid=abc123def456..."
```

#### 3. Informações da Rede
```bash
GET /certificados/info-rede
```

#### 4. Hash de Exemplo
```bash
GET /certificados/hash-exemplo?texto=meu-texto
```

## 🔧 Funcionalidades Implementadas

### 1. Função de Hashing (`gerar_hash_sha256`)
- Localização: `app/services/hashing.py`
- Recebe conteúdo em bytes
- Retorna hash SHA-256 em formato hexadecimal

### 2. Função de Registro na Solana (`registrar_hash_solana`)
- Localização: `app/services/blockchain.py`
- Conecta à Solana Devnet
- Registra hash usando MemoProgram (simulado no MVP)
- Retorna Transaction ID (TXID)

### 3. Função de Geração de PDF (`gerar_certificado_pdf`)
- Localização: `app/services/pdf_generator.py`
- Usa biblioteca fpdf2
- Inclui hash e TXID no certificado
- Retorna conteúdo binário do PDF

### 4. Endpoint FastAPI (`/certificados/emitir`)
- Localização: `app/routes/certificados.py` e `app/main.py`
- Aceita parâmetro `nome_participante`
- Retorna Response HTTP com PDF
- Media type: `application/pdf`

## 🧪 Como Funciona o Processo

1. **Recepção**: API recebe nome do participante
2. **Hashing**: Gera hash SHA-256 do conteúdo do certificado
3. **Blockchain**: Registra hash na Solana Devnet (simulado)
4. **PDF**: Gera certificado PDF com hash e TXID
5. **Resposta**: Retorna PDF como download

## 🔍 Verificação de Autenticidade

Cada certificado contém:
- **Hash SHA-256**: Garante integridade do conteúdo
- **TXID Solana**: Comprova registro na blockchain
- **Link Explorer**: Para verificação manual na rede

## ⚠️ Nota sobre MVP

Este é um MVP para demonstração. Em produção seria necessário:

1. **Chaves Privadas**: Configurar adequadamente as keypairs
2. **Financiamento**: Airdrop ou financiamento de contas de teste
3. **Biblioteca Solana**: Instalar `solana-py` e `solders`
4. **Segurança**: Implementar autenticação e autorização
5. **Persistência**: Banco de dados para armazenar metadados
6. **Monitoramento**: Logs e métricas de produção

## 🌍 Solana Devnet

- **URL**: https://api.devnet.solana.com
- **Explorer**: https://explorer.solana.com/?cluster=devnet
- **Faucet**: https://faucet.solana.com/

## 🐛 Resolução de Problemas

### Erro de importação das bibliotecas Solana
Se você encontrar erros de importação, instale as dependências corretas:

```bash
pip install solana solders
```

### Erro na geração de PDF
Verifique se o fpdf2 está instalado:

```bash
pip install fpdf2
```

### Erro de porta em uso
Mude a porta no arquivo `main.py` ou termine processos na porta 8000:

```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 📝 Logs e Debug

Para debug, verifique os logs no terminal onde a aplicação está rodando. O FastAPI fornece logs detalhados de todas as requisições.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Verifique a documentação em `/docs`
- Consulte os logs da aplicação

---

**Desenvolvido com ❤️ usando FastAPI e Solana**