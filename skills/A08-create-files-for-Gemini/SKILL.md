---
name: A08-create-files-for-Gemini
description: 特化文件建立與進階編輯技能（適用於 Windows 11 + Google AntiGravity 環境）。支援 Word (.docx)、簡報 (.pptx)、試算表 (.xlsx) 與 PDF (.pdf) 的高品質新檔建立、專業版面樣式、結構編修、公式計算與互動表單填寫。建立檔案時強制整合 Theme Factory 專業主題配色工廠詢問風格。針對文件純文字讀取與解析，一律無縫對接既有之 markitdown 技能，不重複造輪子。當使用者要求「建立 Word 文件」、「製作 PPT 簡報」、「產出 Excel 試算表」、「生成 PDF 報告」、「填寫 PDF 表單」或「編輯修改 docx/pptx/xlsx/pdf 格式」時載入。
---

# A08-create-files-for-Gemini：特化文件建立與結構編修技能

本技能專注於在 Windows 11（PowerShell）與 Google AntiGravity 環境下，高品質建立與進階編修四類核心商務文件：**Word (`.docx`)**、**PowerPoint (`.pptx`)**、**Excel (`.xlsx`)** 與 **PDF (`.pdf`)**。

---

## 一、 核心原則與職責劃分（不重複造輪子）

本技能嚴格遵守「不重複造輪子」與「工具職責解耦」原則，與系統既有技能劃分如下：

| 工作任務 | 負責技能／工具 | 執行邏輯與路徑 |
| :--- | :--- | :--- |
| **讀取純文字／大綱提取** | **`markitdown`**（既有全域技能） | 執行 `markitdown <檔案路徑>`，將 docx、pptx、xlsx、pdf 秒級轉為結構化 Markdown 文本，節省 Token。**本技能絕不重複開發或覆蓋讀取解析邏輯。** |
| **風格選配（Pre-step）** | **Theme Factory**（內建色彩工廠） | 建立新檔案前，**強制先詢問使用者偏好之主題配色風格**，提供 10 套專業調色盤選配。 |
| **新檔建立（Create）** | **`A08-create-files-for-Gemini`** | 採用本地已安裝之純 Python 函式庫（`python-docx`、`python-pptx`、`openpyxl`、`reportlab`）生成高質感排版檔案，不受 PowerShell 執行權限限制。 |
| **進階編輯（Edit & Modify）** | **`A08-create-files-for-Gemini`** | 針對現有檔案進行解壓縮、XML 節點替換、投影片複製、批註追蹤、公式覆蓋與資料表追加。 |
| **表單自動填寫（PDF Forms）** | **`A08-create-files-for-Gemini`** | 呼叫本地 `pypdf` 與表單結構萃取腳本自動填入 AcroForm 欄位並校驗座標。 |

---

## 二、 前置作業：Theme Factory 專業主題配色工廠（建立檔案前強制執行）

在建立任何新檔案（Word、PPT、Excel、PDF）前，**嚴禁未經確認直接套用單一死板配色**。必須先透過對話詢問使用者想要什麼樣的風格，或主動呈現以下 Theme Factory 10 大經典主題調色盤供使用者挑選：

### 10 大精選商業調色盤一覽表

| 主題名稱（Theme Key） | 主色（Primary） | 副色（Secondary） | 強調色（Accent） | 最佳適用場景與調性 |
| :--- | :---: | :---: | :---: | :--- |
| **1. Midnight Executive（午夜高階）** | `#1E2761`（海軍藍） | `#CADCFC`（冰藍） | `#FFFFFF`（極致白） | 主管匯報、正式合約、財報分析、企業企劃書（穩健權威） |
| **2. Forest & Moss（森林苔蘚）** | `#2C5F2D`（深林綠） | `#97BC62`（苔綠） | `#F5F5F5`（米白） | ESG 永續報告、農業生技、教育訓練、環境政策（生生不息） |
| **3. Teal Trust（青碧信任）** | `#028090`（青碧藍） | `#00A896`（海泡綠） | `#02C39A`（薄荷綠） | 科技金融 (FinTech)、SaaS 產品企劃、資安防護（專業創新） |
| **4. Ocean Gradient（深海漸層）** | `#065A82`（深海藍） | `#1C7293`（藍綠） | `#21295C`（午夜暗藍） | 技術白皮書、工程規格書、學術研究、深入分析（深邃大氣） |
| **5. Charcoal Minimal（極簡碳黑）** | `#36454F`（碳灰） | `#708090`（板岩灰） | `#212121`（墨黑） | 建築設計、工業工程、法律文案、高端品牌企劃（現代俐落） |
| **6. Warm Terracotta（大地陶土）** | `#B85042`（陶土紅） | `#E7E8D1`（暖沙色） | `#A7BEAE`（灰綠） | 文化創意、非營利組織、人力資源、社會福祉（溫潤人文） |
| **7. Coral Energy（珊瑚活力）** | `#F96167`（珊瑚紅） | `#F9E795`（陽光金） | `#2F3C7E`（深海軍藍） | 新創融資 (Pitch Deck)、行銷發布會、激勵提案（熱情驅動） |
| **8. Berry & Cream（莓果醇厚）** | `#6D2E46`（深莓紫） | `#A26769`（乾燥玫瑰） | `#ECE2D0`（象牙白） | 精品零售、生活品味、公關活動、消費趨勢報告（高貴精緻） |
| **9. Sage Calm（鼠尾草寧靜）** | `#84B59F`（鼠尾草綠） | `#69A297`（尤加利綠） | `#50808E`（板岩藍） | 生技醫療、身心健康、諮商輔導、使用者體驗 UX（舒緩平衡） |
| **10. Cherry Bold（櫻桃醒目）** | `#990011`（櫻桃深紅） | `#FCF6F5`（純淨米白） | `#2F3C7E`（對比海軍藍） | 重大里程碑發布、重大風險預警指引、重要宣導（醒目強烈） |

> **執行指引**：
> 1. 當使用者說「幫我做一份簡報」或「產生一份 Word 報告」時，首先提供 3～4 個最契合該主題的配色選項詢問使用者，例如：「這是一份商業報告，建議採用 **Midnight Executive（午夜高階）** 或 **Teal Trust（青碧信任）**，您希望使用哪種風格？」。
> 2. 若使用者有特定品牌色（如指定企業 CIS 色碼 `#0052CC`），Theme Factory 會自動以該色為主色，搭配 60/30/10 比率計算出和諧的副色與淺色卡片底色。

---

## 三、 四大文件處理模組規範

### 模組 1：Word 文件 (`.docx`)

#### 1. 新檔建立標準（採用 `python-docx` + Theme Factory）
* **階層色系**：主標題採用選定主題之主色（`primary`，24 pt 粗體），一級標題（16 pt 粗體），二級標題採用副色（`secondary`，13 pt 粗體）。
* **表格規範**：表頭強制設定主題主色底色（文字反白粗體），資料列採用主題專屬斑馬紋底色（`zebra_row`），欄寬雙重明確賦值（`Inches`）。
* **快速建立**：
  ```python
  from helpers.create_docx import create_document, add_heading_with_style, add_styled_table
  doc = create_document("report.docx", "年度策略報告", "副標題說明", theme_name="midnight_executive")
  ```

#### 2. 現有文件進階編修（OOXML 與修訂追蹤，對齊上游 `anthropics/skills`）
* **文字段落合併**：
  ```powershell
  python "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\docx\merge_runs.py" input.docx -o merged.docx
  ```
* **新增修訂批註（Comments）**：
  ```powershell
  python "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\docx\comment.py" contract.docx "此處條款需再確認" -o annotated.docx
  ```
* **接受所有修訂變更**：
  ```powershell
  python "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\docx\accept_changes.py" in.docx out.docx
  ```
* **OOXML 結構安全驗證**（含目錄與 Schema 校驗）：
  ```powershell
  python "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\docx\office\validate.py" output.docx
  ```

---

### 模組 2：PowerPoint 簡報 (`.pptx`)

#### 1. 簡報建立標準（採用 `python-pptx` + Theme Factory）
* **標準比例**：全面強制設定為 16:9 寬螢幕版面（`slide_width = Inches(13.333)`, `slide_height = Inches(7.5)`）。
* **高對比視覺**：封面與結尾頁使用主題主色滿版背景，內頁內容採用淺色底搭配主題資訊卡片（`add_card`，底色採用 `card_bg`）。
* **演講備忘錄**：補充逐字稿寫入 `slide.notes_slide.notes_text_frame.text`。
* **快速建立**：
  ```python
  from helpers.create_pptx import create_presentation, add_title_slide, add_content_slide, add_card
  prs = create_presentation()
  add_title_slide(prs, "專案推動簡報", "2026 策略規劃", theme_name="forest_moss")
  ```

#### 2. 現有範本進階操作（含上游新增工具）
* **投影片快速複製**（已同步支援 `docProps/app.xml` 計數與 `defusedxml` 安全解析）：
  ```powershell
  python "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\pptx\add_slide.py" deck.pptx slide2.xml -o updated.pptx
  ```
* **結構化提取每頁文字與講者備忘錄**（上游新增，用於精細檢核投影片結構；一般純文字抽取仍優先走 `markitdown`）：
  ```powershell
  python "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\pptx\slide_text.py" deck.pptx
  ```
* **修正 PptxGenJS 主題色彩與修復提示**（上游新增，選用 Node.js 執行，自動修補 `theme1.xml` 與 `autoZero` 圖表錯誤）：
  ```powershell
  node "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\pptx\apply_theme.js" deck.pptx theme.json out.pptx
  ```
* **清理孤立資源**：
  ```powershell
  python "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\pptx\clean.py" unpacked_dir/
  ```

---

### 模組 3：Excel 試算表 (`.xlsx`)

#### 1. 試算表建立與編修標準（採用 `openpyxl` & `pandas` + Theme Factory）
* **公式第一鐵律**：運算結果**嚴禁硬編碼數值**，必須寫入標準 Excel 公式（如 `sheet['C10'] = '=SUM(C2:C9)'`）。
* **樣式標準**：
  - 表頭底色套用主題主色（反白粗體字）。
  - 輸入格（Input）：淺黃底或藍字（`0000FF`），提示使用者可自由填寫。
  - 斑馬紋交錯列套用主題專用 `zebra_row` 色碼。
* **快速建立**：
  ```python
  from helpers.create_xlsx import create_workbook, setup_sheet_table
  wb = create_workbook()
  setup_sheet_table(wb.active, "財務規劃", headers, data, theme_name="teal_trust")
  ```
* **無損重算公式快取**（選用，需本機安裝 LibreOffice；上游已升級為不覆寫原樣式、僅回填計算值並阻擋外部連結）：
  ```powershell
  python "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\xlsx\recalc.py" workbook.xlsx
  ```

---

### 模組 4：PDF 文件與互動表單 (`.pdf`)

#### 1. 高畫質 PDF 產出（採用 `reportlab` + Theme Factory）
* **排版引擎**：採用 `reportlab.platypus` 中的 `SimpleDocTemplate`、`Paragraph`、`Table` 與 `Spacer`。
* **主題套用**：文件標題、表格首列底色與章節標頭自動對齊選定之 Theme Factory 配色。
* **快速建立**：
  ```python
  from helpers.create_pdf import create_pdf_report
  create_pdf_report("output.pdf", "研究報告", sections, theme_name="ocean_gradient")
  ```

#### 2. 互動表單（AcroForm）填寫
* **萃取表單結構**：
  ```powershell
  python "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\pdf\extract_form_structure.py" form.pdf
  ```
* **自動回填欄位**：
  ```powershell
  python "%USERPROFILE%\.gemini\config\skills\A08-create-files-for-Gemini\scripts\pdf\fill_fillable_fields.py" form.pdf data.json output_filled.pdf
  ```

---

## 四、 硬性規則與目錄防污染原則

1. **主題前置詢問鐵律**：建立檔案前必須先確認視覺配色與主題需求，禁止直接輸出預設死板排版。
2. **依賴環境宣告**：日常建立與編修腳本均設計為純 Python 執行，原生相容 Windows 11；僅在選用 `apply_theme.js`（需 Node.js）或 `recalc.py`（需 LibreOffice）時才涉及外部執行環境。
3. **目錄隔離（Directory Isolation）**：產出檔案與中繼暫存檔強制存放於專案 `_output/` 或專用工作目錄，嚴禁直接散落於專案根目錄。
4. **字元編碼防呆**：所有涉及 JSON、XML 或 CSV 的讀寫，一律強制指定 `encoding='utf-8'`；各 CLI 腳本皆已注入 UTF-8 stdout 保護。
