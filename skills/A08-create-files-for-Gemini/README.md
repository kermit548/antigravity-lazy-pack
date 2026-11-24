# A08-create-files-for-Gemini

本技能由 Anthropics 官方 Skills 庫中的四項特化文件技能（`docx`、`pdf`、`pptx`、`xlsx`）改寫、精簡與整併而成，專門適配 Google AntiGravity 與 Windows 11 本地環境。

## 核心設計理念

1. **拒絕重複造輪子（銜接既有 `markitdown`）**：
   - 純文字讀取、Markdown 結構轉換、大綱提取：全面委託給已安裝之全域技能 `markitdown`（`markitdown <檔案>`）。
   - 本技能集中火力於四種檔案格式的「**建立（Create）**」、「**版面樣式設計（Styling）**」、「**進階修改（Edit）**」與「**互動表單填寫（Form Filling）**」。

2. **Windows 11 原生相容（Python-First）**：
   - 原版 Anthropics 技能部分依賴 Linux 容器預裝之 Node.js 套件（`docx-js`, `pptxgenjs`）與 LibreOffice CLI（`soffice`）。
   - 本版本全面改寫為純 Python 驅動（採用本地已安裝且驗證完畢之 `python-docx`、`python-pptx`、`openpyxl`、`pandas`、`reportlab`、`pypdf`、`pdfplumber`），繞過 Windows 11 PowerShell 腳本執行策略限制，無需額外安裝肥大依賴。

3. **保留專業進階維護工具**：
   - DOCX：保留 `merge_runs.py`（合併破碎 XML runs）、`comment.py`（插入與追蹤批註）、`accept_changes.py`（接受所有修訂變更）。
   - PPTX：保留 `add_slide.py`（跨版面投影片克隆與註冊）、`clean.py`（清理孤立媒體與未引用版面）、`thumbnail.py`（投影片預覽縮圖網格）。
   - XLSX：保留公式檢核防呆標準，嚴禁硬編碼計算值。
   - PDF：保留 AcroForm 結構萃取（`extract_form_structure.py`）與表單填寫校驗腳本（`fill_fillable_fields.py`、`create_validation_image.py`）。

## 目錄結構

```text
A08-create-files-for-Gemini/
├── SKILL.md                 # AntiGravity 技能主定義文件與觸發規則
├── README.md                # 技能說明文件
├── helpers/                 # 快速生成範本與標準函式庫
│   ├── create_docx.py       # Word 企業風格新檔建立器
│   ├── create_pptx.py       # 16:9 現代簡報與資訊卡片建立器
│   ├── create_xlsx.py       # 多工作表與公式試算表建立器
│   └── create_pdf.py        # ReportLab 高畫質 PDF 建立與合併工具
└── scripts/                 # 進階編修與結構工具
    ├── docx/                # Word XML 修訂與註釋工具
    ├── pdf/                 # PDF 表單填寫與欄位提取工具
    ├── pptx/                # PPTX 投影片複製與清理工具
    ├── xlsx/                # 試算表重算與公式檢查
    └── office/              # Office OOXML 結構檢核規格 (Schemas & Validators)
```
