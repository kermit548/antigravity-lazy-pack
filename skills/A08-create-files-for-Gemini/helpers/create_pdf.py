"""
PDF 生成輔助模組 (A08-create-files-for-Gemini)
基於 ReportLab Platypus 與 pypdf，整合 Theme Factory 色彩工廠，專注於產生高品質商業 PDF 報告與多檔案操作
"""
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from pypdf import PdfReader, PdfWriter

try:
    from .theme_factory import get_theme
except ImportError:
    from theme_factory import get_theme

def create_pdf_report(output_path, title, sections, pagesize=A4, theme_name="midnight_executive"):
    """
    建立標準結構化 PDF 報告（整合 Theme Factory 主題色）
    - sections: list of dict: [{'title': '...', 'content': '...', 'table_data': [...]}]
    """
    theme = get_theme(theme_name)
    primary_color = colors.HexColor(f"#{theme['primary'].lstrip('#')}")
    zebra_color = colors.HexColor(f"#{theme.get('zebra_row', 'F8F9FA').lstrip('#')}")
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=pagesize,
        leftMargin=54, rightMargin=54,
        topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=15
    )
    
    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#212121'),
        spaceAfter=8
    )
    
    story = [Paragraph(title, title_style), Spacer(1, 10)]
    
    for sec in sections:
        if 'title' in sec and sec['title']:
            story.append(Paragraph(sec['title'], h1_style))
        if 'content' in sec and sec['content']:
            story.append(Paragraph(sec['content'], body_style))
            
        if 'table_data' in sec and sec['table_data']:
            t = Table(sec['table_data'], repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), primary_color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), zebra_color),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D9D9D9')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            story.append(t)
            story.append(Spacer(1, 10))
            
    doc.build(story)

def merge_pdfs(input_paths, output_path):
    """合併多份 PDF 檔案為單一檔案"""
    writer = PdfWriter()
    for path in input_paths:
        reader = PdfReader(path)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_path, "wb") as f:
        writer.write(f)
