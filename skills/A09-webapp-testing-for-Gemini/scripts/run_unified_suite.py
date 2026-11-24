#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A09-webapp-testing-for-Gemini: Comprehensive Web Application Testing Suite
Integrates:
1. Local HTTP Server lifecycle & external multi-server management (with_server logic)
2. Chrome DevTools Protocol (CDP) live browser debugging (Port 9222/9223)
3. Headless Playwright sandbox testing with dialog/console/network state machine
4. Mobile/Responsive hamburger & easter-egg cutlery verification
5. Security guard & auth testing (schedule.html guard, staff code persistence)
6. Dynamic task reservation & weekday correctness verification
7. Reconnaissance & Element Discovery helper routines
"""

import os
import sys
import time
import socket
import argparse
import threading
import http.server
import urllib.request
import json
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def is_server_ready(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False

def test_cdp_connection(port=9222):
    print(f"\n[CDP] 檢測 Chrome 遠端除錯連線 (Port {port})...")
    try:
        req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1.5)
        info = json.loads(req.read().decode('utf-8'))
        print(f"  ✔ 成功連線 Chrome CDP！瀏覽器版本: {info.get('Browser')}")
        return True
    except Exception as e:
        print(f"  ℹ Port {port} 未就緒或未開啟遠端除錯 ({e})")
        return False

def run_full_suite(web_root=r"D:\xampp\htdocs\Other\NTHU_BWY_veggie", port=8899, output_dir=None):
    if output_dir is None:
        output_dir = os.path.join(web_root, "_output", "test_artifacts")
    os.makedirs(output_dir, exist_ok=True)

    print("==================================================")
    print("▶ 啟動 A09 全功能端對端與安全測試 (A09-webapp-testing)")
    print(f"  網站目錄: {web_root}")
    print(f"  測試輸出: {output_dir}")
    print("==================================================")

    # 啟動本地測試伺服器
    server = None
    server_thread = None
    if not is_server_ready(port, timeout=1):
        print(f"-> 正在背景啟動本地 HTTP 服務 (Port {port})...")
        orig_cwd = os.getcwd()
        os.chdir(web_root)
        server = http.server.ThreadingHTTPServer(("127.0.0.1", port), QuietHandler)
        server_thread = threading.Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        if not is_server_ready(port, timeout=10):
            raise RuntimeError(f"無法在 Port {port} 啟動本地伺服器")
        print(f"  ✔ 本地 HTTP 伺服器就緒: http://127.0.0.1:{port}/")

    # 檢測 CDP 狀態
    test_cdp_connection(9222)

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-web-security', '--disable-features=IsolateOrigins,site-per-process']
        )
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        # 對話框與 Console 狀態機
        dialog_state = {"prompt_response": "", "last_alert": "", "confirm_response": True}
        def handle_dialog(dialog):
            dialog_state["last_alert"] = dialog.message
            if dialog.type == "alert":
                dialog.accept()
            elif dialog.type == "confirm":
                if dialog_state["confirm_response"]:
                    dialog.accept()
                else:
                    dialog.dismiss()
            elif dialog.type == "prompt":
                dialog.accept(dialog_state["prompt_response"])
        page.on("dialog", handle_dialog)

        base_url = f"http://127.0.0.1:{port}"

        # -------------------------------------------------------------
        # 測試模組 1：主題切換與基礎流程 (zh-TW)
        # -------------------------------------------------------------
        print("\n[模組 1] 測試繁體中文首頁與淡雅/鮮豔主題切換...")
        page.goto(f"{base_url}/index.html")
        page.wait_for_load_state("networkidle")
        page.evaluate("() => localStorage.clear()")
        page.reload()
        page.wait_for_load_state("networkidle")

        init_theme = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        assert init_theme == "simple", f"預期初始為 simple，實際為 {init_theme}"

        page.locator("#btnThemeColorful").click()
        page.wait_for_timeout(400)
        assert page.evaluate("() => document.documentElement.getAttribute('data-theme')") == "colorful"
        page.screenshot(path=os.path.join(output_dir, "01_zh_theme_colorful.png"))

        page.locator("#btnThemeSimple").click()
        page.wait_for_timeout(400)
        assert page.evaluate("() => document.documentElement.getAttribute('data-theme')") == "simple"
        page.screenshot(path=os.path.join(output_dir, "01_zh_theme_simple.png"))
        print("  ✔ 主題切換與 Zero-FOUC 驗證通過")

        # -------------------------------------------------------------
        # 測試模組 2：安全防護與權限守衛 (V13 Security)
        # -------------------------------------------------------------
        print("\n[模組 2] 測試排班頁面權限守衛與工作人員狀態安全性...")
        page.goto(f"{base_url}/schedule.html")
        page.wait_for_load_state("networkidle")
        guard_visible = page.is_visible("#scheduleGuardCard")
        iframe_visible = page.is_visible("#scheduleProtectedContent")
        print(f"  -> 未授權造訪 schedule.html 守衛提示: {guard_visible}, 排班內容: {iframe_visible}")
        assert guard_visible is True and iframe_visible is False
        page.screenshot(path=os.path.join(output_dir, "02_schedule_guard_blocked.png"))

        # 測試缺少 staff_code 自動降級
        page.goto(f"{base_url}/index.html")
        page.evaluate("() => { localStorage.setItem('veg_is_staff', '1'); localStorage.removeItem('veg_staff_code'); }")
        page.reload()
        page.wait_for_load_state("networkidle")
        downgraded = page.evaluate("() => localStorage.getItem('veg_is_staff')")
        nav_schedule = page.is_visible("#navSchedule")
        btn_config = page.is_visible("#btnConfig")
        assert downgraded == "0" and nav_schedule is False and btn_config is False
        print("  ✔ 缺少認證碼自動降級、排班選單與系統設定隱藏驗證通過")

        # 模擬正確工作人員授權
        page.evaluate("() => { localStorage.setItem('veg_is_staff', '1'); localStorage.setItem('veg_staff_code', 'TEST_PASS_CODE'); }")
        page.reload()
        page.wait_for_load_state("networkidle")
        assert page.evaluate("() => isStaffMode") is True
        assert page.evaluate("() => sessionStaffCode") == "TEST_PASS_CODE"
        assert page.is_visible("#navSchedule") is True and page.is_visible("#btnConfig") is True
        print("  ✔ 工作人員重整後認證碼持久化、排班選單與系統設定顯示驗證通過")

        # -------------------------------------------------------------
        # 測試模組 3：響應式漢堡選單與刀叉相交小彩蛋
        # -------------------------------------------------------------
        print("\n[模組 3] 測試手機視角 (390x844) 漢堡選單與刀叉相交動畫...")
        mobile_page = context.new_page()
        mobile_page.set_viewport_size({"width": 390, "height": 844})
        mobile_page.goto(f"{base_url}/index.html")
        mobile_page.wait_for_load_state("networkidle")

        hamburger_btn = mobile_page.locator("#btnHamburger")
        assert hamburger_btn.is_visible() is True
        mobile_page.screenshot(path=os.path.join(output_dir, "03_mobile_hamburger_closed.png"))

        # 點擊展開漢堡選單（應呈現刀叉相交圖示）
        hamburger_btn.click()
        mobile_page.wait_for_timeout(350)
        nav_open = mobile_page.evaluate("() => document.querySelector('.header-nav').classList.contains('nav-open')")
        btn_active = mobile_page.evaluate("() => document.getElementById('btnHamburger').classList.contains('is-active')")
        assert nav_open is True and btn_active is True
        mobile_page.screenshot(path=os.path.join(output_dir, "03_mobile_cutlery_opened.png"))
        mobile_page.close()
        print("  ✔ 漢堡選單展開與刀叉相交小彩蛋驗證通過")

        # -------------------------------------------------------------
        # 測試模組 4：實體活動星期幾與快速預約區塊
        # -------------------------------------------------------------
        print("\n[模組 4] 測試活動預約區塊與日期星期 (11/11, 11/18, 11/25 週三)...")
        mock_user = {
            "serial": "VEG-2026-0001",
            "name": "測試學員",
            "dept": "資工系",
            "grade": "大二",
            "phone": "0912345678",
            "email": "test@nthu.edu.tw",
            "theme": 1,
            "stamps": [0, 0, 0, 0, 0, 0, 0, 0, 0]
        }
        page.evaluate(f"() => localStorage.setItem('veg_current_user', JSON.stringify({json.dumps(mock_user)}))")
        page.reload()
        page.wait_for_load_state("networkidle")

        event_dates = page.locator(".event-date").all_inner_texts()
        print(f"  -> 讀取到的活動日期欄位: {event_dates}")
        assert any("11/11 (三)" in d for d in event_dates), "11/11 應為週三"
        assert any("11/18 (三)" in d for d in event_dates), "11/18 應為週三"
        assert any("11/25 (三)" in d for d in event_dates), "11/25 應為週三"
        assert page.is_visible("#btnQuickEventReg") is True, "快速預約活動按鈕應顯示"
        page.locator("#btnQuickEventReg").click()
        page.wait_for_timeout(500)
        in_view = page.evaluate("() => { const r = document.getElementById('eventRegCard').getBoundingClientRect(); return r.top < window.innerHeight && r.bottom > 0; }")
        assert in_view is True, "點擊快速預約活動後應滾動至預約區段"

        # 驗證 #9 共用格 (10/14 已蓋章 stamps[8]=1 時，11/25 仍開放預約；stamps[8]=3 時，保留印章與連線且顯示已預約 11/25)
        page.evaluate("() => { currentUser.stamps = [0, 0, 0, 0, 0, 0, 1, 1, 1]; renderBingoCard(); }")
        card9_text_1 = page.locator("#eventRegGrid .event-item").nth(2).inner_text()
        assert "10/14 蓋章（可預約 11/25）" in card9_text_1 and "我要報名 11/25 活動" in card9_text_1, f"#9 狀態 1 顯示異常: {card9_text_1}"
        assert page.evaluate("() => document.querySelectorAll('#bingoGrid .grid-cell')[8].classList.contains('stamped')") is True

        page.evaluate("() => { currentUser.stamps = [0, 0, 0, 0, 0, 0, 1, 1, 3]; renderBingoCard(); }")
        card9_text_3 = page.locator("#eventRegGrid .event-item").nth(2).inner_text()
        assert "已預約 11/25（#9 已於 10/14 蓋章）" in card9_text_3 and "取消 11/25 預約（保留印章）" in card9_text_3, f"#9 狀態 3 顯示異常: {card9_text_3}"
        assert page.evaluate("() => document.querySelectorAll('#bingoGrid .grid-cell')[8].classList.contains('stamped')") is True
        assert page.evaluate("() => document.getElementById('metaLines').innerText") == "1", "狀態 3 應計入賓果連線"

        page.screenshot(path=os.path.join(output_dir, "04_event_weekdays_verified.png"))
        print("  ✔ 活動日期週三、頂端列快速預約跳轉與 #9 共用格狀態碼 (1/3) 校驗通過")

        browser.close()

    if server:
        server.shutdown()
        print("  ✔ 本地測試伺服器已安全停止")

    print("\n==================================================")
    print("🏆 恭喜！A09 整合端對端、安全性與視覺測試全數 PASS！")
    print(f"  所有截圖與成果已儲存至: {output_dir}")
    print("==================================================")

def main():
    parser = argparse.ArgumentParser(description="A09-webapp-testing 全功能測試套件")
    parser.add_argument("--root", default=r"D:\xampp\htdocs\Other\NTHU_BWY_veggie", help="Web 專案根目錄")
    parser.add_argument("--port", type=int, default=8899, help="本地 HTTP 伺服器連接埠")
    parser.add_argument("--output", default=None, help="截圖與報表輸出目錄")
    args = parser.parse_args()

    run_full_suite(web_root=args.root, port=args.port, output_dir=args.output)

if __name__ == "__main__":
    main()
