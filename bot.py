import os
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
    # Automatikusan kezeli a ChromeDriver-t
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    print("Megnyitom a bejelentkezési oldalt...")
    driver.get("https://faucetcrypto.com/login")
    
    wait = WebDriverWait(driver, 15)
    
    print("E-mail kitöltése...")
    email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    email_field.send_keys(EMAIL)
    
    print("Jelszó kitöltése...")
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(PASSWORD)
    
    time.sleep(1)
    
    print("Kattintás a Bejelentkezés gombra...")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Bejelentkezés')]")
    login_button.click()
    
    time.sleep(5)
    print(f"Jelenlegi URL bejelentkezés után: {driver.current_url}")

except Exception as e:
    print(f"Hiba történt: {e}")

finally:
    try:
        driver.quit()
    except:
        pass
    print("Folyamat kész, böngésző bezárva.")
