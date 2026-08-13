import anthropic
import os
import re
import time
from dotenv import load_dotenv
from icecream import ic
import pandas as pd

load_dotenv()

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Schleife für die Input-Prompts 
meine_prompts = [
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Aluminium-Druckgussteile. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Aluminium-Druckgussteile. Die Teile müssen nach IATF 16949 gefertigt und erstmusterfähig sein, der Jahresbedarf liegt bei rund 50.000 Stück. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um aktuelle Informationen zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Aluminium-Druckgussteile. Gesucht wird im Raum Baden-Württemberg. Welche Anbieter kommen infrage? Verwende die Websuche, um aktuelle Informationen zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Aluminium-Druckgussteile. Die Teile müssen nach IATF 16949 gefertigt und erstmusterfähig sein, der Jahresbedarf liegt bei rund 50.000 Stück. Gesucht wird im Raum Baden-Württemberg. Welche Anbieter kommen infrage? Verwende die Websuche, um aktuelle Informationen zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Drahtbiegeteile und Federn. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Drahtbiegeteile und Federn. Die Teile sollen aus Federstahldraht nach DIN EN 10270 bestehen, der Jahresbedarf liegt bei rund 200.000 Stück. Gesucht wird in Deutschland. Welche Anbieter kommen infrage?  Verwende die Websuche, um aktuelle Informationen zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Drahtbiegeteile und Federn. Gesucht wird im Raum Nordrhein-Westfalen. Welche Anbieter kommen infrage? Verwende die Websuche, um aktuelle Informationen zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Drahtbiegeteile und Federn. Die Teile sollen aus Federstahldraht nach DIN EN 10270 bestehen, der Jahresbedarf liegt bei rund 200.000 Stück. Gesucht wird im Raum Nordrhein-Westfalen. Welche Anbieter kommen infrage? Verwende die Websuche, um aktuelle Informationen zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Kunststoffverpackungen. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Kunststoffverpackungen. Die Verpackungen müssen lebensmittelkonform nach EU-Verordnung 10/2011 sein, Jahresbedarf rund 300.000 Stück. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Kunststoffverpackungen. Gesucht wird im Raum Bayern. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Kunststoffverpackungen. Die Verpackungen müssen lebensmittelkonform nach EU-Verordnung 10/2011 sein, Jahresbedarf rund 300.000 Stück. Gesucht wird im Raum Bayern. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Lohnveredelung von Fahrzeugteilen. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Lohnveredelung von Fahrzeugteilen. Der Betrieb soll nach ISO 9001 zertifiziert sein, zu lackieren sind rund 20.000 Teile pro Jahr. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Lohnveredelung von Fahrzeugteilen. Gesucht wird im Raum Sachsen. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Lohnveredelung von Fahrzeugteilen. Der Betrieb soll nach ISO 9001 zertifiziert sein, zu lackieren sind rund 20.000 Teile pro Jahr. Gesucht wird im Raum Sachsen. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Kabelsätze für Fahrzeuge. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Kabelsätze für Fahrzeuge. Die Fertigung muss nach IATF 16949 zertifiziert sein, der Jahresbedarf liegt bei rund 30.000 Stück. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Kabelsätze für Fahrzeuge. Gesucht wird im Raum Thüringen. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Kabelsätze für Fahrzeuge. Die Fertigung muss nach IATF 16949 zertifiziert sein, der Jahresbedarf liegt bei rund 30.000 Stück. Gesucht wird im Raum Thüringen. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für mechanische Kfz-Zulieferteile. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für mechanische Kfz-Zulieferteile. Gefordert sind IATF 16949 und ein Erstmusterprüfbericht nach VDA 2, Jahresbedarf rund 80.000 Stück. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für mechanische Kfz-Zulieferteile. Gesucht wird im Raum Niedersachsen. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für mechanische Kfz-Zulieferteile. Gefordert sind IATF 16949 und ein Erstmusterprüfbericht nach VDA 2, Jahresbedarf rund 80.000 Stück. Gesucht wird im Raum Niedersachsen. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Pflanzenöle und Fette für die Lebensmittelproduktion. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Pflanzenöle und Fette für die Lebensmittelproduktion. Die Ware muss nach IFS Food zertifiziert sein, der Jahresbedarf liegt bei rund 200 Tonnen. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Pflanzenöle und Fette für die Lebensmittelproduktion. Gesucht wird im Raum Schleswig-Holstein. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Pflanzenöle und Fette für die Lebensmittelproduktion. Die Ware muss nach IFS Food zertifiziert sein, der Jahresbedarf liegt bei rund 200 Tonnen. Gesucht wird im Raum Schleswig-Holstein. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Fertiggerichte für die Betriebsverpflegung. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Fertiggerichte für die Betriebsverpflegung. Gefordert ist eine IFS-Food-Zertifizierung, benötigt werden rund 600 Portionen pro Arbeitstag. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Fertiggerichte für die Betriebsverpflegung. Gesucht wird im Raum Hessen. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Fertiggerichte für die Betriebsverpflegung. Gefordert ist eine IFS-Food-Zertifizierung, benötigt werden rund 600 Portionen pro Arbeitstag. Gesucht wird im Raum Hessen. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Mischfutter für Nutztiere. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Mischfutter für Nutztiere. Verlangt sind GMP+ FSA und QS-Zertifizierung, der Jahresbedarf liegt bei rund 1.500 Tonnen. Gesucht wird in Deutschland. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Mischfutter für Nutztiere. Gesucht wird im Raum Mecklenburg-Vorpommern. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
"Ich bin im Einkauf eines mittelständischen Unternehmens und suche erstmalig einen Lieferanten für Mischfutter für Nutztiere. Verlangt sind GMP+ FSA und QS-Zertifizierung, der Jahresbedarf liegt bei rund 1.500 Tonnen. Gesucht wird im Raum Mecklenburg-Vorpommern. Welche Anbieter kommen infrage? Verwende die Websuche, um Firmenwebsites zu finden.",
]


# Datensammlung für pandas
gesammelte_daten = []
CSV_DATEI = "ergebnisse_anthropic.csv"

# Falls die CSV aus früheren Läufen schon existiert, lädt sie hier,
# damit  die Nummerierung fortgesetzt werden und neue Ergebnisse angehängt werden können statt sie zu überschreiben
if os.path.exists(CSV_DATEI):
    df_bisherige_ergebnisse = pd.read_csv(CSV_DATEI)
    zeilen_nummer = df_bisherige_ergebnisse["Nummer"].max() + 1
else:
    df_bisherige_ergebnisse = None
    zeilen_nummer = 1

# ÄUßERE SCHLEIFE: Geht jeden  Prompt nacheinander durch
for aktueller_prompt in meine_prompts:

    # INNERE SCHLEIFE: Wiederholt den aktuellen Prompt genau 1 Mal
    for durchlauf in range(1, 2):  # Zählt von 1 bis 2
        print(f"Verarbeite Prompt {aktueller_prompt} (Durchlauf {durchlauf} von 1)")

        message = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=4096,
            messages=[{
                 "role": "user",
                 "content": aktueller_prompt
            }],
            tools=[{"type": "web_search_20250305", "name": "web_search", 
                 # max uses: Limit the number of searches per request
                 "max_uses": 2,
                 # user location: Limit the number of searches per request
                "user_location": {
                    "type": "approximate",
                    "city": "Hamburg",
                    "region": "Hamburg",
                    "country": "DE",
                    "timezone": "Europe/Berlin"
                }
            }],
        )
        #Terminal Anzeige
        ic(message.content)
        print()
        
        # 1. Wir sammeln Textblöcke und trennen dabei zwei Arten von URLs:
        #    - zitierte_urls: Quellen, die Claude tatsächlich für die Antwort verwendet hat
        #      (echte Citations + im Antworttext direkt genannte Links)
        #    - gefundene_urls: ALLE Treffer aus der Websuche, unabhängig davon, ob Claude
        #      sie für die Antwort genutzt hat (roher Ergebnis-Pool der Suchmaschine)
        alle_text_stuecke = []
        zitierte_urls = []
        gefundene_urls = []

        for block in message.content:
            block_type = getattr(block, 'type', '')

            # Textblöcke enthalten die finale Antwort und ggf. Citations
            if block_type == 'text':
                alle_text_stuecke.append(block.text)

                # Checken, ob das Attribut 'citations' existiert und nicht "None" ist
                if getattr(block, 'citations', None):
                    for citation in block.citations:
                        # Jede Zitation hat ein 'url' Attribut, das wir herausziehen
                        if getattr(citation, 'url', None):
                            zitierte_urls.append(citation.url)

            # Die rohen Suchergebnisse (mit vollständigen https://-URLs) stecken
            # in einem eigenen Block-Typ, nicht in den Textblöcken
            elif block_type == 'web_search_tool_result':
                such_ergebnisse = block.content
                # Bei einem Fehler ist .content ein einzelnes Error-Objekt statt einer Liste
                if isinstance(such_ergebnisse, list):
                    for ergebnis in such_ergebnisse:
                        if getattr(ergebnis, 'url', None):
                            gefundene_urls.append(ergebnis.url)

        # Alle Textblöcke der Antwort sauber mit Zeilenumbruch zusammenfügen
        komplette_antwort = "\n".join(alle_text_stuecke)

        # 2. Zur Sicherheit suchen wir trotzdem noch im Text nach URLs
        # (Manchmal schreibt Claude URLs direkt in den Text, statt die Zitation zu nutzen -
        # das zählt inhaltlich als "zitierte" Quelle, da Claude explizit darauf verweist)
        text_urls = re.findall(r'https?://[^\s]+', komplette_antwort)
        zitierte_urls.extend(text_urls)

        # 3. Duplikate pro Spalte entfernen
        zitierte_urls_text = ", ".join(sorted(set(zitierte_urls)))
        gefundene_urls_text = ", ".join(sorted(set(gefundene_urls)))

        # 4. In die CSV-Liste eintragen
        gesammelte_daten.append({
            "Nummer": zeilen_nummer,
            "Durchlauf": durchlauf,
            "Modell": "Claude-Sonnet-5",
            "Input_Prompt": aktueller_prompt,
            "Antwort": komplette_antwort,
            "Zitierte_Quellen_URLs": zitierte_urls_text,
            "Gefundene_Quellen_URLs": gefundene_urls_text
        })
        
        ic(komplette_antwort)
        
        zeilen_nummer += 1

        # <-- HIER DIE PAUSE -->
        print(f"Durchlauf {durchlauf} fertig. Warte 65 Sekunden, um das API-Limit nicht zu sprengen...")
        time.sleep(65) # 60 Sekunden Pause, um das API-Limit nicht zu sprengen

# --- DER PANDAS SCHRITT AM ENDE ---
# Wandelt die neuen Daten in eine Tabelle um und hängt sie an die bisherigen Ergebnisse an,
# statt die CSV zu überschreiben
df_neue_ergebnisse = pd.DataFrame(gesammelte_daten)
if df_bisherige_ergebnisse is not None:
    df_gesamt = pd.concat([df_bisherige_ergebnisse, df_neue_ergebnisse], ignore_index=True)
else:
    df_gesamt = df_neue_ergebnisse

df_gesamt.to_csv(CSV_DATEI, index=False, encoding="utf-8")

print(f"\nAlle Durchläufe wurden erfolgreich an '{CSV_DATEI}' angehängt "
      f"(insgesamt {len(df_gesamt)} Zeilen)!")
