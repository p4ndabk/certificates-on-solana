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


@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Página inicial da aplicação com informações básicas.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{APP_NAME}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; text-align: center; margin-bottom: 30px; }}
            h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
            .endpoint {{ background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 4px solid #3498db; }}
            .method {{ background: #27ae60; color: white; padding: 3px 8px; border-radius: 3px; font-size: 12px; font-weight: bold; }}
            .info {{ background: #e8f5e8; padding: 15px; border-radius: 5px; margin: 20px 0; }}
            code {{ background: #f8f9fa; padding: 2px 4px; border-radius: 3px; font-family: 'Courier New', monospace; }}
            pre {{ background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏆 {APP_NAME}</h1>
            
            <div class="info">
                <h2>📋 Sistema de Registro de Certificados</h2>
                <p>Sistema simplificado para registro de certificados na blockchain Solana Testnet.</p>
                <p><strong>Versão:</strong> {APP_VERSION}</p>
            </div>
            
            <h2>🚀 Endpoints Disponíveis</h2>
            
            <div class="endpoint">
                <span class="method">POST</span> <strong>/certificados/registrar</strong>
                <p>Registra um certificado na blockchain e retorna dados JSON</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>/certificados/verificar/{{txid}}</strong>
                <p>Verifica um certificado usando o Transaction ID</p>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span> <strong>/certificados/info-rede</strong>
                <p>Obtém informações sobre o status da rede Solana</p>
            </div>
            
            <h2>💻 Exemplo de Uso</h2>
            <p><strong>Registrar certificado:</strong></p>
            <pre>curl -X POST "http://localhost:8000/certificados/registrar" \\
     -H "Content-Type: application/json" \\
     -d '{{"nome_participante": "João Silva", "evento": "Workshop Blockchain"}}'</pre>
            
            <h2>🌐 Blockchain Info</h2>
            <div class="info">
                <p><strong>Rede:</strong> Solana Testnet</p>
                <p><strong>Explorer:</strong> <a href="https://explorer.solana.com/?cluster=testnet" target="_blank">Solana Explorer (Testnet)</a></p>
                <p><strong>Documentação API:</strong> <a href="/docs" target="_blank">Swagger UI</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


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