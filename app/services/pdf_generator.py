"""
Serviço de geração de certificados em PDF
"""

from datetime import datetime
from fpdf import FPDF
from ..config import CERTIFICATE_TITLE, CERTIFICATE_ISSUER


def gerar_certificado_pdf(hash_certificado: str, txid_solana: str, nome_participante: str = "Participante") -> bytes:
    """
    Gera um certificado em PDF com as informações do hash e TXID da Solana.
    
    Args:
        hash_certificado (str): Hash SHA-256 do certificado
        txid_solana (str): Transaction ID da Solana
        nome_participante (str): Nome do participante do certificado
        
    Returns:
        bytes: Conteúdo binário do PDF gerado
    """
    
    # Criar instância do PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Configurar fonte principal
    pdf.set_font("Helvetica", "B", 24)
    
    # Título do certificado
    pdf.cell(0, 20, CERTIFICATE_TITLE, ln=True, align='C')
    pdf.ln(10)
    
    # Subtítulo
    pdf.set_font("Helvetica", "I", 16)
    pdf.cell(0, 15, "Autenticado na Blockchain Solana", ln=True, align='C')
    pdf.ln(15)
    
    # Nome do participante
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 15, f"Certificamos que", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 15, nome_participante, ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 15, "participou com sucesso do evento/curso.", ln=True, align='C')
    pdf.ln(20)
    
    # Informações de autenticação na blockchain
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "INFORMAÇÕES DE AUTENTICAÇÃO BLOCKCHAIN", ln=True, align='C')
    pdf.ln(10)
    
    # Hash do certificado
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(40, 8, "Hash SHA-256:", ln=False)
    pdf.set_font("Helvetica", "", 10)
    
    # Quebrar hash em linhas para melhor visualização
    hash_lines = [hash_certificado[i:i+32] for i in range(0, len(hash_certificado), 32)]
    for i, line in enumerate(hash_lines):
        if i == 0:
            pdf.cell(0, 8, line, ln=True)
        else:
            pdf.cell(40, 8, "", ln=False)  # Espaço para alinhamento
            pdf.cell(0, 8, line, ln=True)
    
    pdf.ln(5)
    
    # TXID da Solana
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(40, 8, "Solana TXID:", ln=False)
    pdf.set_font("Helvetica", "", 10)
    
    # Quebrar TXID em linhas se necessário
    txid_lines = [txid_solana[i:i+32] for i in range(0, len(txid_solana), 32)]
    for i, line in enumerate(txid_lines):
        if i == 0:
            pdf.cell(0, 8, line, ln=True)
        else:
            pdf.cell(40, 8, "", ln=False)  # Espaço para alinhamento
            pdf.cell(0, 8, line, ln=True)
    
    pdf.ln(5)
    
    # Rede Solana
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(40, 8, "Rede:", ln=False)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, "Solana Devnet", ln=True)
    pdf.ln(5)
    
    # Link do explorador
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(40, 8, "Verificar em:", ln=False)
    pdf.set_font("Helvetica", "", 10)
    explorer_url = f"https://explorer.solana.com/tx/{txid_solana}?cluster=devnet"
    pdf.cell(0, 8, explorer_url, ln=True)
    pdf.ln(15)
    
    # Data de emissão
    data_emissao = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Emitido em: {data_emissao}", ln=True, align='C')
    pdf.ln(10)
    
    # Emissor
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 8, f"Emitido por: {CERTIFICATE_ISSUER}", ln=True, align='C')
    pdf.ln(5)
    
    # Nota sobre verificação
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 5, "Este certificado pode ser verificado na blockchain Solana usando o TXID acima.", ln=True, align='C')
    pdf.cell(0, 5, "A autenticidade é garantida pela imutabilidade da blockchain.", ln=True, align='C')
    
    # Retornar o PDF como bytes
    pdf_output = pdf.output()
    if isinstance(pdf_output, str):
        return pdf_output.encode('latin-1')
    return bytes(pdf_output)


def gerar_certificado_simples(nome_participante: str, evento: str = "Evento Geral") -> bytes:
    """
    Gera um certificado simples sem blockchain (para testes).
    
    Args:
        nome_participante (str): Nome do participante
        evento (str): Nome do evento/curso
        
    Returns:
        bytes: Conteúdo binário do PDF gerado
    """
    
    pdf = FPDF()
    pdf.add_page()
    
    # Título
    pdf.set_font("Helvetica", "B", 24)
    pdf.cell(0, 20, "CERTIFICADO DE PARTICIPAÇÃO", ln=True, align='C')
    pdf.ln(20)
    
    # Conteúdo
    pdf.set_font("Helvetica", "", 16)
    pdf.cell(0, 15, f"Certificamos que {nome_participante}", ln=True, align='C')
    pdf.cell(0, 15, f"participou do {evento}", ln=True, align='C')
    pdf.ln(20)
    
    # Data
    data_emissao = datetime.now().strftime("%d/%m/%Y")
    pdf.cell(0, 10, f"Emitido em: {data_emissao}", ln=True, align='C')
    
    # Retornar o PDF como bytes
    pdf_output = pdf.output()
    if isinstance(pdf_output, str):
        return pdf_output.encode('latin-1')
    return bytes(pdf_output)