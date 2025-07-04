import os
import requests
from bs4 import BeautifulSoup

def fetch_sstp_servers():
    print("[INFO] Fetching VPNGate main page...")
    url = "https://www.vpngate.net/en/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
    return response.text

def parse_html_for_sstp(html):
    print("[INFO] Parsing SSTP servers from HTML...")
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "vg_hosts_table_id"})
    if not table:
        print("[ERROR] Table with SSTP info not found.")
        return []

    sstp_servers = []

    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 1:
            continue

        sstp_cell = None
        for cell in cells:
            if "SSTP" in cell.text:
                sstp_cell = cell
                break

        if sstp_cell and "sstp://" in sstp_cell.text.lower():
            # Try to extract hostname and port from nearby cell
            host_info = cells[0].text.strip()
            if ".opengw.net" in host_info:
                port = "443"  # Default SSTP port if not specified
                if ':' in host_info:
                    host_info, port = host_info.split(':', 1)
                sstp_servers.append(f"{host_info}:{port}")

    return list(set(sstp_servers))

def save_to_file(servers, path="output/sstp.txt"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write("\n".join(servers))
    print(f"[INFO] SSTP server list saved to {path}")

def main():
    html = fetch_sstp_servers()
    sstp_servers = parse_html_for_sstp(html)
    print(f"[INFO] Found {len(sstp_servers)} SSTP servers.")
    save_to_file(sstp_servers)

if __name__ == "__main__":
    main()
