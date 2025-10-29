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
    
    valid_api_key = os.getenv("API_KEY")
    
    if not valid_api_key:
        return await call_next(request)
    
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
    
    return await call_next(request)
