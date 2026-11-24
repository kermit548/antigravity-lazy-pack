---
name: A07-video-use-for-Gemini
description: 透過對話自動剪輯任何影片（Windows 11 PowerShell + 本地 faster-whisper 版）。支援單詞級語音轉錄、切除贅字與停頓、自動調色、生成覆疊動畫、燒錄字幕——適用於口播、蒙太奇、教學、旅遊、訪談等各類題材。當使用者要求「幫我剪輯影片」、「用 video-use 剪片」、「自動剪掉贅字與停頓並上字幕」時載入。
---

# Video Use for Google AntiGravity (Windows 11 + faster-whisper)

## 核心原則 (Principle)

1. **LLM 透過原始逐字稿與隨選視覺切片進行推理。** 唯一需要預先產出的衍生檔案是段落級時間軸逐字稿（`takes_packed.md`）。其他所有判斷——贅字標記、重錄挑選、鏡頭分類、重點評分——皆由你在決策當下直接從逐字稿推導。
2. **音訊優先，視覺隨行。** 剪輯候選切點來自語音單詞邊界與靜音間隙。僅在需要視覺確認的決策點才呼叫 `timeline_view.py`。
3. **詢問 → 確認 → 執行 → 迭代 → 持久化紀錄。** 在使用者以白話確認剪輯策略前，絕不直接動刀剪輯。
4. **通用化處理。** 不預設立場假設影片類型。先觀察素材、詢問使用者需求，再開始剪輯。
5. **預設享有完整藝術自由。** 本文件中的所有具體數值、預設集、字型、色彩、時長、敘事結構與技巧皆為實戰範例，而非死板規定。請理解其原理後，根據實際素材與使用者需求做出品味決策。**唯一必須嚴格遵守的只有下方的「硬性規則（Hard Rules）」。**
6. **自由創造。** 若素材需要本文件未提及的技巧——分割畫面、子母畫面（PiP）、名條字卡、反應鏡頭切換、變速（Speed ramp）、定格、交叉淡化、L-cut、J-cut——請直接運用 `ffmpeg` 與 `PIL` 實作，無需等待許可。
7. **呈現給使用者前必須自我檢驗（Self-eval）。** 自己不會拿來發佈的半成品，絕不端給使用者。

---

## 硬性規則 (Hard Rules — 工程正確性，不可妥協)

違反以下規則會導致無聲失敗或產出損壞影片。這不是美學品味問題，而是工程正確性，必須嚴格遵守：

1. **字幕必須在濾鏡鏈的「最後一步」燒錄**（在所有動畫 overlay 之後）。否則動畫圖層會遮蓋字幕，造成無聲錯誤。
2. **採用「單段獨立抽取 → 無損 `-c copy` 串接」**，而非單通複雜濾鏡圖。否則加入動畫時會導致所有片段被二次編碼。
3. **每個片段邊界強制加入 30 ms 音訊淡入淡出**（`afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03`）。否則每個切點都會產生爆音（Audio pop）。
4. **動畫疊加圖層必須使用 `setpts=PTS-STARTPTS+T/TB`** 將動畫第 0 幀平移對齊至顯示視窗起點。否則顯示時會直接跳到動畫中段。
5. **主字幕檔 (`master.srt`) 必須使用輸出時間軸偏移量**：`output_time = word.start - segment_start + segment_offset`。否則片段串接後字幕時間會嚴重錯位。
6. **絕不在單詞中間切斷。** 每個剪輯切點邊界必須對齊 `faster-whisper` 產出的單詞時間戳記邊界。
7. **每個剪輯邊界必須預留緩衝（Padding）。** 工作區間：30–200 ms。語音時間戳記可能存在 50–100 ms 漂移，預留緩衝可吸收誤差。快節奏取小值，電影感取大值。
8. **強制使用單詞級（Word-level）逐字轉錄。** 絕不使用僅有句子級的 SRT 模式（會遺失次秒級停頓資訊）。
9. **每個來源檔案轉錄結果必須快取。** 除非來源影片本身變更，否則絕不重複執行轉錄。
10. **多個動畫必須透過平行 Subagents 同時生成。** 絕不序列執行。透過 `invoke_subagent` 一次平行啟動 N 個動畫子代理，總耗時約等於最慢的那一個。
11. **執行前必須先確認策略。** 在使用者核准白話剪輯計畫前，絕不開始渲染。
12. **所有工作階段產出物一律存放在 `<videos_dir>\edit\`。** 絕不在 `video-use-for-google\` 技能目錄內寫入任何專案暫存或輸出檔。
13. **GPU 自動識別與硬體加速規範（重要鐵律）**：日後編寫任何 FFmpeg 轉檔、抽段、濾鏡合成或影片渲染腳本時，**必須執行 GPU 自動識別**。啟動時自動偵測環境是否具備硬體編碼加速（支援階層：NVIDIA `h264_nvenc` > Intel `h264_qsv` > AMD `h264_amf` > CPU `libx264` 備援），嚴禁未經偵測直接寫死 CPU `libx264`。

---

## 目錄結構 (Directory Layout)

本技能位於 `%USERPROFILE%\.gemini\config\skills\A07-video-use-for-Gemini\`。使用者的原始影片素材保留於原位，所有剪輯產出物一律寫入 `<videos_dir>\edit\`：

```text
<videos_dir>\
├── <原始影片素材，保持原樣不修改>
└── edit\
    ├── project.md               ← 專案記憶；每次工作階段追加紀錄
    ├── takes_packed.md          ← 段落級時間軸逐字稿，LLM 的主要閱讀視圖
    ├── edl.json                 ← 剪輯決策清單 (Edit Decision List)
    ├── transcripts\<name>.json  ← 快取的 faster-whisper 單詞級 JSON
    ├── animations\slot_<id>\    ← 各動畫插槽的原始碼、渲染檔與設計說明
    ├── clips_graded\            ← 含調色與 30 ms 音訊淡入淡出的分段抽取檔
    ├── master.srt               ← 對齊輸出時間軸的主字幕檔
    ├── downloads\               ← yt-dlp 下載素材
    ├── verify\                  ← 除錯影格與 timeline_view PNG 檢視圖
    ├── preview.mp4              ← 預覽輸出
    └── final.mp4                ← 最終成品輸出
```

---

## 環境檢查 (Windows 11 / PowerShell Setup)

每次冷啟動時，僅需在 PowerShell 快速驗證以下項目（無需重新安裝）：

- **無需 API Key**：語音轉錄採用本機 Python 環境已內建之 `faster-whisper`（預設使用 `small` 模型，可透過 `--model base|small|medium|large-v3` 或環境變數 `WHISPER_MODEL` 指定）。
- **`ffmpeg` 與 `ffprobe`** 在系統 `PATH` 中可正常呼叫。
- **Python 依賴**：`faster-whisper`、`pillow`、`numpy` 已安裝。
- 若需製作 HyperFrames 或 Remotion 網頁動畫插槽，確認系統具備 `node` 與 `npm`；若需 Manim 數學動畫，讀取本技能目錄下的 `skills\manim-video\SKILL.md`。

所有輔助腳本位於本技能目錄的 `helpers\` 下，請以完整路徑呼叫（例如：`python "%USERPROFILE%\.gemini\config\skills\A07-video-use-for-Gemini\helpers\transcribe_batch.py" ...`）。

---

## 輔助腳本工具箱 (Helpers)

- **`helpers\transcribe.py <video>`** — 單檔本地 `faster-whisper` 單詞級轉錄。支援 `--model small`、`--language zh`、`--audio-track 0`。具自動快取。
- **`helpers\transcribe_batch.py <videos_dir>`** — 批次轉錄資料夾內所有影片（預先載入模型並自動跳過已快取檔案）。多片段專案首選。
- **`helpers\pack_transcripts.py --edit-dir <dir>`** — 將 `transcripts\*.json` 打包為 `takes_packed.md`（以靜音 ≥ 0.5s 分段，並自動清除中文字元間多餘空白）。
- **`helpers\timeline_view.py <video> <start> <end>`** — 產出「膠卷影格 + 音訊波形 + 單詞標籤 + 靜音陰影」合成 PNG。**隨選視覺下鑽工具**——僅在決策點呼叫，勿對整部影片迴圈掃描。
- **`helpers\render.py <edl.json> -o <out>`** — 依照「分段抽取 → 無損串接 → 動畫疊加 (PTS 對齊) → 字幕最後燒錄 → 雙通 -14 LUFS 響度標準化」管線渲染。支援 `--preview`（快速預覽）、`--draft`（720p 極速切點檢查）、`--build-subtitles`（自動生成 `master.srt`）。
- **`helpers\grade.py <in> -o <out>`** — FFmpeg 濾鏡調色工具。預設為數據驅動之 `auto` 自動微調模式（限制在 ±8% 內修正曝光與對比），亦支援 `--preset warm_cinematic|neutral_punch|subtle|none` 或 `--filter "<raw>"`。

---

## 標準剪輯流程 (The Process)

1. **清點素材 (Inventory)**：
   - 用 `ffprobe` 檢查來源影片資訊。
   - 對素材資料夾執行 `transcribe_batch.py`。
   - 執行 `pack_transcripts.py` 產出 `takes_packed.md`。
   - 抽樣執行 1～2 次 `timeline_view.py` 取得畫面初步視覺印象。
2. **預先掃描問題 (Pre-scan)**：
   - 閱讀 `takes_packed.md`，列出明顯吃螺絲、口誤、重複重錄或應避開的語句，作為後續剪輯指令依據。
3. **對話確認需求 (Converse)**：
   - 用白話向使用者描述你看到的素材內容，並根據素材特性提問：影片定位、目標時長與長寬比、視覺/品牌風格、節奏感、必留畫面、必刪片段、動畫與調色偏好、字幕需求。
4. **提出剪輯策略 (Propose Strategy)**：
   - 以 4～8 句話總結：敘事結構、鏡次選擇、剪輯方向、動畫規劃、調色方向、字幕風格與預估總時長。**等待使用者確認後才可往下執行。**
5. **執行剪輯 (Execute)**：
   - 產出 `edl.json`（若為多鏡次大型專案可委派 Editor Subagent）。
   - 在模糊切點處使用 `timeline_view.py` 確認畫面與波形。
   - 若有多個動畫，透過 `invoke_subagent` 平行生成至 `<edit>\animations\slot_<id>\`。
   - 透過 `render.py` 合成輸出。
6. **產生預覽 (Preview)**：
   - 執行 `render.py --preview`。
7. **自我檢驗 (Self-eval，展示給使用者前必做)**：
   - 對**渲染後的輸出檔**（非原始素材）在每個切點邊界（±1.5s 視窗）執行 `timeline_view.py`，並用 `view_file` 檢查圖片是否有：
     - 切點處的視覺跳幀、閃爍或突兀斷裂
     - 切點邊界的波形尖峰（漏網的爆音）
     - 字幕被動畫圖層遮擋（違反硬性規則 1）
     - 動畫時間錯位或顯示錯誤影格（違反硬性規則 4）
   - 抽樣檢查開頭 2s、結尾 2s 及 2～3 個中段點，確認調色一致性与字幕可讀性。
   - 使用 `ffprobe` 驗證輸出總時長符合 EDL 預期，並以 `ffmpeg -i out.mp4 -af ebur128=peak=true -f null -` 量測整合響度（Integrated Loudness）與真峰值（True Peak）。
   - 若發現問題：修正 → 重新渲染 → 重新檢驗（**最多上限 3 次自我檢驗迴圈**；若 3 次後仍有問題則向使用者回報）。
8. **迭代與持久化紀錄 (Iterate + Persist)**：
   - 根據使用者回饋調整 EDL 並重新渲染（絕不重新轉錄已快取之音訊）。確認無誤後輸出最終成品 `final.mp4`，並將工作階段紀錄追加寫入 `<edit>\project.md`。

---

## 剪輯工藝指南 (Cut Craft)

- **音訊優先**：候選切點皆由單詞邊界與靜音間隙決定。
- **保留情緒峰值**：笑聲、金句、語氣強調點。切點應延伸至反應結束之後——笑聲與反應本身就是節拍的一部分。
- **說話者交替（Speaker handoffs）**：保留適當呼吸空間（常見值：400–600 ms；快節奏短片可縮短，紀錄片可拉長）。
- **靜音間隙即最佳切點**：≥ 400 ms 的靜音通常最乾淨；150–400 ms 的片語邊界需搭配 `timeline_view.py` 視覺確認；< 150 ms 不安全（易切在詞句中間）。
- **切點邊界緩衝（Padding）**：例如在保留首詞前留 50 ms、末詞後留 80 ms，維持在 30–200 ms 安全區間內（硬性規則 7）。
- **音畫同步思考**：絕不將音訊與畫面拆開獨立推理，每個切點必須同時在聲音與畫面上自然成立。

---

## 打包逐字稿格式 (`takes_packed.md`)

`pack_transcripts.py` 會讀取所有 `transcripts\*.json` 並產出單一 Markdown 檔案，每個鏡次（Take）包含多行段落級文字，每行開頭皆標註 `[start-end]` 秒數區間。當靜音 ≥ 0.5s 時自動斷行：

```markdown
## C0103  (duration: 43.0s, 8 phrases)
  [002.52-005.36] S0 Ninety percent of what a web agent does is completely wasted.
  [006.08-006.74] S0 We fixed this.
```

---

## 多鏡次挑選 Subagent 任務範本 (Editor Sub-agent Brief)

當任務需要「從大量片段中挑出每個節拍的最佳鏡次並按敘事邏輯組裝」時，可透過 `invoke_subagent` 啟動子代理，提示詞結構如下：

```text
你正在剪輯一部 <類型> 影片。請為每個敘事節拍（Beat）挑選出表現最佳的鏡次（Take），並按照敘事節拍順序組裝，而非按照原始檔名順序。

輸入資訊：
  - takes_packed.md（所有鏡次的時間標註段落逐字稿）
  - 產品/敘事背景：<2 句話背景說明>
  - 講者資訊：<姓名、角色、口條風格>
  - 預期敘事結構：<選擇常見原型或自訂結構>
  - 需避開的口誤清單：<預掃描階段發現的口誤>
  - 目標總時長：<秒數>

常見敘事結構原型（可選用、改編或自創）：
  - 產品發佈 / Demo：HOOK → PROBLEM → SOLUTION → BENEFIT → EXAMPLE → CTA
  - 教學影片：INTRO → SETUP → STEPS → GOTCHAS → RECAP
  - 訪談影片：(QUESTION → ANSWER → FOLLOWUP) 循環
  - 旅遊 / 活動：ARRIVAL → HIGHLIGHTS → QUIET MOMENTS → DEPARTURE
  - 紀錄片：THESIS → EVIDENCE → COUNTERPOINT → CONCLUSION

嚴格規則：
  - start 與 end 時間必須精確落在逐字稿的單詞邊界上。
  - 切點邊界需加上 30–200 ms 緩衝（Padding）。
  - 優先選擇 ≥ 400 ms 的靜音區間作為切點。
  - 若超時，請自行刪減次要節拍或修剪尾部並回報總時長。

輸出格式（純 JSON 陣列，不含多餘文字）：
  [{"source": "C0103", "start": 2.42, "end": 6.85, "beat": "HOOK",
    "quote": "...", "reason": "..."}, ...]
```

---

## 調色指南 (Color Grade)

調色的核心是**觀察畫面並推理**，而非盲目套用濾鏡。先透過 `timeline_view.py` 檢視影格，判斷問題所在，微調後再次檢視。

- **`auto`（預設推薦）**：在 `edl.json` 將 `"grade": "auto"`，由 `grade.py` 對每個片段抽樣計算亮度（YAVG）、動態範圍與飽和度，自動進行 ±8% 以內的曝光與對比微調。
- **`subtle`**：極輕微對比提升與飽和度收斂（`eq=contrast=1.03:saturation=0.98`）。
- **`neutral_punch`**：輕度對比提升 + 柔和 S 曲線，不改變色相。
- **`warm_cinematic`**：復古電影感（+12% 對比、暖暗部與冷亮部），僅在需要強烈風格化時選用。
- **`none`**：不套用任何調色濾鏡。

硬性規定：調色必須在**分段抽取階段（Per-segment extraction）**完成，避免二次編碼。

---

## 字幕指南 (Subtitles)

字幕設計包含三個維度：**分塊字數（Chunking）**、**大小寫（Case）** 與 **垂直邊距（MarginV）**：

- **`bold-overlay`（`render.py` 內建預設）**：適合短影音與快節奏社群影片。約 2–3 詞一組、遇到標點或 ≥ 0.3s 停頓自動斷句、全大寫（中文字元則自動去除字間空白）、Windows 11 預設採用 `Microsoft JhengHei`（微軟正黑體）18 號粗體、白字黑邊、`MarginV=90`（避開 TikTok / Reels / Shorts 底部約 30% 的平台 UI 遮擋區）。
- 若使用者提供自訂 `.srt` 字幕檔，可在 `edl.json` 的 `"subtitles"` 欄位指定路徑。

硬性規定：字幕必須在濾鏡鏈最後一步燒錄（規則 1），且時間戳記必須使用輸出時間軸偏移量（規則 5）。

---

## 動畫疊加指南 (Animations)

若使用者需要資訊字卡、數據動畫或動態圖表疊加：

1. **工具選擇**：
   - **PIL + PNG 序列 + FFmpeg**：最適合計數器、打字機文字、進度條、簡潔資訊字卡。在 Windows 11 環境下無需額外前端依賴、迭代最快且最穩定。在 PIL 中請明確傳入 Windows 字型路徑（如 `C:/Windows/Fonts/msjhbd.ttc` 或 `C:/Windows/Fonts/consola.ttf`），絕不依賴預設字型。
   - **Manim**：適合正式數學推導、狀態機、演算法圖解（請先閱讀 `skills\manim-video\SKILL.md`）。
   - **HyperFrames / Remotion**：適合複雜 Web UI 動態捕捉與 React 組件動畫。
2. **動態曲線（Easing）**：絕不使用機械感的 `linear`，一律使用三次方緩動：
   ```python
   def ease_out_cubic(t: float) -> float:
       return 1.0 - (1.0 - t) ** 3

   def ease_in_out_cubic(t: float) -> float:
       return 4.0 * t ** 3 if t < 0.5 else 1.0 - (-2.0 * t + 2.0) ** 3 / 2.0
   ```
3. **打字機文字定位技巧**：計算文字水平置中時，必須以「完整字串總寬度」作為錨點，而非當前局部字串寬度，否則文字在打出過程中會不斷向左滑動。
4. **平行生成**：多個動畫插槽必須放在 `<edit>\animations\slot_<id>\render.mp4`，並使用 `invoke_subagent` 平行派發給多個子代理同時渲染。

---

## EDL 格式規範 (`edl.json`)

```json
{
  "version": 1,
  "sources": {
    "C0103": "D:/Videos/C0103.MP4",
    "C0108": "D:/Videos/C0108.MP4"
  },
  "ranges": [
    {
      "source": "C0103",
      "start": 2.42,
      "end": 6.85,
      "beat": "HOOK",
      "quote": "...",
      "reason": "口條最清晰，且在 38.46 秒口誤前切斷。"
    },
    {
      "source": "C0108",
      "start": 14.30,
      "end": 28.90,
      "beat": "SOLUTION",
      "quote": "...",
      "reason": "唯一沒有開頭吃螺絲的鏡次。"
    }
  ],
  "grade": "auto",
  "overlays": [
    {
      "file": "animations/slot_1/render.mp4",
      "start_in_output": 0.0,
      "duration": 5.0
    }
  ],
  "subtitles": "master.srt",
  "total_duration_s": 19.03
}
```

---

## 專案記憶持久化 (`project.md`)

每次工作階段結束時，在 `<edit>\project.md` 追加一個段落：

```markdown
## Session N — YYYY-MM-DD

**Strategy:** 一段話描述本次剪輯策略
**Decisions:** 鏡次挑選、切點、調色、動畫決策與原因
**Reasoning log:** 非顯而易見的決策背後之推論紀錄
**Outstanding:** 待辦或下階段微調項目
```

啟動時若發現 `<edit>\project.md` 已存在，請先讀取並以一句話向使用者摘要上次進度，再詢問是否接續剪輯。
