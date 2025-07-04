import requests
import os

OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "sstp.txt")

def fetch_vpngate_csv():
    url = "http://www.vpngate.net/api/iphone/"
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        content = r.text
        return content.splitlines()
    except Exception as e:
        print(f"[ERROR] Failed to fetch VPNGate CSV: {e}")
        return []

def extract_sstp_servers(csv_lines):
    servers = []
    # خط اول هدر و خط دوم توضیحات هست، از خط سوم شروع کن
    for line in csv_lines[2:]:
        if line.startswith("#") or line.strip() == "":
            continue
        fields = line.split(",")
        # مطمئن شو طول فیلدها کافی است
        if len(fields) < 15:
            continue

        hostname = fields[0].strip()
        # فیلد 12: LogType (SSTP=4)
        log_type = fields[11].strip()
        # فیلد 1: IP
        ip = fields[1].strip()
        # فیلد 14: OpenVPN_ConfigData_Base64 ولی برای SSTP باید port رو بگیریم
        # VPNGate در CSV پورت‌ها را مستقیم نمی‌دهد؛ فرض کنیم همیشه 443 یا پورت SSTP پیش‌فرض است.
        # چون پورت SSTP معمولاً 443 است، استفاده میکنیم.

        if log_type == "4":  # SSTP
            # به صورت examplehostname:port ذخیره می‌کنیم، پورت 443 پیش‌فرض SSTP است
            servers.append(f"{hostname}:443")

    return servers

def main():
    print("[INFO] Fetching VPNGate SSTP servers...")
    csv_lines = fetch_vpngate_csv()
    if not csv_lines:
        print("[ERROR] No CSV data fetched.")
        return

    sstp_servers = extract_sstp_servers(csv_lines)
    print(f"[INFO] Found {len(sstp_servers)} SSTP servers.")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        for server in sstp_servers:
            f.write(server + "\n")

    print(f"[INFO] SSTP server list saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
