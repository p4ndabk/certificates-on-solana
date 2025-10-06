
Eu sou um desenvolvedor Python e estou criando um MVP (Mínimo Produto Viável) de um sistema de emissão de certificados usando FastAPI e Solana. O objetivo é demonstrar como registrar a autenticidade de um certificado PDF na blockchain de teste (Devnet) da Solana.

**Requisitos do Projeto:**

1.  **Framework:** FastAPI.
2.  **Bibliotecas:** `fastapi`, `solana-py`, `hashlib` (nativo), `fpdf2` (para gerar o PDF final).
3.  **Ambiente:** O código deve estar configurado para interagir com a **Solana Devnet**.
4.  **Estrutura de Arquivos:** Crie um único arquivo chamado `main.py` para o MVP.

**Funcionalidades Necessárias em `main.py`:**

1.  **Função de Hashing:** Crie uma função chamada `gerar_hash_sha256(conteudo_bytes: bytes) -> str` que recebe o conteúdo binário de um arquivo e retorna seu hash SHA-256.
2.  **Função de Registro na Solana:** Crie uma função **assíncrona** chamada `registrar_hash_solana(certificado_hash: str) -> str` que:
    * Conecta-se à **Solana Devnet** (URL: `https://api.devnet.solana.com`).
    * Utiliza uma `Keypair` de exemplo (PODE SER SIMULADA OU MOCKADA se o Copilot não puder gerar a Keypair, mas a estrutura da chamada RPC deve estar correta).
    * Cria uma **transação simples** que registra o `certificado_hash` usando o `MemoProgram`.
    * Retorna o **Transaction ID (TXID)** como string.
3.  **Função de Geração de PDF:** Crie uma função chamada `gerar_certificado_pdf(hash_certificado: str, txid_solana: str) -> bytes` usando a biblioteca **`fpdf2`**. O PDF deve conter um título e as strings formatadas mostrando o **Hash** e o **TXID** da Solana. O retorno deve ser o conteúdo binário do PDF.
4.  **Endpoint FastAPI:** Crie uma rota `POST` em `/certificados/emitir` que:
    * Aceita um campo de formulário chamado `nome_participante` (str).
    * Simula a chamada às funções de **Hashing**, **Registro na Solana** e **Geração de PDF**.
    * Retorna uma `Response` HTTP com `media_type="application/pdf"`, contendo o PDF gerado.

**Instrução para o Copilot:**

Gere o código completo do `main.py`, incluindo as importações, as classes/tipos necessários do FastAPI (como `Response` e `UploadFile` – embora o upload do arquivo seja simplificado para este prompt) e os stubs para a interação com a Solana. Adicione comentários onde a lógica real de geração de Keypair ou airdrop de SOL precisaria ser adicionada.

certificados_solana/
├── app/
│   ├── __init__.py
│   ├── main.py            # Ponto de entrada da aplicação
│   ├── routes/
│   │   └── certificados.py # Rotas relacionadas à emissão de certificados
│   ├── services/
│   │   ├── blockchain.py   # Funções para integração com Solana
│   │   ├── pdf_generator.py# Funções para gerar PDFs
│   │   └── hashing.py      # Funções de hashing (SHA-256)
│   └── config.py           # Configurações globais (ex: URL da Devnet)
├── requirements.txt
└── README.md

