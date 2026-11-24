"""
DOCX 生成輔助模組 (A08-create-files-for-Gemini)
基於 python-docx，整合 Theme Factory 色彩工廠，專注於產生符合企業排版水準之 Word 文件
"""
import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

try:
    from .theme_factory import get_theme, hex_to_rgb
except ImportError:
    from theme_factory import get_theme, hex_to_rgb

def set_cell_background(cell, fill_hex):
    """設定儲存格背景色 (例如 'F2F2F2')"""
    fill_hex = fill_hex.lstrip('#')
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def create_document(output_path, title, subtitle=None, author=None, theme_name="midnight_executive"):
    """建立具備專業樣式與 Theme Factory 調色盤之 Word 文件基礎框架"""
    doc = Document()
    theme = get_theme(theme_name)
    primary_rgb = hex_to_rgb(theme["primary"])
    
    # 邊界設定：標準 1 英吋 (72 pt)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # 主標題
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(6)
    title_run = title_p.add_run(title)
    title_run.font.name = 'Arial'
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(*primary_rgb)
    
    # 副標題與作者
    if subtitle:
        sub_p = doc.add_paragraph()
        sub_p.paragraph_format.space_after = Pt(12)
        sub_run = sub_p.add_run(subtitle)
        sub_run.font.name = 'Arial'
        sub_run.font.size = Pt(13)
        sub_run.font.italic = True
        sub_run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        
    if author:
        meta_p = doc.add_paragraph()
        meta_p.paragraph_format.space_after = Pt(24)
        meta_run = meta_p.add_run(f"作者／單位：{author}")
        meta_run.font.size = Pt(10)
        meta_run.font.color.rgb = RGBColor(0x77, 0x77, 0x77)
        
    return doc

def add_heading_with_style(doc, text, level=1, theme_name="midnight_executive"):
    """新增具階層色系之標準標題"""
    theme = get_theme(theme_name)
    primary_rgb = hex_to_rgb(theme["primary"])
    secondary_rgb = hex_to_rgb(theme["secondary"])
    
    p = doc.add_heading(level=level)
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(14 if level == 1 else 10)
    p.paragraph_format.space_after = Pt(4)
    
    run = p.add_run(text)
    run.font.name = 'Arial'
    run.font.bold = True
    if level == 1:
        run.font.size = Pt(16)
        run.font.color.rgb = RGBColor(*primary_rgb)
    elif level == 2:
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(*secondary_rgb)
    else:
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    return p

def add_styled_table(doc, headers, data, col_widths=None, theme_name="midnight_executive"):
    """新增具現代商業排版風格之表格（整合 Theme Factory 主題色）"""
    theme = get_theme(theme_name)
    primary_hex = theme["primary"]
    zebra_hex = theme.get("zebra_row", "F8F9FA")
    
    table = doc.add_table(rows=1 + len(data), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # 表頭排版
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = title
        set_cell_background(hdr_cells[i], primary_hex)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(4)
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            run.font.size = Pt(10)
            
    # 資料列排版
    for row_idx, row_data in enumerate(data):
        row_cells = table.rows[row_idx + 1].cells
        bg_color = zebra_hex if row_idx % 2 == 1 else 'FFFFFF'
        for col_idx, cell_value in enumerate(row_data):
            row_cells[col_idx].text = str(cell_value)
            set_cell_background(row_cells[col_idx], bg_color)
            p = row_cells[col_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            for run in p.runs:
                run.font.size = Pt(9.5)
                
    # 欄寬套用
    if col_widths and len(col_widths) == len(headers):
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return table
