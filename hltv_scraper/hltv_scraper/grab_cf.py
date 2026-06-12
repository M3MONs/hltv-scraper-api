import asyncio
import json
from pathlib import Path

import nodriver as uc

CF_TARGET_URL = "https://www.hltv.org/stats"
CF_SESSION_FILE = Path(__file__).resolve().parents[1] / "cf_session.json"


async def grab_cf_session():
    browser = await uc.start(headless=False)
    tab = await browser.get(CF_TARGET_URL)
    print("Waiting for cf_clearance... (solve the challenge in the browser window if it appears)")

    for _ in range(180):
        cookies = await browser.cookies.get_all()
        cf = next((c for c in cookies if c.name == "cf_clearance"), None)
        if cf:
            ua = await tab.evaluate("navigator.userAgent")
            CF_SESSION_FILE.write_text(
                json.dumps({"cf_clearance": cf.value, "user_agent": ua}, indent=2)
            )
            print(f"Saved session to {CF_SESSION_FILE}")
            break
        await asyncio.sleep(1)
    else:
        print("Failed to obtain cf_clearance within 3 minutes.")

    browser.stop()


if __name__ == "__main__":
    uc.loop().run_until_complete(grab_cf_session())