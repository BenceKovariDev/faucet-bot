import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

EMAIL = os.environ.get("FC_EMAIL")
PASSWORD = os.environ.get("FC_PASS")

print("--- GitHub Actions Undetected Bot Indul ---")

# Beállítások a rejtett, védelmet megkerülő böngészőhöz
options = uc.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

try:
    # Az undetected_chromedriver automatikusan kezeli a kompatibilis drivert
    driver = uc.Chrome(options=options, use_subprocess=True)
    
    print("Megnyitom a bejelentkezési oldalt...")
    driver.get("https://faucetcrypto.com/login")
    
    wait = WebDriverWait(driver, 25)
    
    print("E-mail kitöltése...")
    email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email' or @name='email']")))
    email_field.clear()
    email_field.send_keys(EMAIL)
    
    print("Jelszó mező kitöltése...")
    password_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password' or @name='password']")))
    password_field.clear()
    password_field.send_keys(PASSWORD)
    
    time.sleep(2)
    
    print("Kattintás a Bejelentkezés gombra...")
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' or contains(text(), 'Bejelentkezés')]")))
    login_button.click()
    
    print("Várakozás a bejelentkezés utáni betöltésre...")
    time.sleep(10)
    
    print(f"Aktuális URL: {driver.current_url}")
    
    if "dashboard" in driver.current_url:
        print("Sikeres belépés!")
        driver.get("https://faucetcrypto.com/dashboard/ptc")
        time.sleep(5)
    else:
        print("A botvédelmen nem sikerült átjutni, vagy hibásak az adatok.")

except Exception as e:
    print(f"Hiba történt: {e}")

finally:
    try:
        driver.quit()
    except:
        pass
    print("Folyamat kész, böngésző bezárva.")
