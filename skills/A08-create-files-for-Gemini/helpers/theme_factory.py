"""
Theme Factory — 專業主題配色工廠 (A08-create-files-for-Gemini)
提供 10 套經過專業視覺設計之商務、科技、永續與人文色彩調色盤，
為 Word (.docx)、PowerPoint (.pptx)、Excel (.xlsx) 與 PDF (.pdf) 提供跨文件格式的統一視覺風格。
"""

THEMES = {
    "midnight_executive": {
        "name": "Midnight Executive（午夜高階）",
        "description": "經典海軍藍與冰藍搭配，穩健沉著，極具權威感",
        "best_for": "主管匯報、正式合約、財報分析、商業企劃書",
        "primary": "1E2761",      # 海軍藍
        "secondary": "CADCFC",    # 冰藍
        "accent": "FFFFFF",       # 極致白
        "dark_neutral": "10163A", # 墨藍黑
        "light_neutral": "F4F6FB",# 冰白灰
        "card_bg": "F0F4FA",
        "zebra_row": "F8F9FD"
    },
    "forest_moss": {
        "name": "Forest & Moss（森林苔蘚）",
        "description": "深林綠與苔蘚綠交織，沉穩自然，象徵生生不息與永續成長",
        "best_for": "ESG 永續報告、農業生技、教育訓練、環境政策",
        "primary": "2C5F2D",      # 深林綠
        "secondary": "97BC62",    # 苔蘚綠
        "accent": "F5F5F5",       # 奶油白
        "dark_neutral": "1E3B1F",
        "light_neutral": "F7F9F6",
        "card_bg": "F1F5EF",
        "zebra_row": "F8FAF7"
    },
    "teal_trust": {
        "name": "Teal Trust（青碧信任）",
        "description": "青碧藍與海泡綠調和，傳遞高度專業、數據信任與前瞻性",
        "best_for": "科技金融 (FinTech)、SaaS 軟體規劃、資安防護、數據科學",
        "primary": "028090",      # 青碧藍
        "secondary": "00A896",    # 海泡綠
        "accent": "02C39A",       # 薄荷綠
        "dark_neutral": "013D45",
        "light_neutral": "F2F9F9",
        "card_bg": "EAF5F5",
        "zebra_row": "F5FAFA"
    },
    "ocean_gradient": {
        "name": "Ocean Gradient（深海漸層）",
        "description": "深海藍與午夜暗藍搭配，大氣深邃，展現深厚技術實力",
        "best_for": "技術白皮書、工程技術規格書、學術研討、長篇分析",
        "primary": "065A82",      # 深海藍
        "secondary": "1C7293",    # 水藍綠
        "accent": "21295C",       # 午夜藍
        "dark_neutral": "0E1A38",
        "light_neutral": "F0F6F9",
        "card_bg": "E8F1F5",
        "zebra_row": "F4F8FA"
    },
    "charcoal_minimal": {
        "name": "Charcoal Minimal（極簡碳黑）",
        "description": "碳灰與純淨白對比，乾淨俐落，極致現代主義",
        "best_for": "建築營造、工業設計、法律文件、高端品牌提案",
        "primary": "36454F",      # 碳灰
        "secondary": "708090",    # 板岩灰
        "accent": "212121",       # 墨黑
        "dark_neutral": "1A2024",
        "light_neutral": "F8F9FA",
        "card_bg": "F0F2F4",
        "zebra_row": "F6F7F8"
    },
    "warm_terracotta": {
        "name": "Warm Terracotta（大地陶土）",
        "description": "暖陶土紅與暖沙色結合，溫潤大氣，蘊含豐富人文溫度",
        "best_for": "文化創意、非營利組織、人力資源、社會福祉專案",
        "primary": "B85042",      # 陶土紅
        "secondary": "E7E8D1",    # 暖沙色
        "accent": "A7BEAE",       # 灰綠
        "dark_neutral": "4A1E18",
        "light_neutral": "FAF8F5",
        "card_bg": "F5F0EB",
        "zebra_row": "FAF7F5"
    },
    "coral_energy": {
        "name": "Coral Energy（珊瑚活力）",
        "description": "亮眼珊瑚紅與活力金黃，充滿熱情、驅動力與現代感",
        "best_for": "新創融資簡報 (Pitch Deck)、行銷發布會、激勵提案、大眾文宣",
        "primary": "F96167",      # 珊瑚紅
        "secondary": "F9E795",    # 陽光金
        "accent": "2F3C7E",       # 深海軍藍
        "dark_neutral": "1F2752",
        "light_neutral": "FFFDF5",
        "card_bg": "FFF8EB",
        "zebra_row": "FFFAF0"
    },
    "berry_cream": {
        "name": "Berry & Cream（莓果醇厚）",
        "description": "深醇莓紫搭配乾燥玫瑰與奶油色，高貴精緻且富有層次",
        "best_for": "生活品味、精品時尚、公關活動企劃、女性消費趨勢報告",
        "primary": "6D2E46",      # 深莓紫
        "secondary": "A26769",    # 乾燥玫瑰
        "accent": "ECE2D0",       # 象牙白
        "dark_neutral": "3D1726",
        "light_neutral": "FAF6F7",
        "card_bg": "F5ECF0",
        "zebra_row": "F9F3F6"
    },
    "sage_calm": {
        "name": "Sage Calm（鼠尾草寧靜）",
        "description": "鼠尾草灰綠與尤加利綠結合，清新舒緩，撫平視覺焦慮",
        "best_for": "生技醫療、身心健康、諮商輔導手冊、使用者體驗 (UX) 研究",
        "primary": "84B59F",      # 鼠尾草灰綠
        "secondary": "69A297",    # 尤加利綠
        "accent": "50808E",       # 板岩藍
        "dark_neutral": "264239",
        "light_neutral": "F4F8F6",
        "card_bg": "EBF3F0",
        "zebra_row": "F3F7F5"
    },
    "cherry_bold": {
        "name": "Cherry Bold（櫻桃醒目）",
        "description": "深櫻桃紅搭配純米白與深暗對比，視覺衝擊力強大，醒目警示",
        "best_for": "重大里程碑成果、重大風險預警指引、關鍵競賽提案",
        "primary": "990011",      # 櫻桃紅
        "secondary": "FCF6F5",    # 純淨米白
        "accent": "2F3C7E",       # 對比深藍
        "dark_neutral": "4A0008",
        "light_neutral": "FDF9F9",
        "card_bg": "F9EDEE",
        "zebra_row": "FAF2F3"
    }
}

def hex_to_rgb(hex_str):
    """將 6 碼 Hex 字串轉為 (r, g, b) 整數 Tuple"""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def get_theme(theme_key="midnight_executive"):
    """取得指定之調色盤字典，若未對應則預設返回 midnight_executive"""
    key = str(theme_key).lower().replace('-', '_').replace(' ', '_')
    for k, v in THEMES.items():
        if key in k or k in key:
            return v
    return THEMES["midnight_executive"]

def list_themes_summary():
    """列印所有主題供使用者選配"""
    summary = []
    for k, v in THEMES.items():
        summary.append({
            "key": k,
            "name": v["name"],
            "description": v["description"],
            "best_for": v["best_for"],
            "primary": f"#{v['primary']}",
            "secondary": f"#{v['secondary']}"
        })
    return summary
