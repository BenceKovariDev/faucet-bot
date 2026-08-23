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

print("--- GitHub Actions FaucetCrypto PTC Bot Indul ---")

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
    
    wait = WebDriverWait(driver, 20)
    
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
    
    print("Várakozás a bejelentkezésre...")
    time.sleep(7)
    
    print(f"Jelenlegi URL: {driver.current_url}")
    
    if "dashboard" in driver.current_url or "home" in driver.current_url:
        print("Sikeres bejelentkezés! Navigálás a PTC feladatok oldalára...")
        driver.get("https://faucetcrypto.com/dashboard/ptc")
        time.sleep(5)
        
        try:
            print("Keresem az elérhető PTC feladat gombját...")
            # Megkeressük az első olyan gombot, amiben benne van az "Óra" szöveg vagy a kék kattintható elem
            ptc_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Óra')] | //button[contains(., 'Óra')]")))
            ptc_button.click()
            print("Sikeresen rákattintottam egy PTC feladatra!")
            
            # Várakozunk, hogy lejárjon az időzítő (pl. 16-40 másodperc)
            print("Várakozás a hirdetés lefutására...")
            time.sleep(20)
            
        except Exception as e:
            print(f"Nem találtam kattintható PTC feladatot vagy hiba történt: {e}")
    else:
        print("A bejelentkezés nem sikerült vagy ellenőrzésbe ütközött.")

except Exception as e:
    print(f"Hiba történt a futás során: {e}")

finally:
    try:
        driver.quit()
    except:
        pass
    print("Folyamat kész, böngésző bezárva.")
