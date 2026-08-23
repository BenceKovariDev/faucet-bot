import os
import requests

EMAIL = os.environ.get("FC_EMAIL")
PASSWORD = os.environ.get("FC_PASS")

print("--- GitHub Actions HTTP Bot Indul ---")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

try:
    print("1. Kapcsolódás a Faucetcrypto oldalhoz...")
    response = session.get("https://faucetcrypto.com/login")
    print(f"Főoldal státusz: {response.status_code}")
    
    print("2. Bejelentkezési adatok küldése...")
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    login_response = session.post("https://faucetcrypto.com/login", data=payload, allow_redirects=True)
    
    print(f"Bejelentkezési válasz státusz: {login_response.status_code}")
    print(f"Aktuális URL: {login_response.url}")
    
    if "dashboard" in login_response.url:
        print("Sikeres bejelentkezés!")
    else:
        print("A szerver válaszolt, de a bejelentkezést ellenőrizni kell.")

except Exception as e:
    print(f"Hiba történt: {e}")

print("Folyamat vége.")
