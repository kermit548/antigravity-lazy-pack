# video-use-for-google (Windows 11 PowerShell + faster-whisper 版)

本專案改寫自 [browser-use/video-use](https://github.com/browser-use/video-use)，專為 **Google AntiGravity** 與 **Windows 11 (PowerShell)** 環境量身打造，並以本地 **`faster-whisper`** 完全取代原本綁定的雲端付費服務 ElevenLabs Scribe。

將原始影片素材放入任意資料夾，透過與 AntiGravity 對話，即可自動完成單詞級語音轉錄、贅字與空白切除、自動調色、30 ms 音訊防爆音淡入淡出、字幕燒錄與動畫疊加，最終輸出 `edit/final.mp4`。

---

## 本版核心改進（相較原版 `video-use`）

| 項目 | 原版 `browser-use/video-use` | 本版 `video-use-for-google` |
| :--- | :--- | :--- |
| **語音轉錄引擎** | 強制綁定雲端付費 ElevenLabs Scribe API | **本地免費 `faster-whisper`**（支援 `word_timestamps=True` 單詞時間戳記與快取） |
| **作業系統與 Shell** | 預設 macOS / Linux (`bash`、`brew`、`ln -sfn`) | **原生支援 Windows 11 (`PowerShell`)** |
| **FFmpeg 路徑相容性** | Unix 路徑假設（Windows 磁碟機冒號與反斜線會在 `subtitles` / `metadata` filter 報錯） | **全面採用 POSIX 路徑正規化與冒號跳脫**，修正 Windows 下 FFmpeg 濾鏡與 concat 路徑問題 |
| **中文字型與編碼** | 硬編碼 macOS `Helvetica` / `Menlo`，檔案讀寫未指定 UTF-8 | **全面強制 UTF-8 編碼**，預設支援 Windows 11 `Microsoft JhengHei`（微軟正黑體）與 `Consolas`，並自動消除中文字元間多餘空白 |

---

## 核心工作流

```text
Transcribe (faster-whisper) ──> Pack (takes_packed.md) ──> LLM 規劃 EDL ──> Render (FFmpeg) ──> Self-Eval (timeline_view)
```

1. **第一層：單詞級語音轉錄 (`helpers/transcribe.py` & `helpers/transcribe_batch.py`)**
   透過 FFmpeg 抽取 16 kHz 單聲道音訊，交由本地 `faster-whisper` 產出精確到每個詞（Word-level）的時間戳記與停頓間距，並透過 `helpers/pack_transcripts.py` 打包為輕量化的 `takes_packed.md`（僅約 12 KB 即可表達長片時間軸）。
2. **第二層：隨選視覺切片 (`helpers/timeline_view.py`)**
   僅在剪輯決策點（如多鏡次挑選、停頓切點確認）針對指定秒數區間生成「膠卷縮圖 + 音訊波形 + 單詞標籤 + 靜音區標示」的合成 PNG。
3. **第三層：分段調色、無損串接與字幕壓製 (`helpers/render.py` & `helpers/grade.py`)**
   依據 `edl.json` 進行單段裁切、自動調色、30 ms 音訊淡入淡出、無損串接、動畫疊加、字幕最後燒錄，以及雙通 `-14 LUFS` 響度標準化。

---

## PowerShell 常用指令

```powershell
# 1. 批次轉錄素材目錄下所有影片（自動快取已轉錄檔案）
python helpers/transcribe_batch.py "D:\Videos\RawFootage" --model small

# 2. 將轉錄 JSON 打包為 LLM 易讀的對話段落時間軸
python helpers/pack_transcripts.py --edit-dir "D:\Videos\RawFootage\edit"

# 3. 產出指定時間區間的膠卷與波形檢視圖
python helpers/timeline_view.py "D:\Videos\RawFootage\clip01.mp4" 2.0 10.5

# 4. 根據 EDL 渲染預覽或最終成品（自動生成並燒錄字幕）
python helpers/render.py "D:\Videos\RawFootage\edit\edl.json" -o "D:\Videos\RawFootage\edit\final.mp4" --build-subtitles
```

完整剪輯規範與 12 條硬性規則請參閱 [`SKILL.md`](./SKILL.md)。
