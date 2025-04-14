from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep

def visit(base, path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-jit")
    chrome_options.add_argument("--disable-wasm")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.binary_location = "/usr/bin/chromium"

    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(5)

    driver.get(base + "/a")
    driver.add_cookie({
        "name": "token",
        "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaXNfYWRtaW4iOnRydWV9.9fzUQML_O2T0PmAvkBDXoa21xzRYrbS2ZwmmaLoLFYU",
        "path": "/",
        "httpOnly": True,
        "samesite": "Strict",
        "domain": "127.0.0.1"
    })
    try:
        driver.get(base + path)
        # print(driver.page_source)
    except: pass

    sleep(3)
    driver.close()

# visit("http://127.0.0.1:5001/panel")