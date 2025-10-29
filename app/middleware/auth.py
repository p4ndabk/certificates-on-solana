"""
Middleware de autenticação por API Key
"""

import os
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable


async def api_key_middleware(request: Request, call_next: Callable) -> Response:
    """
    Middleware para validação de API Key
    
    Args:
        request: Request object do FastAPI
        call_next: Próximo middleware/handler na cadeia
        
    Returns:
        Response: Resposta HTTP
    """
    
    # Rotas que não precisam de autenticação
    public_routes = ["/health", "/docs", "/redoc", "/openapi.json"]
    
    # Verificar se é uma rota pública
    if request.url.path in public_routes:
        return await call_next(request)
    
    # Pegar API key válida do ambiente
    valid_api_key = os.getenv("API_KEY")
    
    if not valid_api_key:
        # Se não há API key configurada, permite acesso (modo desenvolvimento)
        return await call_next(request)
    
    # Verificar se a requisição tem o header x-api-key
    provided_api_key = request.headers.get("x-api-key")
    
    if not provided_api_key:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid API Key"}
        )
    
    if provided_api_key != valid_api_key:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid API Key"}
        )
    
    # API key válida, continuar com a requisição
    return await call_next(request)
