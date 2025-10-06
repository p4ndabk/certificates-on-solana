"""
Sistema de Emissão de Certificados na Blockchain Solana
Ponto de entrada principal da aplicação FastAPI
"""

from fastapi import FastAPI, Form, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import asyncio

# Importações dos serviços
from app.services.hashing import gerar_hash_sha256, gerar_hash_texto
from app.services.blockchain import registrar_hash_solana, verificar_transacao, obter_info_rede
from app.services.pdf_generator import gerar_certificado_pdf

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
    <html>
    <head>
        <title>{APP_NAME}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
            .header {{ text-align: center; margin-bottom: 30px; }}
            .section {{ margin: 20px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
            .endpoint {{ background-color: #f5f5f5; padding: 10px; margin: 10px 0; border-radius: 3px; }}
            .method {{ font-weight: bold; color: #007bff; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{APP_NAME}</h1>
                <p>{APP_DESCRIPTION}</p>
                <p><strong>Versão:</strong> {APP_VERSION}</p>
            </div>
            
            <div class="section">
                <h2>🚀 Endpoints Disponíveis</h2>
                
                <div class="endpoint">
                    <span class="method">POST</span> <strong>/certificados/emitir</strong>
                    <p>Emite um certificado autenticado na blockchain Solana</p>
                    <p><em>Parâmetros:</em> nome_participante (form), evento (form, opcional)</p>
                </div>
                
                <div class="endpoint">
                    <span class="method">POST</span> <strong>/certificados/verificar</strong>
                    <p>Verifica a autenticidade de um certificado usando TXID</p>
                    <p><em>Parâmetros:</em> txid (form)</p>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <strong>/certificados/info-rede</strong>
                    <p>Obtém informações sobre o status da rede Solana</p>
                </div>
                
                <div class="endpoint">
                    <span class="method">GET</span> <strong>/certificados/hash-exemplo</strong>
                    <p>Gera um hash SHA-256 de exemplo</p>
                    <p><em>Parâmetros:</em> texto (query, opcional)</p>
                </div>
            </div>
            
            <div class="section">
                <h2>📖 Documentação</h2>
                <p><a href="/docs" target="_blank">Swagger UI (Interactive API docs)</a></p>
                <p><a href="/redoc" target="_blank">ReDoc (Alternative API docs)</a></p>
            </div>
            
            <div class="section">
                <h2>🔗 Blockchain</h2>
                <p><strong>Rede:</strong> Solana Devnet</p>
                <p><strong>Explorer:</strong> <a href="https://explorer.solana.com/?cluster=devnet" target="_blank">Solana Explorer (Devnet)</a></p>
            </div>
            
            <div class="section">
                <h2>🧪 Teste Rápido</h2>
                <p>Para testar a emissão de certificado, você pode usar curl:</p>
                <pre>curl -X POST "http://localhost:8000/certificados/emitir" \\
     -H "Content-Type: application/x-www-form-urlencoded" \\
     -d "nome_participante=João Silva&evento=Workshop Blockchain" \\
     --output certificado.pdf</pre>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content


@app.get("/health")
async def health_check():
    """
    Endpoint de verificação de saúde da aplicação.
    """
    try:
        # Testar conectividade com Solana
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
            "status": "degraded",
            "app": APP_NAME,
            "version": APP_VERSION,
            "error": str(e)
        }


# Função principal para desenvolvimento (MVP completo em um arquivo)
@app.post("/certificados/emitir")
async def emitir_certificado_mvp(
    nome_participante: str = Form(..., description="Nome do participante"),
    evento: str = Form(default="Evento Geral", description="Nome do evento/curso")
):
    """
    MVP: Emite um certificado autenticado na blockchain Solana.
    Esta é a implementação completa conforme solicitado na referência.
    
    Args:
        nome_participante (str): Nome do participante
        evento (str): Nome do evento/curso
        
    Returns:
        Response: PDF do certificado com autenticação blockchain
    """
    
    try:
        # 1. Função de Hashing - gerar_hash_sha256
        conteudo_certificado = f"Certificado para {nome_participante} - {evento}"
        conteudo_bytes = conteudo_certificado.encode('utf-8')
        certificado_hash = gerar_hash_sha256(conteudo_bytes)
        
        # 2. Função de Registro na Solana - registrar_hash_solana
        txid_solana = await registrar_hash_solana(certificado_hash)
        
        # 3. Função de Geração de PDF - gerar_certificado_pdf
        pdf_bytes = gerar_certificado_pdf(
            hash_certificado=certificado_hash,
            txid_solana=txid_solana,
            nome_participante=nome_participante
        )
        
        # 4. Endpoint FastAPI - Retorna Response com PDF
        filename = f"certificado_{nome_participante.replace(' ', '_')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao emitir certificado: {str(e)}"
        )


# Endpoint alternativo que aceita JSON

class CertificadoRequest(BaseModel):
    nome_participante: str
    evento: str = "Evento Geral"

@app.post("/certificados/emitir-json")
async def emitir_certificado_json(request: CertificadoRequest):
    """
    Emite um certificado autenticado na blockchain Solana (versão JSON).
    
    Args:
        request (CertificadoRequest): Dados do certificado em JSON
        
    Returns:
        Response: PDF do certificado com autenticação blockchain
    """
    
    try:
        # 1. Função de Hashing - gerar_hash_sha256
        conteudo_certificado = f"Certificado para {request.nome_participante} - {request.evento}"
        conteudo_bytes = conteudo_certificado.encode('utf-8')
        certificado_hash = gerar_hash_sha256(conteudo_bytes)
        
        # 2. Função de Registro na Solana - registrar_hash_solana
        txid_solana = await registrar_hash_solana(certificado_hash)
        
        # 3. Função de Geração de PDF - gerar_certificado_pdf
        pdf_bytes = gerar_certificado_pdf(
            hash_certificado=certificado_hash,
            txid_solana=txid_solana,
            nome_participante=request.nome_participante
        )
        
        # 4. Endpoint FastAPI - Retorna Response com PDF
        filename = f"certificado_{request.nome_participante.replace(' ', '_')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao emitir certificado: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    print(f"Iniciando {APP_NAME} v{APP_VERSION}")
    print("Documentação disponível em: http://localhost:8000/docs")
    print("Página inicial: http://localhost:8000")
    print("Solana Devnet Explorer: https://explorer.solana.com/?cluster=devnet")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )