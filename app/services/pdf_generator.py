"""
Serviço de geração de certificados em PDF
"""

from datetime import datetime
from fpdf import FPDF
from ..config import CERTIFICATE_TITLE, CERTIFICATE_ISSUER


def gerar_certificado_pdf(hash_certificado: str, txid_solana: str, nome_participante: str = "Participante", evento: str = "Evento Geral") -> bytes:
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
    
    # Margens personalizadas para melhor uso do espaço
    pdf.set_margins(20, 20, 20)
    
    # Header decorativo
    pdf.set_font("Helvetica", "B", 28)
    pdf.cell(0, 15, CERTIFICATE_TITLE, ln=True, align='C')
    pdf.ln(5)
    
    # Linha decorativa
    pdf.set_draw_color(50, 50, 50)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    pdf.ln(8)
    
    # Subtítulo
    pdf.set_font("Helvetica", "I", 14)
    pdf.cell(0, 10, "Autenticado na Blockchain Solana", ln=True, align='C')
    pdf.ln(8)
    
    # Nome do participante - seção principal
    pdf.set_font("Helvetica", "", 16)
    pdf.cell(0, 10, "Certificamos que", ln=True, align='C')
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 12, nome_participante, ln=True, align='C')
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 14)
    pdf.cell(0, 10, f"participou com sucesso do evento: {evento}", ln=True, align='C')
    pdf.ln(12)
    
    # Informações de autenticação blockchain - layout compacto
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "AUTENTICAÇÃO BLOCKCHAIN", ln=True, align='C')
    pdf.ln(5)
    
    # Box para informações técnicas
    y_start = pdf.get_y()
    pdf.set_draw_color(200, 200, 200)
    pdf.rect(25, y_start, 160, 35)
    
    # Hash SHA-256 - compacto
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(35, 6, "Hash SHA-256:", ln=False)
    pdf.set_font("Helvetica", "", 8)
    
    # Dividir hash em duas linhas para melhor legibilidade
    hash_line1 = hash_certificado[:32]
    hash_line2 = hash_certificado[32:]
    
    pdf.cell(0, 6, hash_line1, ln=True)
    pdf.cell(35, 6, "", ln=False)  # Espaço para alinhamento
    pdf.cell(0, 6, hash_line2, ln=True)
    
    # TXID - compacto
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(35, 6, "Solana TXID:", ln=False)
    pdf.set_font("Helvetica", "", 8)
    
    # Dividir TXID em duas linhas se muito longo
    if len(txid_solana) > 32:
        txid_line1 = txid_solana[:32]
        txid_line2 = txid_solana[32:]
        pdf.cell(0, 6, txid_line1, ln=True)
        pdf.cell(35, 6, "", ln=False)
        pdf.cell(0, 6, txid_line2, ln=True)
    else:
        pdf.cell(0, 6, txid_solana, ln=True)
    
    # Rede
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(35, 6, "Rede:", ln=False)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "Solana Devnet", ln=True)
    
    pdf.ln(8)
    
    # Link do explorador - formatação melhorada
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "VERIFICAÇÃO NA BLOCKCHAIN:", ln=True, align='C')
    pdf.ln(5)
    
    # URL do explorer em partes menores
    pdf.set_font("Helvetica", "", 9)
    explorer_base = "https://explorer.solana.com/tx/"
    
    # Primeira linha: Label e início da URL
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(30, 6, "Explorer:", ln=False)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, explorer_base, ln=True)
    
    # Segunda linha: TXID
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(30, 6, "TX ID:", ln=False)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, txid_solana, ln=True)
    
    # Terceira linha: Cluster
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(30, 6, "Cluster:", ln=False)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, "devnet", ln=True)
    
    pdf.ln(10)
    
    # Data de emissão e informações finais
    data_emissao = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"Emitido em: {data_emissao}", ln=True, align='C')
    pdf.ln(5)
    
    # Emissor
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, f"Emitido por: {CERTIFICATE_ISSUER}", ln=True, align='C')
    pdf.ln(8)
    
    # Instruções de verificação - mais compactas
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 4, "Para verificar este certificado, acesse o Solana Explorer com o TXID acima.", ln=True, align='C')
    pdf.cell(0, 4, "A autenticidade é garantida pela imutabilidade da blockchain Solana.", ln=True, align='C')
    
    # Linha decorativa final
    pdf.ln(5)
    pdf.set_draw_color(50, 50, 50)
    pdf.line(30, pdf.get_y(), 180, pdf.get_y())
    
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