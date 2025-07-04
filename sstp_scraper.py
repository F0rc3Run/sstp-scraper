import requests
import csv
import base64
import os

def fetch_vpngate_csv():
    url = "https://www.vpngate.net/api/iphone/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}")
    lines = response.text.strip().splitlines()
    return lines[2:]  # Skip first two lines (header/comment)

def extract_sstp_servers(csv_lines):
    sstp_servers = []
    for line in csv_lines:
        if line.startswith('*') or ',' not in line:
            continue
        fields = line.split(',')
        if len(fields) < 16:  # بررسی ایمنی
            continue
        hostname = fields[0]
        port = fields[15]
        if port.strip().isdigit():
            sstp_servers.append(f"{hostname}:{port.strip()}")
    return sstp_servers

def save_to_files(servers):
    os.makedirs("bot_data", exist_ok=True)
    with open("sstp_servers.txt", "w") as f1, open("bot_data/sstp.txt", "w") as f2:
        joined = "\n".join(servers)
        f1.write(joined)
        f2.write(joined)

def main():
    print("[INFO] Fetching VPNGate SSTP servers...")
    csv_lines = fetch_vpngate_csv()
    sstp_servers = extract_sstp_servers(csv_lines)
    print(f"[INFO] Found {len(sstp_servers)} SSTP servers.")
    save_to_files(sstp_servers)

if __name__ == "__main__":
    main()
