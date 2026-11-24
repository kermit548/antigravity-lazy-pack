"""
PPTX 生成輔助模組 (A08-create-files-for-Gemini)
基於 python-pptx，整合 Theme Factory 色彩工廠，專注於產生 16:9 現代高質感簡報，支援圖表、雙欄與統計標題卡
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

try:
    from .theme_factory import get_theme, hex_to_rgb
except ImportError:
    from theme_factory import get_theme, hex_to_rgb

def create_presentation():
    """建立標準 16:9 寬螢幕簡報 (13.333" x 7.5")"""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs

def add_title_slide(prs, title, subtitle, theme_name="midnight_executive"):
    """新增具 Theme Factory 風格之高端封面頁"""
    theme = get_theme(theme_name)
    primary_rgb = hex_to_rgb(theme["primary"])
    secondary_rgb = hex_to_rgb(theme["secondary"])
    accent_rgb = hex_to_rgb(theme.get("accent", "FFFFFF"))
    
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    # 主色背景矩形
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(*primary_rgb)
    bg.line.color.rgb = RGBColor(*primary_rgb)
    
    # 標題文字方塊
    tx_box = slide.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(11.0), Inches(3.0))
    tf = tx_box.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = 'Arial'
    p.font.size = Pt(44)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*accent_rgb)
    p.space_after = Pt(16)
    
    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.name = 'Arial'
    p2.font.size = Pt(20)
    p2.font.color.rgb = RGBColor(*secondary_rgb)
    
    return slide

def add_content_slide(prs, title, category=None, theme_name="midnight_executive"):
    """新增具備標準版頭之內容頁"""
    theme = get_theme(theme_name)
    primary_rgb = hex_to_rgb(theme["primary"])
    
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    
    # 分類標籤
    if category:
        cat_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.5), Inches(10.0), Inches(0.4))
        ctf = cat_box.text_frame
        ctf.margin_left = ctf.margin_top = ctf.margin_right = ctf.margin_bottom = 0
        cp = ctf.paragraphs[0]
        cp.text = category.upper()
        cp.font.name = 'Arial'
        cp.font.size = Pt(11)
        cp.font.bold = True
        cp.font.color.rgb = RGBColor(0x75, 0x75, 0x75)
        
    # 主標題
    t_box = slide.shapes.add_textbox(Inches(1.0), Inches(0.85), Inches(11.0), Inches(0.8))
    tf = t_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = 'Arial'
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(*primary_rgb)
    
    return slide

def add_card(slide, left, top, width, height, title, body_bullets, theme_name="midnight_executive"):
    """新增視覺卡片容器，承載文字或條列重點（整合主題色）"""
    theme = get_theme(theme_name)
    primary_rgb = hex_to_rgb(theme["primary"])
    card_bg_rgb = hex_to_rgb(theme.get("card_bg", "F4F6F9"))
    
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(*card_bg_rgb)
    card.line.color.rgb = RGBColor(0xEA, 0xEE, 0xF3)
    
    tb = slide.shapes.add_textbox(left + Inches(0.3), top + Inches(0.3), width - Inches(0.6), height - Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True
    
    tp = tf.paragraphs[0]
    tp.text = title
    tp.font.name = 'Arial'
    tp.font.size = Pt(18)
    tp.font.bold = True
    tp.font.color.rgb = RGBColor(*primary_rgb)
    tp.space_after = Pt(10)
    
    for item in body_bullets:
        bp = tf.add_paragraph()
        bp.text = f"•  {item}"
        bp.font.name = 'Arial'
        bp.font.size = Pt(13)
        bp.font.color.rgb = RGBColor(0x21, 0x21, 0x21)
        bp.space_after = Pt(6)
