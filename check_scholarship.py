import requests
from bs4 import BeautifulSoup
import hashlib

URL = "https://www.isc.kyushu-u.ac.jp/intlweb/scholarship_jp/view/list.php"

def get_page_hash():
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def send_slack_message(text):
    import os
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    requests.post(webhook_url, json={"text": text})

def main():
    hash_file = "last_hash.txt"
    new_hash = get_page_hash()

    try:
        with open(hash_file, "r") as f:
            old_hash = f.read().strip()
    except FileNotFoundError:
        old_hash = ""

    if new_hash != old_hash:
        send_slack_message(f"🎓 奨学金情報が更新されました！\n{URL}")
        with open(hash_file, "w") as f:
            f.write(new_hash)
    else:
        print("No update detected.")

if __name__ == "__main__":
    main()
