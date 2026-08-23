import os
import requests
from bs4 import BeautifulSoup

EMAIL = os.environ.get("FC_EMAIL")
PASSWORD = os.environ.get("FC_PASS")

print("--- GitHub Actions API / HTTP Bot Indul ---")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "hu-HU,hu;q=0.9,en-US;q=0.8,en;q=0.7"
})

try:
    print("1. Bejelentkezési oldal lekérése...")
    login_page = session.get("https://faucetcrypto.com/login")
    
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    print("2. Bejelentkezési adatok küldése...")
    response = session.post("https://faucetcrypto.com/login", data=payload, allow_redirects=True)
    
    print(f"Válasz státuszkód: {response.status_code}")
    print(f"Aktuális válasz URL: {response.url}")
    
    if "dashboard" in response.url or response.status_code == 200:
        print("A kérés sikeresen lefutott.")
    else:
        print("A szerver vagy a védelem blokkolta a kérést.")

except Exception as e:
    print(f"Hiba történt a kérés során: {e}")

print("Folyamat kész.")
