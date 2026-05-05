from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin, urlparse
from collections import deque
import time
import random

BASE_URL = "https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/"
OUTPUT_DIR = Path("./cfn-docs-text")
OUTPUT_DIR.mkdir(exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

def get_filename(url):
    path = urlparse(url).path
    name = path.rstrip("/").split("/")[-1]
    if not name or not name.endswith(".html"):
        name = "index"
    return name.replace(".html", ".txt")

visited = set()

# すでに保存済みのファイルをvisitedに追加（再実行時の重複スキップ）
for f in OUTPUT_DIR.glob("*.txt"):
    visited.add(f.stem)

queue = deque([BASE_URL])
count = 0

try:
    while queue:
        url = queue.popleft()

        if url in visited:
            continue
        visited.add(url)

        try:
            driver.get(url)
            time.sleep(2)

            soup = BeautifulSoup(driver.page_source, "html.parser")

            main = soup.find("div", {"id": "main-content"}) or soup.find("main")
            if main:
                text = main.get_text(separator="\n", strip=True)
                filename = get_filename(url)
                (OUTPUT_DIR / filename).write_text(text, encoding="utf-8")
                count += 1
                print(f"保存: {filename} ({count}ページ目)")

            for a in soup.find_all("a", href=True):
                href = urljoin(url, a["href"]).split("#")[0]
                if href.startswith(BASE_URL) and href not in visited:
                    queue.append(href)

        except Exception as e:
            print(f"エラー: {url} {e}")

        time.sleep(random.uniform(0.5, 1.0))

finally:
    driver.quit()

print("完了")