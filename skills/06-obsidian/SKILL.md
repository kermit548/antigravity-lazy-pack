---
name: antigravity-obsidian
description: 在 AntiGravity 連接 Obsidian（本機保留 MCPVault MCP 設定，另支援直接讀寫 vault）。說「連接 Obsidian」「設定 Obsidian」時載入。
---

# 連接 Obsidian（AntiGravity 版，本機保留 MCPVault 設定）

> **本機客製標記**：上游 `antigravity-lazy-pack v1.5` 改為直接讀寫 vault 而不裝 MCP，但**本機刻意保留 `@bitbonsai/mcpvault` MCP 設定**，與 `%USERPROFILE%\.gemini\config\mcp_config.json` 中既有的 `"obsidian"` 項目保持一致。

## 一、 本機現行 MCPVault 設定（預設保留）

1. **已安裝套件**：`@bitbonsai/mcpvault`（`%APPDATA%\npm\mcpvault.cmd`）
2. **對應 Vault 路徑**：`<YOUR_OBSIDIAN_VAULT_PATH>`
3. **AntiGravity MCP 設定檔**（`%USERPROFILE%\.gemini\config\mcp_config.json`）：
   ```json
   "obsidian": {
     "command": "C:\\Users\\<USERNAME>\\AppData\\Roaming\\npm\\mcpvault.cmd",
     "args": [
       "<YOUR_OBSIDIAN_VAULT_PATH>"
     ],
     "enabled": true
   }
   ```
4. **常用操作**：直接使用 `obsidian` MCP 工具（`read_note`、`write_note`、`patch_note`、`search_notes`、`list_directory`、`update_frontmatter` 等）讀寫筆記。

## 二、 替代方案（上游 v1.5 直接讀寫模式）

若未來決定停用 MCPVault，可在 `mcp_config.json` 移除 `"obsidian"` 項目，改由 AntiGravity 直接讀寫 `<YOUR_OBSIDIAN_VAULT_PATH>` 內的 Markdown 檔案（於專案 `AGENTS.md` 註記對應路徑即可）。

## 三、 安全提醒

* 嚴禁將私人筆記內容或含敏感資訊的本機路徑提交（commit）至公開儲存庫。
