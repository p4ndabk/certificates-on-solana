"""
Serviço de hashing para gerar hashes SHA-256 dos certificados
"""

import hashlib


def gerar_hash_sha256(conteudo_bytes: bytes) -> str:
    """
    Gera um hash SHA-256 a partir do conteúdo em bytes.
    
    Args:
        conteudo_bytes (bytes): Conteúdo binário do arquivo
        
    Returns:
        str: Hash SHA-256 em formato hexadecimal
    """
    sha256_hash = hashlib.sha256()
    sha256_hash.update(conteudo_bytes)
    return sha256_hash.hexdigest()


def gerar_hash_texto(texto: str) -> str:
    """
    Gera um hash SHA-256 a partir de uma string de texto.
    
    Args:
        texto (str): Texto a ser hashado
        
    Returns:
        str: Hash SHA-256 em formato hexadecimal
    """
    return gerar_hash_sha256(texto.encode('utf-8'))