import requests
from bs4 import BeautifulSoup
import os

OUTPUT_FILE = "output/sstp.txt"
URL = "https://www.vpngate.net/en/"

def fetch_html(url):
    print("[INFO] Fetching VPNGate main page...")
    try:
        res = requests.get(url, timeout=15)
        res.raise_for_status()
        return res.text
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None

def parse_sstp_servers(html):
    print("[INFO] Parsing SSTP servers from HTML...")
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", {"id": "vg_hosts_table_id"})
    if not table:
        print("[ERROR] Could not find servers table in page.")
        return []

    servers = []

    # جدول سرورها، هر ردیف (tr) یک سرور است، ردیف اول هدر جدول است
    rows = table.find_all("tr")[1:]

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 15:
            continue

        hostname = cols[1].get_text(strip=True)
        sstp_supported = cols[11].get_text(strip=True)  # ستون LogType (یا ستون SSTP اگر متفاوت است)

        # در صفحه VPNGate ستون 12 (index 11) برای پروتکل‌ها نیست اما ستون 14 یا 15 مربوط به پروتکل‌هاست.
        # بررسی می‌کنیم ستون 13 (index 12) که پروتکل‌ها رو نمایش میده:
        protocols_text = cols[12].get_text(strip=True).lower()
        if 'sstp' in protocols_text:
            port = 443  # پورت پیش‌فرض SSTP معمولاً 443 است
            servers.append(f"{hostname}:{port}")

    return servers

def save_servers(servers, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write("\n".join(servers))
    print(f"[INFO] SSTP server list saved to {filepath}")

def main():
    html = fetch_html(URL)
    if not html:
        return
    sstp_servers = parse_sstp_servers(html)
    print(f"[INFO] Found {len(sstp_servers)} SSTP servers.")
    save_servers(sstp_servers, OUTPUT_FILE)

if __name__ == "__main__":
    main()
