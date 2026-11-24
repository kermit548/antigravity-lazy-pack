---
name: video-use-install
description: 在 Windows 11 (PowerShell) 與 Google AntiGravity 環境安裝與驗證 video-use-for-google（整合本地 faster-whisper 與 FFmpeg）。
---

# video-use-for-google 安裝指南 (Windows 11 / PowerShell)

本文件僅供首次安裝或環境檢查使用。日常剪輯請直接讀取 `SKILL.md` 並搭配 `helpers/` 目錄下的腳本。

## 系統必要條件

1. **Python 3.10+**（已安裝 `faster-whisper`、`pillow`、`numpy`）。
2. **`ffmpeg` 與 `ffprobe`** 已加入系統 `PATH` 環境變數（選配 `yt-dlp` 用於下載網路影片素材）。
3. **無需外部付費 API Key**：本版本已全面改用本地 `faster-whisper` 取代雲端 ElevenLabs Scribe。

## Windows 11 (PowerShell) 安裝與檢查步驟

### 1. 驗證 FFmpeg 與 Python 套件

於 PowerShell 執行以下指令確認環境就緒：

```powershell
# 檢查 ffmpeg 與 ffprobe
Get-Command ffmpeg, ffprobe

# 檢查或安裝 Python 核心依賴
pip install faster-whisper pillow numpy
```

### 2. 註冊至 AntiGravity 全域技能目錄

若要註冊為 AntiGravity 全域技能，可在 PowerShell 建立目錄連結或複製至 `%USERPROFILE%\.gemini\config\skills\video-use`：

```powershell
New-Item -ItemType Junction -Path "$env:USERPROFILE\.gemini\config\skills\video-use" -Target "%USERPROFILE%\.gemini\config\skills\A07-video-use-for-Gemini"
```

### 3. 模型與硬體加速設定（選配）

`helpers/transcribe.py` 預設使用 `small` 模型並自動偵測 `cuda` / `cpu`（若無 CUDA 則自動退回 `cpu` + `int8`）。如需自訂預設模型，可在技能根目錄建立 `.env`：

```ini
WHISPER_MODEL=small
WHISPER_DEVICE=auto
WHISPER_COMPUTE_TYPE=int8
```
