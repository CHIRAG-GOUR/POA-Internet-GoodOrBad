import sys, os, time
from playwright.sync_api import sync_playwright

# Ensure UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

def test_chapters():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='msedge', headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        console_logs = []
        page.on('console', lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        page.on('pageerror', lambda err: console_logs.append(f"[ERROR] {err}"))

        print("Navigating to http://localhost:5175/index.html ...")
        page.goto("http://localhost:5175/index.html")
        page.wait_for_timeout(2000)

        # Start game
        start_btn = page.query_selector("#startBtn")
        assert start_btn is not None, "startBtn not found"
        print("Start screen found. Clicking startBtn...")
        start_btn.click()
        page.wait_for_timeout(1000)

        def dismiss_dialogue():
            for _ in range(12):
                is_showing = page.evaluate("document.getElementById('dialogue') && document.getElementById('dialogue').classList.contains('show')")
                if not is_showing:
                    break
                page.click("#dNext")
                page.wait_for_timeout(500)
            page.wait_for_timeout(500)

        # --------------------------------------------------------------------
        # TEST CHAPTER 7: Privacy Locker (3D Cyber Vault & Public Profile)
        # --------------------------------------------------------------------
        print("\n=== Testing Chapter 7 (Privacy Locker) ===")
        page.evaluate("loadChapter(6)")
        page.wait_for_timeout(1500)
        dismiss_dialogue()
        
        # Check sorting card
        sort_card = page.query_selector("#sortCard")
        btn_vault = page.query_selector("#btnVault")
        btn_public = page.query_selector("#btnPublic")
        print(f"Privacy UI found: sortCard={sort_card is not None}, btnVault={btn_vault is not None}, btnPublic={btn_public is not None}")

        if btn_vault:
            item_txt = page.query_selector("#itemText").inner_text() if page.query_selector("#itemText") else "N/A"
            print("Item 1 to sort:", item_txt)
            print("Clicking Keep Private (Vault)...")
            btn_vault.click()
            page.wait_for_timeout(1000)
            
            # Check review consequence modal
            rev_modal = page.query_selector("#revModal")
            print("Consequence Review Modal visible:", rev_modal is not None)
            if rev_modal:
                desc = page.query_selector("#revDesc").inner_text() if page.query_selector("#revDesc") else rev_modal.inner_text()
                print("  Consequence Review Description:", desc)
                page.screenshot(path="ch7_consequence_modal.png")
                btn_cont = page.query_selector("#btnRevContinue")
                if btn_cont:
                    btn_cont.click()
                    print("Clicked Continue on Review Modal")
                    page.wait_for_timeout(800)

        page.screenshot(path="ch7_after_sort.png")
        print("Captured ch7_after_sort.png")

        # --------------------------------------------------------------------
        # TEST CHAPTER 8: Scam Alley (Kid's Room & Interactive Chat Window)
        # --------------------------------------------------------------------
        print("\n=== Testing Chapter 8 (Scam Alley) ===")
        page.evaluate("loadChapter(7)")
        page.wait_for_timeout(1500)
        dismiss_dialogue()
        
        chat_win = page.query_selector(".chat-window")
        chat_msgs = page.query_selector("#chatMessages")
        print(f"Chat UI found: chatWin={chat_win is not None}, chatMessages={chat_msgs is not None}")
        
        reply_opts = page.query_selector_all(".chat-opt-btn")
        print(f"Found {len(reply_opts)} reply options in chat window.")
        for idx, opt in enumerate(reply_opts):
            print(f"  Option {idx+1}: {opt.inner_text()}")
            
        if len(reply_opts) > 1:
            print("Selecting Option 2 (Block & Report)...")
            reply_opts[1].click()
            page.wait_for_timeout(1800)

        page.screenshot(path="ch8_chat_replied.png")
        print("Captured ch8_chat_replied.png")

        # --------------------------------------------------------------------
        # TEST CHAPTER 10: Truth Lab (Dual Live Meters & Detective Rating)
        # --------------------------------------------------------------------
        print("\n=== Testing Chapter 10 (Truth Lab) ===")
        page.evaluate("loadChapter(9)")
        page.wait_for_timeout(1500)
        dismiss_dialogue()

        truth_bar = page.query_selector("#truthBar")
        false_bar = page.query_selector("#falseBar")
        truth_pct = page.query_selector("#truthPct")
        false_pct = page.query_selector("#falsePct")
        print(f"Truth Lab UI found: truthBar={truth_bar is not None}, falseBar={false_bar is not None}")

        if truth_pct and false_pct:
            print(f"Initial Meters -> Truth: {truth_pct.inner_text()}, Falsehood: {false_pct.inner_text()}")

        truth_opts = page.query_selector_all(".truth-opt-btn")
        print(f"Found {len(truth_opts)} forensic option buttons.")
        for idx, opt in enumerate(truth_opts):
            print(f"  Option {idx+1}: {opt.inner_text()}")
            
        if len(truth_opts) > 1:
            print("Selecting Option 2 (Debunk as Fake)...")
            truth_opts[1].click()
            page.wait_for_timeout(1800)
            if truth_pct and false_pct:
                print(f"Updated Meters -> Truth: {truth_pct.inner_text()}, Falsehood: {false_pct.inner_text()}")

        page.screenshot(path="ch10_meter_updated.png")
        print("Captured ch10_meter_updated.png")

        print("\nConsole errors (if any):")
        errors = [log for log in console_logs if "[ERROR]" in log or "[error]" in log]
        for err in errors:
            print(err)
        if not errors:
            print("No console errors detected! ALL CLEAN!")

        browser.close()

if __name__ == '__main__':
    test_chapters()
