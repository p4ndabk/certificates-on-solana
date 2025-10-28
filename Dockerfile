FROM python:3.11-slim

WORKDIR /app

# Instala dependências do sistema para Python, TLS e Solana CLI
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instala Python dependências primeiro
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Variáveis de ambiente básicas
ENV PORT=8080 \
    HOST=0.0.0.0 \
    PYTHONUNBUFFERED=1 \
    WALLET_CONFIGURED=true \
    SOLANA_NETWORK=devnet \
    SOLANA_URL=https://api.devnet.solana.com \
    SOLANA_WALLET_PATH=/app/wallet/certificates-wallet.json

EXPOSE 8080

# Executa com uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
