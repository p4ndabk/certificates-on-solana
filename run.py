#!/usr/bin/env python3
"""
Script de inicialização do servidor de Certificados na Solana
Executa a partir da raiz do projeto
"""

if __name__ == "__main__":
    import uvicorn
    
    print("Iniciando Certificados na Solana...")
    print("Documentação: http://localhost:8000/docs")
    print("Interface: http://localhost:8000")
    print("Solana Explorer: https://explorer.solana.com/?cluster=devnet")
    print("=" * 50)
    
    # Executar servidor
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8223,
        reload=True,
        log_level="info"
    )