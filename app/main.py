"""
Sistema de Registro de Certificados na Blockchain Solana
Ponto de entrada principal da aplicação FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# Importações das rotas
from app.routes.certificados import router as certificados_router

# Configurações
from app.config import APP_NAME, APP_VERSION, APP_DESCRIPTION

# Criar instância da aplicação FastAPI
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(certificados_router)

@app.get("/health")
async def health_check():
    """
    Endpoint de health check para verificar se a aplicação está funcionando.
    
    Returns:
        dict: Status da aplicação e informações básicas
    """
    
    try:
        # Testar conectividade com Solana
        from app.services.blockchain import obter_info_rede
        info_rede = await obter_info_rede()
        
        return {
            "status": "healthy",
            "app": APP_NAME,
            "version": APP_VERSION,
            "solana_network": info_rede.get("network", "unknown"),
            "solana_status": info_rede.get("status", "unknown")
        }
        
    except Exception as e:
        return {
            "status": "partial",
            "app": APP_NAME,
            "version": APP_VERSION,
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    
    print(f"Iniciando {APP_NAME} v{APP_VERSION}")
    print("Documentação disponível em: http://localhost:8000/docs")
    print("Página inicial: http://localhost:8000")
    print("Solana Testnet Explorer: https://explorer.solana.com/?cluster=testnet")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )