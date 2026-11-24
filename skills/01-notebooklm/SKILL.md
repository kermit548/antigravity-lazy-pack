---
name: antigravity-notebooklm
description: 在 AntiGravity 連接 NotebookLM MCP（預設使用本機第三方 notebooklm-mcp-cli，官方 Gemini Notebook 遠端 MCP 作為 Plan B 備用）。說「連接 NotebookLM」「設定 NotebookLM」時載入。
---

# 連接 NotebookLM MCP（AntiGravity 版）

本技能預設採用 **Plan A（本機第三方 `notebooklm-mcp-cli`）**，提供完整 35 項工具（包含筆記本問答查詢 `notebook_query`、跨筆記本查詢、Deep Research、Studio 生成與下載）；當需要純官方 REST / 遠端介面或僅執行基礎筆記本與來源匯入時，改用 **Plan B（Google 官方遠端 MCP）**。

---

## Plan A（預設）：本機第三方 `notebooklm-mcp-cli`

### 1. 安裝或升級

```powershell
# 初次安裝
uv tool install notebooklm-mcp-cli

# 升級至最新版（若因 MCP 伺服器運行中導致 .pyd 檔案存取被拒，請先停止 notebooklm-mcp.exe 與相關 python.exe 再重裝）
uv tool install --upgrade --reinstall notebooklm-mcp-cli
```

* 實測若 `%USERPROFILE%\.local\bin\nlm.exe` 未加入 `PATH` 或出現子指令解析異常，請直接指定套件虛擬環境內的執行檔路徑：
  `%APPDATA%\uv\tools\notebooklm-mcp-cli\Scripts\nlm.exe`

### 2. 登入認證（二選一）

#### 方式 A：標準瀏覽器登入
```powershell
& "$env:APPDATA\uv\tools\notebooklm-mcp-cli\Scripts\nlm.exe" login
```
（於彈出的瀏覽器視窗完成 Google 帳號登入）

#### 方式 B：從已開啟的 CDP Chrome 視窗直接提取憑證（推薦已有 CDP 連線時使用）
若您已於本機 Chrome CDP（例如 `127.0.0.1:9223`）開啟 https://notebook.google.com 並完成登入，可直接透過 `--provider openclaw` 與 `--cdp-url` 提取 Cookie 與 CSRF Token：

```powershell
& "$env:APPDATA\uv\tools\notebooklm-mcp-cli\Scripts\nlm.exe" login --provider openclaw --cdp-url http://127.0.0.1:9223 --force
```

### 3. 驗證與重載憑證

```powershell
$env:PYTHONIOENCODING = "utf-8"
$nlm = "$env:APPDATA\uv\tools\notebooklm-mcp-cli\Scripts\nlm.exe"
& $nlm login --check
& $nlm doctor
& $nlm notebook list
```

* 若 AntiGravity MCP 伺服器已啟動，重新登入後呼叫 MCP 工具 `refresh_auth` 即可載入新憑證，再用 `notebook_list` 驗證。
* 建議可執行 `nlm auth storage set protected` 將憑證改由 Windows 系統憑證管理員保護。
* 嚴禁將本機 Cookie / Token 設定檔提交（commit）至任何版本庫。

### 4. 註冊至 AntiGravity MCP 設定檔

編輯 `%USERPROFILE%\.gemini\config\mcp_config.json`，確認 `notebooklm` 項目指向 `notebooklm-mcp.exe`（`command` 必須為單一字串）：

```json
{
  "mcpServers": {
    "notebooklm": {
      "type": "local",
      "command": "C:\\Users\\<USERNAME>\\AppData\\Roaming\\uv\\tools\\notebooklm-mcp-cli\\Scripts\\notebooklm-mcp.exe",
      "args": [],
      "enabled": true
    }
  }
}
```

### 5. Plan A 常見故障排除

1. **升級出現 `存取被拒 (os error 5)`（鎖定 `_pydantic_core.*.pyd`）**：
   * 原因：背景執行中的 `notebooklm-mcp.exe` 與其子程序 `python.exe` 正在載入該 DLL。
   * 解法：停止 `notebooklm-mcp.exe` 及其子程序後，再執行 `uv tool install --upgrade --reinstall notebooklm-mcp-cli`。
2. **`Authentication expired` 且 `refresh_auth` 自動續期失敗**：
   * 原因：儲存的 Google 登入 Cookie 已失效，或瀏覽器設定檔提取的憑證遭 NotebookLM 拒絕。
   * 解法：執行 `nlm.exe login`，或於已登入的 CDP 瀏覽器上執行 `nlm.exe login --provider openclaw --cdp-url http://127.0.0.1:9223 --force`，完成後呼叫 MCP `refresh_auth`。
3. **IDE 顯示 `No such command 'mcp'` 或 `Failed to load MCP servers`**：
   * 原因：新版已拆分為獨立執行檔 `notebooklm-mcp.exe`，不支援 `nlm mcp`；且 `command` 欄位不可為陣列。
   * 解法：將 `command` 直接指向 `notebooklm-mcp.exe`，`args` 設為 `[]`。
4. **Windows + Python 3.14 出現 `FileExistsError: [WinError 183]`**：
   * 解法：若舊版環境發生此問題，可將套件目錄 `notebooklm_tools\utils\config.py` 中 `safe_mkdir` 的 `except FileExistsError:` 改為 `return`。

---

## Plan B（備用）：Google 官方 Gemini Notebook 遠端 MCP

官方文件參考：https://developers.google.com/notebook/docs 與 https://developers.google.com/notebook/docs/mcp

> **適用與限制（Public Preview）**：目前官方遠端 MCP 僅提供 **7 項**筆記本與來源 CRUD 工具（**不含**問答 `notebook_query`、Studio 生成與本機檔案直接上傳）；僅支援個人 Google 帳號（不支援 Workspace），且該帳號須至少在網頁登入過一次 https://notebook.google.com ；Access Token 有效期限為 **1 小時**。

### 1. 端點與驗證規格

| 設定項目 | 官方規格值 |
| :--- | :--- |
| Server URL | `https://notebook.googleapis.com/mcp` |
| 傳輸協定 | Streamable HTTP（JSON-RPC 2.0，HTTP POST `Content-Type: application/json`） |
| OAuth 2.0 Scope | `https://www.googleapis.com/auth/notebook`（讀寫）或 `notebook.readonly`（唯讀） |
| 必要 HTTP Headers | `Authorization: Bearer <ACCESS_TOKEN>`、`x-goog-user-project: <PROJECT_ID>` |

### 2. 啟用 API 並透過 `gcloud` ADC 取得 Token

```powershell
$PROJECT_ID = "YOUR_PROJECT_ID"
gcloud services enable notebook.googleapis.com --project="$PROJECT_ID"
gcloud auth application-default login --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/notebook"
$ACCESS_TOKEN = (gcloud auth application-default print-access-token).Trim()
```

### 3. 驗證遠端連線（`tools/list`）

```powershell
$headers = @{
  "Authorization"        = "Bearer $ACCESS_TOKEN"
  "x-goog-user-project"  = "$PROJECT_ID"
  "Content-Type"         = "application/json"
  "MCP-Protocol-Version" = "2026-07-28"
  "Mcp-Method"           = "tools/list"
}
$body = '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{"_meta":{"io.modelcontextprotocol/protocolVersion":"2026-07-28"}}}'
Invoke-RestMethod -Uri "https://notebook.googleapis.com/mcp" -Method Post -Headers $headers -Body $body | ConvertTo-Json -Depth 10
```

### 4. 註冊至 AntiGravity MCP 設定檔（可與 Plan A 並存）

在 `%USERPROFILE%\.gemini\config\mcp_config.json` 的 `mcpServers` 內另行新增 `"gemini-notebook-api"`（Token 每小時過期需更新）：

```json
{
  "mcpServers": {
    "gemini-notebook-api": {
      "url": "https://notebook.googleapis.com/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",
        "x-goog-user-project": "YOUR_PROJECT_ID"
      }
    }
  }
}
```

### 5. Plan B 官方工具清單與常見錯誤

* **官方 7 項 MCP 工具**：`create_notebook`、`get_notebook`、`list_notebooks`、`update_notebook`、`create_source`（網頁 URL、YouTube、純文字、Markdown）、`get_source`、`list_sources`（本機檔案上傳需改呼叫 REST `UploadSource` 端點）。
* **`403 WORKSPACE_ACCOUNT_NOT_SUPPORTED`**：使用了 Google Workspace 帳號，請改用個人 Gmail 帳號重新執行 `gcloud auth application-default login`。
* **`404 Account not found for user.`**：該帳號從未登入過 https://notebook.google.com ，請先於瀏覽器登入一次。
* **`401 UNAUTHENTICATED`**：Token 超過 1 小時過期，或誤用未含 `notebook` Scope 的 `gcloud auth print-access-token`。
