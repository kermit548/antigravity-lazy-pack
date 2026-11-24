---
name: antigravity-github
description: 在 AntiGravity 連接 GitHub CLI。說「連接 GitHub」「設定 GitHub」時載入。
---

# 連接 GitHub（AntiGravity 版）

## 步驟

### 1. 檢查
```bash
gh auth status
```

### 2. 登入
```bash
gh auth login --web --git-protocol https
```

### 3. 設定 Git 使用者
```bash
git config --global user.name "你的名字"
git config --global user.email "your-email@example.com"
```

### 4. 安全規則
- 不把 GitHub token 寫進 Markdown、AGENTS 或 repo
- commit 前先檢查 diff，不無差別 `git add .`


### 5. Git 與 GitHub 工作流驗證規則（背景 `git push` 防干擾）
- **專案初始化綁定憑證助手**：建議先執行以下指令將 GitHub CLI 指定為 Git 憑證助手，確保能跨 Session 安全讀取本機已授權的 GitHub 憑證：
  ```bash
  gh auth setup-git
  ```
- **背景執行 `git push` 前清空 `GITHUB_TOKEN`**：為防範背景沙箱自動注入無效 `GITHUB_TOKEN` 環境變數導致驗證失敗（`Authentication failed`），在執行 `git push` 前必須先將 `GITHUB_TOKEN` 環境變數清空。
  - Windows PowerShell 優先指令組合：
    ```powershell
    $env:GITHUB_TOKEN=$null; git push
    ```
