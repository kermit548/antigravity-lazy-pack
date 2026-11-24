---
name: antigravity-lazy-packs
description: AntiGravity 懶人包 — 服務連接與工作流程設定。說「AntiGravity 懶人包」「安裝 Antigravity 設定」時載入。
---

# AntiGravity 懶人包 — AI Agent 自動安裝入口

當使用者給你這個 repo 網址並說要安裝時，請依以下流程執行。

## 步驟一：認識可用懶人包

### 說明文件索引
- `README-數字系列基本技能.md`：數字系列基本技能（`01`–`06`）完整安裝與設定指南
- `README-A系列改編技能.md`：A 系列改編技能（`A01`–`A09`）功能總覽、觸發詞與共用設計規範

### 可安裝技能清單

| 編號 | Skill 名稱 | 說明 |
|------|-----------|------|
| 01 | `01-notebooklm` | 連接 NotebookLM MCP |
| 02 | `02-github` | 連接 GitHub CLI |
| 03 | `03-firebase` | 連接 Firebase MCP |
| 04 | `04-draw` | 生圖指引 |
| 05 | `05-workflow` | 開工 / 收工 / 新專案初始化 |
| 06 | `06-obsidian` | 連接 Obsidian MCP (MCPVault) |
| A01 | `A01-soil-html-deck` | SOIL 互動式單檔 HTML 簡報 |
| A02 | `A02-soil-image-deck` | SOIL 純圖片／底圖 `.pptx` 教學簡報 |
| A03 | `A03-soil-teaching-deck` | SOIL 標準可編輯 `.pptx` 教學簡報 |
| A04 | `A04-find-skills` | 探索與搜尋可用 Agent Skills |
| A05 | `A05-deep-research-explainer` | 研究型深度解說長文生成 |
| A06 | `A06-error-screenshot-helper` | 錯誤截圖與終端報錯診斷 |
| A07 | `A07-video-use-for-Gemini` | 自動影片剪輯與字幕燒錄 |
| A08 | `A08-create-files-for-Gemini` | 特化 Word/PPT/Excel/PDF 建立與編修 |
| A09 | `A09-webapp-testing-for-Gemini` | Web 應用程式 E2E 與資安自動化測試 |
| 00 | `00-install-all` | 一次安裝全部（`01`–`06` 與 `A01`–`A09`） |

## 步驟二：讓使用者選擇

列出上表給使用者看，然後問：「你要安裝哪些？輸入全部或編號組合（例如 01, 02, A08）。」

## 步驟三：依序安裝

對選取的每個 skill（全域安裝加 `-g`，僅限單一專案安裝請省略 `-g`）：
```bash
npx skills add kermit548/antigravity-lazy-pack --skill <skill名稱> -g -y
```

若 `npx skills add` 無法使用，改為手動：讀取 `skills/<名稱>/SKILL.md` 內容並執行（全域放置於 `%USERPROFILE%\.gemini\config\skills\`；僅限單一專案放置於目標專案 `./.agents/skills/`）。
若安裝於專案 `./.agents/skills/`，呼叫 `A01`、`A02`、`A07`、`A08`、`A09` 等輔助腳本時，請以實際載入之技能目錄取代全域路徑 `%USERPROFILE%\.gemini\config\skills\`。

## 步驟四：回報結果

每項回報安裝狀態（✅/⚠️/❌），最後列總表。
