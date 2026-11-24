"""
XLSX 生成輔助模組 (A08-create-files-for-Gemini)
基於 openpyxl 與 pandas，整合 Theme Factory 色彩工廠，專注於產生專業多工作表試算表、公式運算與儲存格樣式
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

try:
    from .theme_factory import get_theme
except ImportError:
    from theme_factory import get_theme

FONT_FAMILY = 'Arial'
REGULAR_FONT = Font(name=FONT_FAMILY, size=10)
BOLD_FONT = Font(name=FONT_FAMILY, size=10, bold=True)
THIN_BORDER_SIDE = Side(border_style='thin', color='D9D9D9')
GRID_BORDER = Border(left=THIN_BORDER_SIDE, right=THIN_BORDER_SIDE, top=THIN_BORDER_SIDE, bottom=THIN_BORDER_SIDE)

def create_workbook():
    """建立空白工作簿"""
    return openpyxl.Workbook()

def setup_sheet_table(ws, title, headers, data, formulas=None, theme_name="midnight_executive"):
    """
    建立標準格式化表格（整合 Theme Factory 主題色）
    - headers: list of header strings
    - data: list of lists (數值或純文字)
    - formulas: dict or list of formula definitions for summary rows
    """
    theme = get_theme(theme_name)
    primary_hex = theme["primary"].lstrip('#')
    zebra_hex = theme.get("zebra_row", "F8F9FA").lstrip('#')
    
    header_fill = PatternFill(start_color=primary_hex, end_color=primary_hex, fill_type='solid')
    zebra_fill = PatternFill(start_color=zebra_hex, end_color=zebra_hex, fill_type='solid')
    header_font = Font(name=FONT_FAMILY, size=11, bold=True, color='FFFFFF')
    
    ws.title = title
    ws.views.sheetView[0].showGridLines = True
    
    # 寫入表頭
    ws.append(headers)
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = GRID_BORDER
    ws.row_dimensions[1].height = 26
    
    # 寫入資料列
    for row_idx, row_values in enumerate(data, start=2):
        ws.append(row_values)
        is_zebra = (row_idx % 2 == 1)
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.font = REGULAR_FONT
            cell.border = GRID_BORDER
            cell.alignment = Alignment(vertical='center')
            if is_zebra:
                cell.fill = zebra_fill
        ws.row_dimensions[row_idx].height = 20
        
    # 自動調適欄寬
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            val_str = str(cell.value or '')
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)
