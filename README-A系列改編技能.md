# A 系列改編技能清單（Adapted Skills for Gemini / AntiGravity）

本目錄收錄將各類開源社群、學術工作流（李俊儀教授 SOIL 教學簡報工作流）與外部 AI 平台（如 Anthropic 官方 Skills 庫、`browser-use` 團隊）之實用技能，深度重構與在地化改編為適用於 **Windows 11（PowerShell）** 與 **Google AntiGravity / Gemini** 環境的特化技能。

所有技能均嚴格奉行「**不重複造輪子**」架構原則：
1. **多媒體生圖**：統一呼叫 AntiGravity 內建生圖引擎（`antigravity-draw`），無須外接付費 API。
2. **長文件與多格式檔案讀取**：純文字、表格萃取與大綱提煉全面委託既有全域技能 **`markitdown`**。
3. **離線與本地化優先**：轉錄採用本地 `faster-whisper`，文件建立全面採用本地已驗證之 Python 函式庫，消除外部環境與執行策略限制。
4. **目錄隔離防污染**：中間產物與渲染輸出嚴格限制在各專案之 `_output/` 或專用工作目錄內。

---

## 技能總覽

| Skill 名稱 | 核心功能摘要 | 原始出處 | 觸發詞／使用方式 |
| :--- | :--- | :--- | :--- |
| **`A01-soil-html-deck`** | 李俊儀教授 SOIL 六顆引擎驅動（v2 `soil_interactive_deck_v1` YAML 規格＋互動路由器＋Golden Trio 三樣張鎖定），輸出單一離線 HTML 互動式簡報（內嵌 base64 圖片、Chart.js 圖表、RWD 與 `verify_html.py` 自動化檢驗） | 李俊儀教授 `mathruffian-dot/soil-deck-skills` v2 + AntiGravity 在地化改編 | 說「做 HTML 簡報」、「互動式簡報」、「網頁版簡報」、「線上簡報」、「要有互動圖表的簡報」 |
| **`A02-soil-image-deck`** | SOIL 六引擎純圖片／底圖教學簡報（v2 `soil_image_deck_v2` YAML 規格＋黃金樣張鎖定＋`baked`/`plate` 雙模式＋繁中粗圓體強制檢查），由 `pack_pptx.py` 打包輸出為 16:9 `.pptx` 檔 | 李俊儀教授 `mathruffian-dot/soil-deck-skills` v2 + `antigravity-draw` 視覺工作流改編 | 說「做純圖片簡報」、「全圖簡報」、「每頁都是 AI 生的圖」、「做一份像海報一樣的教學簡報」 |
| **`A03-soil-teaching-deck`** | SOIL 六引擎標準教學簡報 v2，產出「文字物件可雙擊編輯＋AI 概念插圖＋幾何圖形原生備援」之混合式 `.pptx` 簡報，支援認知負荷診斷與結構編修 | 李俊儀教授 `mathruffian-dot/soil-deck-skills` v2 改編 | 說「幫我做教學簡報」、「做一份上課用的投影片」、「幫我把教材做成簡報」、「這份簡報哪裡可以改」 |
| **`A04-find-skills`** | 協助搜尋、探索並安裝適合的 AI Agent Skills，檢視社群技能庫並指引全域或專案安裝流程 | Anthropic Claude Code 原生 `find-skills` 改編（轉為繁中習慣與 AntiGravity 手動/全域目錄放置機制） | 說「如何做某事」、「尋找技能」、「有沒有可以做 XX 的 skill」、「find a skill for X」 |
| **`A05-deep-research-explainer`** | 將複雜概念或科技主題轉化為 3000～5000 字無技術門檻但具嚴謹邏輯之研究型解說長文（Markdown 格式，含 Clickable File Link） | Anthropic Claude Code 官方 `deep-research-explainer` 改編（移除 Linux 輸出路徑硬編碼，轉為本地工作區與點擊連結） | 說「深入搞懂某個主題」、「幫我把 XX 講清楚」、「寫一篇關於 XX 的深度解說／研究型文章」、「系統性整理 XX 的原理與應用」 |
| **`A06-error-screenshot-helper`** | 判讀非技術使用者之錯誤截圖與終端報錯，提供白話診斷、根因分析與逐步修復指引，強化 AntiGravity / Gemini 環境排查 | Anthropic Claude Code 官方 `error-screenshot-helper` 改編（去除正文 Emoji、補充 AntiGravity 與 API 報錯排查） | 說「這是什麼錯誤」、「我遇到問題」、「畫面跳出這個」、「這個錯誤怎麼解決」、「幫我看這個截圖」 |
| **`A07-video-use-for-Gemini`** | 自動剪輯口播、教學或旅遊影片（Windows 11 PowerShell + 本地 faster-whisper 版），支援單詞級轉錄、切除贅字與停頓、自動調色與字幕燒錄 | 開源專案 `browser-use/video-use` 改編（移除雲端付費 ElevenLabs Scribe 改採本地離線 faster-whisper，支援 GPU 硬體編碼加速） | 說「幫我剪輯影片」、「用 video-use 剪片」、「自動剪掉贅字與停頓並上字幕」 |
| **`A08-create-files-for-Gemini`** | 特化商務文件新檔建立、排版樣式設計、結構進階修改、公式計算與 PDF 表單填寫（涵蓋 Word `.docx`、PowerPoint `.pptx`、Excel `.xlsx`、PDF `.pdf`）；建立新檔前強制整合 **Theme Factory（專業主題配色工廠）** 詢問使用者偏好風格 | Anthropic 官方 Skills 庫（`docx`, `pdf`, `pptx`, `xlsx`）改編（解除 Linux/LibreOffice 依賴，轉為純 Python 原生引擎並與 `markitdown` 職責解耦） | 說「建立 Word 文件」、「製作 PPT 簡報」、「產出 Excel 試算表」、「生成 PDF 報告」、「填寫 PDF 表單」、「編輯修改 docx/pptx/xlsx/pdf 格式」 |
| **`A09-webapp-testing-for-Gemini`** | 全功能 Web 應用程式 E2E 自動化測試、安全防護（PII、XSS、權限守衛）與視覺測試；整合本地伺服器生命週期管理（`with_server.py`）與 Chrome 遠端除錯（CDP 9222/9223） | Anthropic Claude Code 官方 `webapp-testing` 改編（適配 Windows 11 本地多伺服器與 Google AntiGravity CDP 沙盒環境） | 說「測試網頁功能」、「執行 E2E 測試」、「驗證網站安全性」、「測試漢堡選單或佈景主題」、「檢查前端連線與 Console 錯誤」 |

---

## 架構原則與共用規範

### 1. 簡報類技能共用設計憲法（A01～A03）
* **林長揚 30 原則**：字級規範（55 / 34 / 21 / 13 pt）、Z 字型視覺動線、強調色 1～2 種、進度條設計、標題小於等於 10 字。
* **SOIL 六顆引擎**：概念定位 → 脈絡定位 → 頁面架構 → 認知編修 → 風格建構 → 總導演。
* **三段式脈絡**：引起動機 → 維持注意 → 喚起行動。

### 2. 特化文件處理與既有工具邊界（A08）
* **純文字讀取與大綱解析**：一律由全域技能 `markitdown` 承擔，不重複編寫轉換器。
* **新檔建立與樣式排版**：全面使用 Python 函式庫（`python-docx`、`python-pptx`、`openpyxl`、`reportlab`），格式皆套用標準色票（深藍 `#1E2761`、深綠 `#2C5F2D`、圓角資訊卡片底色 `#F4F6F9`）。
* **試算表公式運算**：強制寫入 Excel 公式（如 `=SUM()`），嚴禁硬編碼數值結果。

### 3. 多媒體與影片剪輯邊界（A07）
* **音訊轉錄**：全面採用本地 `faster-whisper`，產出單詞級時間戳記 JSON，不消耗雲端 Token 與頻寬。
* **編碼與加速**：編寫轉檔或渲染腳本時強制進行 GPU 偵測（優先順序：NVIDIA `h264_nvenc` > Intel `h264_qsv` > AMD `h264_amf` > CPU `libx264`）。
* **音訊保護**：片段切點強制加入 30 ms 淡入淡出以消除爆音（Audio pop），字幕強制在濾鏡鏈最後一步燒錄。

---

## 實體儲存與全域映射路徑

* **本地儲存與備份路徑**：`<LOCAL_SKILL_BACKUP_DIR>`
* **全域技能啟動路徑**：`%USERPROFILE%\.gemini\config\skills\`
  * 系統載入時以全域路徑為基準，所有技能均保持雙向鏡像同步。
