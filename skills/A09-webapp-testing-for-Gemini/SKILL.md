---
name: A09-webapp-testing-for-Gemini
description: 全功能 Web 應用程式端對端 (E2E)、安全性防護與視覺自動化測試技能（適用於 Windows 11 + Google AntiGravity 環境）。深度整合本地 HTTP/多伺服器生命週期管理 (with_server)、Chrome 遠端除錯連線 (CDP Port 9222/9223)、Playwright 對話框狀態機、響應式斷點與彩蛋檢驗、V13 存取守衛與資安漏洞排查、以及動態元素偵察 (Reconnaissance-then-action)。當使用者要求「測試網頁功能」、「執行 E2E 測試」、「驗證網站安全性」、「測試漢堡選單或佈景主題」、「檢查前端連線與 Console 錯誤」或「執行 webapp-testing」時載入。
---

# A09-webapp-testing-for-Gemini：全功能 Web 應用程式自動化與安全測試技能

本技能專注於在 Windows 11 與 Google AntiGravity 環境下，為前端網頁、單頁應用 (SPA) 與串接後端（如 Google Apps Script、Node.js、Python 等）的 Web 系統提供高可靠度、全自動化之測試與除錯能力。

---

## 一、 核心架構與測試決策樹（Decision Tree）

```
測試任務啟動
  ├─ 1. 是否需對接使用者真實已開啟之 Chrome（包含已登入之 Google 帳號/試算表）？
  │     ├─ 是 → 啟用 Chrome CDP 模組 (Port 9222/9223)，執行 connect_over_cdp
  │     └─ 否 → 啟用 Playwright 乾淨獨立沙盒 (Chromium Headless)
  │
  ├─ 2. 目標伺服器是否已在運行？
  │     ├─ 是 (如 XAMPP Apache, http://localhost/...) → 直接連線目標網址
  │     └─ 否 (需動態啟動單一/多伺服器) → 使用 scripts/with_server.py 或內建 ThreadingHTTPServer
  │
  ├─ 3. 測試目標類型判斷：
  │     ├─ A. 完整回歸測試 → 執行全功能整合套件 (scripts/run_unified_suite.py)
  │     ├─ B. 針對性安全排查 → 執行權限守衛、個資洩漏 (PII)、XSS 與 Token 檢查
  │     ├─ C. 響應式與視覺彩蛋 → 設定手機 (390x844)/平板/桌機 Viewport，驗證動畫與轉場
  │     └─ D. 未知/動態動態介面 → 遵循「偵察後行動 (Reconnaissance-then-action)」探索 Selectors
```

---

## 二、 核心模組與四大增強能力

### 模組 1：本地與多伺服器生命週期管理 (`with_server.py`)
參考並吸收上游 `anthropics/skills/webapp-testing` 架構並進行 Windows 11 本地化強化（新增 `taskkill /F /T` 完整清理子程序樹、防止 Port 佔用殘留，並注入 UTF-8 stdout 保護）。呼叫輔助腳本前一律先執行 `--help` 確認參數介面，將腳本視為黑箱工具直接呼叫以節省 Context Token：

```powershell
# 查看參數介面（黑箱呼叫原則）
python "%USERPROFILE%\.gemini\config\skills\A09-webapp-testing-for-Gemini\scripts\with_server.py" --help

# 單一開發伺服器
python "%USERPROFILE%\.gemini\config\skills\A09-webapp-testing-for-Gemini\scripts\with_server.py" --server "npm run dev" --port 5173 -- python my_test.py

# 複合式伺服器 (前後端雙服務)
python "%USERPROFILE%\.gemini\config\skills\A09-webapp-testing-for-Gemini\scripts\with_server.py" `
  --server "cd backend && python server.py" --port 3000 `
  --server "cd frontend && npm run dev" --port 5173 `
  -- python my_test.py
```

---

### 模組 2：Chrome CDP 實體瀏覽器連線 (Port 9222 / 9223)
支援跨越獨立沙盒限制，直接連線使用者日常開啟之 Chrome 視窗，適用於需真實 Google 登入態、Google Drive / Google 試算表之端對端測試：

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    context = browser.contexts[0] if browser.contexts else browser.new_context()
    page = context.new_page()
    page.goto("http://localhost/Other/NTHU_BWY_veggie/index.html")
    # 進行真實環境操作驗證...
```

---

### 模組 3：對話框狀態機與安全邊界防護測試
內建標準 `dialog_state` 狀態機，精確處理 JavaScript 原生 `alert`、`confirm` 與 `prompt`（包含工作人員代碼輸入）：

```python
dialog_state = {"prompt_response": "", "last_alert": "", "confirm_response": True}

def handle_dialog(dialog):
    dialog_state["last_alert"] = dialog.message
    if dialog.type == "alert":
        dialog.accept()
    elif dialog.type == "confirm":
        dialog.accept() if dialog_state["confirm_response"] else dialog.dismiss()
    elif dialog.type == "prompt":
        dialog.accept(dialog_state["prompt_response"])

page.on("dialog", handle_dialog)
```

並針對常見 Web 漏洞提供標準驗證套件：
* **存取守衛（Auth Guard）**：檢查未認證用戶造訪受保護頁面（如 `schedule.html`）時是否強制阻攔且不發送機密請求。
* **憑證持久化（Token Persistence）**：驗證重新整理（F5）或跨頁面時，認證狀態是否安全無縫還原。
* **防偽造降級機制**：驗證若使用者手動偽造權限標記（如 `localStorage.setItem('veg_is_staff', '1')`）但無合法認證碼時，系統是否自動降級防護。

---

### 模組 4：偵察後行動（Reconnaissance-then-action）
針對動態生成的未知網頁或頻繁重構的 UI，先偵察探索再執行動作，杜絕定位器（Selector）脆弱問題：

1. **等待網路閒置**：`page.wait_for_load_state('networkidle')`
2. **元素動態探索**：呼叫 `examples/element_discovery.py` 提取頁面中所有可見按鈕、連結與輸入框。
3. **主動記錄瀏覽器主控台**：呼叫 `examples/console_logging.py` 捕獲前端語法或網路載入警告。

---

## 三、 標準測試執行指令

### 1. 執行全功能一鍵端對端與安全性測試
```bash
python "%USERPROFILE%\.gemini\config\skills\A09-webapp-testing-for-Gemini\scripts\run_unified_suite.py" --root "D:\xampp\htdocs\Other\NTHU_BWY_veggie" --port 8899
```

### 2. 測試產出成果規範
* 所有測試截圖與報告強制存放於指定輸出目錄（預設為專案子目錄 `_output/test_artifacts/` 或 Brain 的 `scratch/` 隔離區），嚴禁散落於專案根目錄。
