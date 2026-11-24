import os
import sys
import json
import argparse
import shutil

def main():
    parser = argparse.ArgumentParser(description="AntiGravity 內建生圖轉接腳本")
    parser.add_argument("prompt", type=str, help="生圖提示詞")
    parser.add_argument("--name", type=str, default="generated_img", help="輸出檔名前綴")
    parser.add_argument("--outdir", type=str, default=".", help="輸出目錄")
    parser.add_argument("--size", type=str, default="1024x1024", help="比例尺寸 (此參數於內建工具中將自動對應最佳解析度)")
    parser.add_argument("--quality", type=str, default="low", help="品質等級 (內建生圖不扣除 OpenAI 額度)")
    parser.add_argument("--n", type=int, default=1, help="生成張數")
    
    args = parser.parse_args()
    
    # 由於此腳本為 CLI 介面，當使用者透過終端機執行時，
    # 提醒使用者與 AntiGravity AI 助理直接對話即可完成高品質生圖。
    print(f"提示詞: {args.prompt}")
    print(f"檔名: {args.name}")
    print(f"輸出路徑: {args.outdir}")
    print("\n[提示] 您正使用 AntiGravity 2.0！不需要外接 API 即可生圖。")
    print("請直接在 AI 對話框中輸入您的生圖需求（例如：「畫一隻穿西裝的龍蝦」），")
    print("系統將自動呼叫底層強大的 Nano Banana 模型為您生成，並展示在介面中。")

if __name__ == "__main__":
    main()
