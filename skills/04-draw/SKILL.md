---
name: antigravity-draw
description: AntiGravity 內建生圖技能。當使用者要求「畫一張」、「生一張圖」、「做一張圖」、「產生圖片」、「畫個封面」、「畫插圖」、「畫示意圖」、「畫分鏡」等任何需要生成或編輯圖像的情境時載入。
---

# 內建生圖技能（generate_image）

當使用者要求生成、畫圖或修改圖片時，必須使用此技能。

## 觸發情境
使用者輸入包含以下關鍵字或意圖：
- 「畫一張 XX」、「生一張圖」、「做一張圖」
- 「畫個封面／插圖／示意圖／分鏡」
- 「產生圖片」、「幫我生圖」

## 使用方式
直接呼叫系統內建的 `generate_image` 工具。

### 工具參數說明
- **Prompt**（必要）：描述要生成的圖像內容。
- **ImageName**（必要）：生成的圖像檔名（全小寫、底線連接，最多 3 個英文單字，例如 `cover_mockup`）。
- **ImagePaths**（選填）：若需要修改或基於現有圖片生成，傳入現有圖片的絕對路徑。

## 生圖提示詞（Prompt）優化原則
為了發揮底線模型（Gemini 2.5 Flash Image / Nano Banana）的最大效能，請在 `Prompt` 中使用以下結構化描述：
1. **主體（Subject）**：人、事、物之詳細特徵描述。
2. **場景背景（Background/Setting）**：環境、光影、氛圍。
3. **藝術風格（Style）**：例如：Sleek 3D Render, Vibrant Illustration, Minimalist Vector Art, Photorealistic 等。
4. **色彩與色調（Color Palette）**：特定配色調性。

## 檔案存取規範
1. 預設生圖結果會作為 Artifact 儲存在當前對話的 Artifacts 目錄中。
2. 若使用者有特定輸出目錄要求（如 `./assets/` 或 `./generated/`），請在生成後，利用系統指令或檔案工具將其複製或移動至指定專案目錄中。
