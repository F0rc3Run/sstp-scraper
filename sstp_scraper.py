import requests
import os

def fetch_vpngate_csv():
    url = "http://www.vpngate.net/api/iphone/"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.text.splitlines()
    except Exception as e:
        print(f"[ERROR] Cannot fetch VPNGate CSV: {e}")
        return []

def debug_csv_header_and_sample(csv_lines):
    print("[DEBUG] Showing CSV sample row to identify SSTP column index...")
    for line in csv_lines:
        if line.startswith('*') or ',' not in line:
            continue
        fields = line.strip().split(',')
        print(f"[DEBUG] Sample row with {len(fields)} fields:")
        for idx, val in enumerate(fields):
            print(f"  [{idx}] {val}")
        break

def extract_sstp_servers(csv_lines):
    sstp_servers = []
    for line in csv_lines:
        if line.startswith('*') or ',' not in line:
            continue
        fields = line.strip().split(',')
        if len(fields) < 15:
            continue
        hostname = fields[0]
        try:
            sstp_support = fields[14].strip()  # ممکنه نیاز باشه این عدد رو تغییر بدی بعد از debug
        except IndexError:
            continue
        if sstp_support == '1':
            sstp_servers.append(f"{hostname}:443")
    return sstp_servers

def main():
    print("[INFO] Fetching VPNGate SSTP servers...")
    csv_lines = fetch_vpngate_csv()
    if not csv_lines:
        print("[ERROR] No CSV data received.")
        return

    debug_csv_header_and_sample(csv_lines)  # فقط برای یک‌بار بررسی، بعداً می‌تونی پاکش کنی

    sstp_servers = extract_sstp_servers(csv_lines)
    print(f"[INFO] Found {len(sstp_servers)} SSTP servers.")

    os.makedirs("output", exist_ok=True)
    with open("output/sstp.txt", "w") as f:
        f.write("\n".join(sstp_servers))

    print("[INFO] SSTP server list saved to output/sstp.txt")

if __name__ == "__main__":
    main()
