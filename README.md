# Sistema de Certificados na Blockchain Solana

Sistema profissional para emissão e verificação de certificados autenticados na blockchain Solana, com suporte para JSON canonizado e hashing SHA-256.

## Características Principais

- Registro de certificados na blockchain Solana (testnet/mainnet)
- JSON canonizado para garantir integridade de dados
- Hash SHA-256 para verificação de autenticidade
- API REST completa com FastAPI
- **Interface web moderna inspirada no Solana**
- Interface de documentação automática (Swagger)
- Suporte para carteiras personalizadas do usuário
- Modo simulação para desenvolvimento sem custos

## Arquitetura do Sistema

```
certificates-on-solana/
├── app/
│   ├── main.py              # Ponto de entrada da aplicação
│   ├── config.py            # Configurações globais e logging
│   ├── wallet_config.py     # Configurações de carteira
│   ├── routes/
│   │   └── certificados.py  # Endpoints da API
│   └── services/
│       ├── blockchain.py    # Integração com Solana
│       └── hashing.py       # Funções de hash SHA-256
├── frontend/
│   ├── index.html          # Interface web principal
│   ├── css/
│   │   └── main.css        # Estilos com tema Solana
│   └── js/
│       └── main.js         # Aplicação JavaScript vanilla
├── wallet/
│   ├── README.md           # Guia de configuração de carteira
│   └── .gitignore          # Proteção de arquivos sensíveis
├── run.py                  # Script de execução
└── requirements.txt        # Dependências Python
```

## Tecnologias Utilizadas

- **Framework Backend**: FastAPI
- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **Design**: Interface inspirada no Solana (gradientes roxo/verde)
- **Blockchain**: Solana (testnet/mainnet)
- **Hashing**: SHA-256 nativo (hashlib)
- **Servidor ASGI**: Uvicorn
- **JSON**: Canonização com ordenação de chaves
- **Logging**: Sistema estruturado de logs

## Instalação e Configuração

### 1. Clonar o Repositório

```bash
git clone <url-do-repositorio>
cd certificates-on-solana
```

### 2. Ambiente Virtual (Recomendado)

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt

# Para funcionalidade completa da blockchain (opcional):
pip install solana solders
```

### 4. Executar a Aplicação

#### Backend (API)
```bash
# Método recomendado
python run.py

# Alternativo com uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend (Interface Web)
```bash
# Em outro terminal, navegue até a pasta frontend
cd frontend

# Inicie um servidor HTTP local
python3 -m http.server 8080

# Ou use Node.js se preferir
npx serve -s . -l 8080
```

### 5. Acessar o Sistema

- **Interface Web**: http://localhost:8080
- **API Backend**: http://localhost:8000
- **Documentação API**: http://localhost:8000/docs

## Interface Web

A interface web oferece uma experiência moderna e intuitiva:

### Características do Frontend
- 🎨 **Design Solana**: Identidade visual com gradientes roxo/verde característicos
- 📱 **Responsivo**: Funciona perfeitamente em desktop e mobile  
- 🔄 **SPA**: Single Page Application com navegação fluida
- ⚡ **Vanilla JS**: Sem frameworks, JavaScript puro para máxima performance
- 💫 **Animações**: Transições suaves e feedback visual

### Funcionalidades Disponíveis
1. **📝 Registrar Certificado**: Formulário para registrar novos certificados
2. **✅ Verificar Certificado**: Interface para verificar autenticidade
3. **💼 Wallet Info**: Visualizar informações da carteira Solana

### Navegação
- Clique nos botões da navegação para alternar entre funcionalidades
- Formulários com validação em tempo real
- Alertas e feedback visual para todas as ações
- Resultados detalhados com links para o Solana Explorer

## Uso da API

### Interface de Documentação
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints Principais

#### Registrar Certificado
```bash
POST /certificados/register
Content-Type: application/json

{
  "name": "João Silva",
  "event": "Curso de Python",
  "document": "12345678901",
  "duration_hours": 40
}
```

#### Verificar Certificado
```bash
POST /certificados/verify/{txid}
Content-Type: application/json

{
  "event": "PlythonFloripa 25/10/2025",
  "uuid": "173146f8-5a92-4f57-98ee-fd629f3a92a0",
  "name": "Samuel Richard miranda da silva",
  "document": "08625155956",
  "duration_hours": 5,
  "time": "2025-10-24T12:56:37.161876"
}
```

#### Informações da Carteira
```bash
POST /certificados/wallet-info
```

### Exemplo com cURL

```bash
curl -X POST "http://localhost:8000/certificados/register" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "David Richard",
       "event": "PythonFloripa",
       "document": "08625455153", 
       "duration_hours": 5
     }'
```

## JSON Canonizado

O sistema usa JSON canonizado para garantir hashes consistentes:

1. **Ordenação alfabética** de chaves
2. **Separadores compactos** (`,` e `:`)
3. **Sem espaços em branco** extras
4. **UTF-8 sem escape** para caracteres especiais

### Exemplo de JSON Canonizado:
```json
{"document":"08625455153","duration_hours":5,"event":"PythonFloripa","name":"David Richard","time":"2025-10-07T15:30:45.123456","uuid":"550e8400-e29b-41d4-a716-446655440000"}
```

## Configuração de Carteira

O sistema **nunca cria carteiras automaticamente** por motivos de segurança. Consulte o [Guia de Carteira](wallet/README.md) para configuração manual.

### Modos de Operação

1. **Modo Simulação** (padrão): Sem custos, sem transações reais
2. **Modo Real**: Requer carteira configurada e SOL

## Verificação de Certificados

Cada certificado registrado contém:

- **Hash SHA-256**: Integridade dos dados
- **TXID Solana**: Prova de registro na blockchain  
- **UUID único**: Identificador do certificado
- **Timestamp**: Data/hora de emissão
- **Metadados**: Nome, evento, documento, duração

### Validação Manual

```bash
# Gerar hash do JSON canonizado
printf '{"document":"123","duration_hours":5,"event":"Evento","name":"Nome","time":"2025-10-07T...","uuid":"..."}' | shasum -a 256
```

## Logs e Monitoramento

O sistema inclui logging estruturado:

```python
# Configuração em app/config.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Segurança

- **Carteiras controladas pelo usuário**: Sistema nunca gerencia chaves privadas
- **Arquivos protegidos**: .gitignore previne commits acidentais
- **Logs sem dados sensíveis**: Informações críticas não são logadas
- **Validação de entrada**: Todos os inputs são validados

## Solução de Problemas

### Frontend

#### Tela em Branco
```bash
# Verifique se os arquivos existem:
ls frontend/
# Deve mostrar: index.html, css/, js/

# Verifique se o servidor está rodando na pasta correta:
cd frontend
python3 -m http.server 8080

# Acesse: http://localhost:8080
```

#### Erros no Console do Navegador
```bash
# Abra F12 no navegador e verifique:
# - Se os arquivos CSS e JS estão carregando
# - Se há erros de JavaScript
# - Se a API está rodando em localhost:8000
```

#### Erro de CORS
Se houver problemas de CORS entre frontend e backend, adicione no backend:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Backend

#### Bibliotecas Solana não encontradas
```bash
pip install solana solders
```

#### Porta em uso
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows  
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

#### Erro de carteira
Consulte o [Guia de Carteira](wallet/README.md) para configuração correta.

## Desenvolvimento

### Estrutura de Códigos

- `app/main.py`: Configuração FastAPI e rotas
- `app/services/blockchain.py`: Lógica de integração Solana
- `app/services/hashing.py`: Funções de hash SHA-256
- `app/routes/certificados.py`: Endpoints da API
- `app/config.py`: Configurações e logging

## Teste Real
solana: https://explorer.solana.com/tx/4BCKEC12t748Laf27aVQzKFL5JsqikuvQQsXmWn3wexpQiko2MypS688apLcEc1nvNXLPmvz4DMfxVeE5d831Z16?cluster=devnet

```json
{
    "status": "sucesso",
    "certificado": {
        "event": "PlythonFloripa",
        "name": "David Richard",
        "document": "08625455153",
        "uuid": "4f126041-9c58-4e26-b641-4cb9dada81f1",
        "time": "2025-10-07T15:08:04.641753",
        "duration_hours": 5,
        "json_canonico": {
            "event": "PlythonFloripa",
            "uuid": "4f126041-9c58-4e26-b641-4cb9dada81f1",
            "name": "David Richard",
            "document": "08625455153",
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

### Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Implemente testes se necessário
4. Faça commit das mudanças
5. Abra um Pull Request

## Licença

Este projeto está sob licença MIT. Consulte o arquivo LICENSE para detalhes.

## Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação em `/docs`
- Verifique os logs da aplicação

---

**Sistema desenvolvido com FastAPI e integração blockchain Solana**
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