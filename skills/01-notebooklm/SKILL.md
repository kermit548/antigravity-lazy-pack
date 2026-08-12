---
name: antigravity-notebooklm
description: 在 AntiGravity 連接 NotebookLM MCP。說「連接 NotebookLM」「設定 NotebookLM」時載入。
---

# 連接 NotebookLM（AntiGravity 版）

## 步驟

### 1. 安裝
```bash
uv tool install notebooklm-mcp-cli
nlm --version
```

### 2. 登入 (優先使用 Chrome Remote Debugging / CDP 擷取)
為避免 Windows 下 PowerShell 無法彈出瀏覽器視窗，**預設優先連線至 Chrome Remote Debugging 埠 (9222/9223)** 透過 CDP 自動同步 Cookie 至 nlm：
```python
import asyncio, json, urllib.request, websockets
from notebooklm_tools.core.auth import AuthManager

async def sync_cookies(port=9223):
    targets = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list").read())
    ws_url = [t for t in targets if t.get("type") == "page"][0]["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({"id": 1, "method": "Network.getAllCookies"}))
        cookies = json.loads(await ws.recv())["result"]["cookies"]
        google_cookies = [c for c in cookies if "google" in c.get("domain", "")]
        AuthManager("default").save_profile(cookies=google_cookies, force=True)

asyncio.run(sync_cookies())
```
若 Chrome 未開啟 Remote Debugging，再使用備用互動式登入：
```bash
nlm login
```

### 3. 驗證
```bash
nlm doctor
nlm list
```
若 Windows 有編碼錯誤：`$env:PYTHONIOENCODING = "utf-8"`

### 4. 註冊 MCP
設定以 AntiGravity 的 MCP 設定檔為準：
```json
"notebooklm": {
  "type": "local",
  "command": ["nlm", "mcp"],
  "enabled": true
}
```

⚠️ 不要複製 cookie/token，不把筆記本清單 commit 到 repo。
