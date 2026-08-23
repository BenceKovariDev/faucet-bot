import os
import requests
from bs4 import BeautifulSoup

EMAIL = os.environ.get("FC_EMAIL")
PASSWORD = os.environ.get("FC_PASS")

print("--- GitHub Actions API / HTTP Bot Indul ---")

# Munkamenet létrehozása a sütik (cookies) megőrzéséhez
session = requests.Session()

# Alap fejrészek (headers), hogy normális böngészőnek tűnjön a kérés
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7"
})

try:
    print("1. Bejelentkezési oldal lekérése...")
    login_page = session.get("https://faucetcrypto.com/login")
    
    # BeautifulSoup segítségével kereshetünk biztonsági tokeneket (CSRF token), ha az oldal kérni szokta
    soup = BeautifulSoup(login_page.text, 'html.parser')
    
    # Megpróbáljuk elküldeni a POST kérést a bejelentkezési adatokkal
    # Megjegyzés: Ha a Faucetcrypto Cloudflare védettsége megállítja a tiszta HTTP kérést, 
    # azt a válasz státuszkódjából (pl. 403 vagy 503) fogjuk látni.
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    print("2. Bejelentkezési adatok küldése...")
    response = session.post("https://faucetcrypto.com/login", data=payload, allow_redirects=True)
    
    print(f"Válasz státuszkód: {response.status_code}")
    print(f"Aktuális válasz URL: {response.url}")
    
    if "dashboard" in response.url or response.status_code == 200:
        print("A kérés lefutott. Ellenőrizzük a fiók állapotát...")
        # Itt lekérhetjük a PTC oldalakat
        ptc_page = session.get("https://faucetcrypto.com/dashboard/ptc")
        print(f"PTC oldal státusz: {ptc_page.status_code}")
    else:
        print("A Cloudflare vagy a szerver blokkolta a kérést (védelem aktív).")

except Exception as e:
    print(f"Hiba történt a kérés során: {e}")

print("Folyamat kész.")import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

EMAIL = os.environ.get("FC_EMAIL")
PASSWORD = os.environ.get("FC_PASS")

print("--- GitHub Actions FaucetCrypto Bot Indul ---")

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

if os.path.exists("/usr/bin/google-chrome"):
    options.binary_location = "/usr/bin/google-chrome"
elif os.path.exists("/opt/google/chrome/chrome"):
    options.binary_location = "/opt/google/chrome/chrome"

try:
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    print("Megnyitom a bejelentkezési oldalt...")
    driver.get("https://faucetcrypto.com/login")
    
    wait = WebDriverWait(driver, 25)
    
    print("Várakozás az e-mail mezőre...")
    # Biztosabb keresés input típus vagy név alapján
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @name='email']")))
    email_field.clear()
    email_field.send_keys(EMAIL)
    
    print("Jelszó mező kitöltése...")
    password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password' or @name='password']")))
    password_field.clear()
    password_field.send_keys(PASSWORD)
    
    time.sleep(1)
    
    print("Kattintás a Bejelentkezés gombra...")
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' or contains(text(), 'Bejelentkezés')]")))
    login_button.click()
    
    print("Várakozás a bejelentkezés utáni betöltésre...")
    time.sleep(8)
    
    print(f"Aktuális URL: {driver.current_url}")
    
    if "dashboard" in driver.current_url:
        print("Sikeres belépés a Dashboardra!")
        driver.get("https://faucetcrypto.com/dashboard/ptc")
        time.sleep(5)
    else:
        print("A bejelentkezés valószínűleg nem irányított át a dashboardra.")

except Exception as e:
    print(f"Hiba történt a futás során: {e}")

finally:
    try:
        driver.quit()
    except:
        pass
    print("Folyamat kész, böngésző bezárva.")
