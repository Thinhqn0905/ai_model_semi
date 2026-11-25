"""Capture dashboard screenshots (product readiness evidence).
  python scripts/shoot_dashboard.py --out reports/run4/screenshots
Starts `streamlit run app/dashboard.py` headless on port 8599, opens it in headless Chromium (Playwright), screenshots the landing page and
every sidebar page it can click, then stops the server. No data is created; pages show whatever result files exist locally.
"""
import argparse, subprocess, sys, time
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--out", default="reports/run4/screenshots"); ap.add_argument("--port", type=int, default=8599)
    a = ap.parse_args(); out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    srv = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "app/dashboard.py", "--server.headless", "true",
                            "--server.port", str(a.port), "--browser.gatherUsageStats", "false"],
                           stdout=open(out / "streamlit.log", "w"), stderr=subprocess.STDOUT)
    names = []
    try:
        time.sleep(20)
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1500, "height": 1000})
            pg.goto(f"http://localhost:{a.port}", wait_until="networkidle"); time.sleep(8)
            pg.screenshot(path=str(out / "00_landing.png"), full_page=True); names.append("00_landing.png")
            labels = pg.locator('[data-testid="stSidebar"] label').all_inner_texts()
            for i, lab in enumerate(labels[:15], 1):
                try:
                    pg.locator('[data-testid="stSidebar"] label').nth(i - 1).click(); time.sleep(6)
                    fn = f"{i:02d}_" + "".join(c if c.isalnum() else "_" for c in lab)[:40] + ".png"
                    pg.screenshot(path=str(out / fn), full_page=True); names.append(fn)
                except Exception as e:                       # keep going; record the failure
                    names.append(f"FAILED {lab}: {e!r}"[:200])
            b.close()
    finally:
        srv.terminate()
    (out / "README.md").write_text("# Dashboard screenshots (headless Chromium via Playwright)\n\nCaptured by `python scripts/shoot_dashboard.py`; "
                                   "pages show the result files present locally (no data created).\n\n" + "\n".join(f"- {n}" for n in names) + "\n",
                                   encoding="utf-8")
    print(names)


if __name__ == "__main__":
    main()
