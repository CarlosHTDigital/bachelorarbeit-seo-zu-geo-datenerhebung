import requests
import csv
import os
import time
import random
from urllib.parse import urlparse
from dotenv import load_dotenv

# Laedt die Variablen aus der .env-Datei im Projektordner
load_dotenv()

# ============================================================
# KONFIGURATION
# ============================================================

# API-Key kommt aus der .env-Datei 
API_KEY = os.getenv("AHREFS_API_KEY")

if not API_KEY:
    raise SystemExit(
        "Kein API-Key gefunden.\n"
        "Lege in der .env-Datei die Zeile 'AHREFS_API_KEY=dein_key' an\n"
        "und achte darauf, dass die .env im selben Ordner wie das Skript liegt."
    )

API_URL = "https://api.ahrefs.com/v3/public/domain-rating-free"
CSV_DATEI = "ergebnisse_domain_authority_ahrefs.csv"

# Da das Domain Rating pro DOMAIN gilt (nicht pro URL), 
# wird das Ergebnis wird gecacht und
# trotzdem für jede Ursprungs-URL in die CSV geschrieben.
NUR_EINE_ABFRAGE_PRO_DOMAIN = True

# Trage hier deine URL-Liste ein
urls = [
  
]


# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def hole_domain(url):
    """Extrahiert die Domain aus einer URL (ohne www.)."""
    netloc = urlparse(url).netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc


def hole_domain_rating(domain):
    """
    Fragt das Domain Rating bei Ahrefs ab.
    Rueckgabe: (wert, status)
    """
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    params = {
        "target": domain,
        "output": "json",
    }

    # Bis zu 3 Versuche, falls das Rate Limit zuschlaegt
    for versuch in range(1, 4):
        try:
            response = requests.get(API_URL, headers=headers, params=params, timeout=30)

            if response.status_code == 200:
                daten = response.json()
                return daten["domain_rating"]["domain_rating"], "OK"

            if response.status_code == 429:
                wartezeit = 30 * versuch
                print(f"   -> Rate Limit erreicht. Warte {wartezeit} Sekunden...")
                time.sleep(wartezeit)
                continue

            # 400 = ungueltiges Ziel, 401 = Key falsch, 403 = kein Zugriff
            return "", f"HTTP {response.status_code}"

        except Exception as e:
            print(f"   -> Netzwerkfehler: {e}")
            time.sleep(5)

    return "", "Fehler (Limit/Netzwerk)"


# ============================================================
# HAUPTFUNKTION
# ============================================================

def check_domain_rating():
    results = []
    cache = {}  # domain -> (wert, status)

    for index, url in enumerate(urls, 1):
        domain = hole_domain(url)
        print(f"[{index}/{len(urls)}] Pruefe: {domain}")

        # Bereits abgefragte Domain? Dann Wert aus dem Cache nehmen.
        if NUR_EINE_ABFRAGE_PRO_DOMAIN and domain in cache:
            wert, status = cache[domain]
            print(f"-> Aus Cache: DR {wert}")
        else:
            wert, status = hole_domain_rating(domain)
            cache[domain] = (wert, status)
            print(f"-> Domain Rating: {wert} ({status})")

            # Kurze Pause, damit die API nicht ueberrannt wird
            wait_time = random.uniform(1.0, 2.5)
            time.sleep(wait_time)

        results.append({
            "URL": url,
            "Domain": domain,
            "domain_rating": wert,
            "status": status,
        })

    # CSV-Export mit automatischer Erkennung (Anhaengen falls vorhanden)
    fieldnames = ["URL", "Domain", "domain_rating", "status"]
    file_exists = os.path.exists(CSV_DATEI)

    with open(CSV_DATEI, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        # Ueberschrift nur schreiben, wenn die Datei neu erstellt wird
        if not file_exists:
            writer.writeheader()

        writer.writerows(results)

    print(f"\nFertig! Ergebnisse wurden an '{CSV_DATEI}' angehaengt.")
    print("Hinweis: Bei Veroeffentlichung der Daten ist die Angabe")
    print("'Domain Rating by Ahrefs' (https://ahrefs.com/) verpflichtend.")


# Skript ausfuehren
if __name__ == "__main__":
    check_domain_rating()
