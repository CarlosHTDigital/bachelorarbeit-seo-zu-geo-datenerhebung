import os
import re
import time
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

gesammelte_daten = []
CSV_DATEI = "ergebnisse_openai.csv"

if os.path.exists(CSV_DATEI):
    df_bisherige_ergebnisse = pd.read_csv(CSV_DATEI)
    zeilen_nummer = df_bisherige_ergebnisse["Nummer"].max() + 1
else:
    df_bisherige_ergebnisse = None
    zeilen_nummer = 1

for aktueller_prompt in meine_prompts:
    for durchlauf in range(1, 2):
        print(f"OpenAI: Verarbeite Prompt '{aktueller_prompt[:30]}...' (Durchlauf {durchlauf}/1)")

        try:
            response = client.responses.create(
                model="gpt-5.6-luna",
                tools=[{"type": "web_search"}],
                input=aktueller_prompt,
            )

            komplette_antwort = ""
            zitierte_urls = []
            gefundene_urls = []

            # Durch das 'output'-Array iterieren
            for item in getattr(response, 'output', []):
                
                # 1. Den fertigen Text und die Zitationen finden
                if getattr(item, 'type', '') == 'message':
                    for content_part in getattr(item, 'content', []):
                        if getattr(content_part, 'type', '') == 'output_text':
                            komplette_antwort += getattr(content_part, 'text', '')
                            
                            # Zitationen auslesen
                            for ann in getattr(content_part, 'annotations', []):
                                if getattr(ann, 'type', '') == 'url_citation':
                                    if hasattr(ann, 'url') and ann.url:
                                        zitierte_urls.append(ann.url)

                # 2. Die gefundenen/aufgerufenen Seiten aus den Tool-Calls finden
                elif getattr(item, 'type', '') == 'web_search_call':
                    action = getattr(item, 'action', None)
                    if action:
                        action_type = getattr(action, 'type', '')
                        
                        if action_type == 'open_page' and hasattr(action, 'url'):
                            if action.url:
                                gefundene_urls.append(action.url)
                                
                        elif action_type == 'search' and getattr(action, 'sources', None):
                            for src in action.sources:
                                if hasattr(src, 'url') and src.url:
                                    gefundene_urls.append(src.url)

            # Manuell nach URLs im Text fischen
            text_urls = re.findall(r'https?://[^\s)]+', komplette_antwort)
            zitierte_urls.extend(text_urls)

            # In die Liste eintragen
            gesammelte_daten.append({
                "Nummer": zeilen_nummer,
                "Durchlauf": durchlauf,
                "Modell": "GPT-5.6-luna",
                "Input_Prompt": aktueller_prompt,
                "Antwort": komplette_antwort,
                "Zitierte_Quellen_URLs": ", ".join(sorted(set(zitierte_urls))),
                "Gefundene_Quellen_URLs": ", ".join(sorted(set(gefundene_urls)))
            })
            zeilen_nummer += 1

            # Korrekt eingereckte Pause am Ende des Durchlaufs
            print(f"Durchlauf {durchlauf} fertig. Warte 65 Sekunden, um das API-Limit nicht zu sprengen...")
            time.sleep(65)

        except Exception as e:
            print(f"Fehler bei OpenAI: {e}")

# In die CSV schreiben
df_neue_ergebnisse = pd.DataFrame(gesammelte_daten)
if df_bisherige_ergebnisse is not None:
    df_gesamt = pd.concat([df_bisherige_ergebnisse, df_neue_ergebnisse], ignore_index=True)
else:
    df_gesamt = df_neue_ergebnisse

df_gesamt.to_csv(CSV_DATEI, index=False, encoding="utf-8")
print(f"OpenAI fertig! Gespeichert in '{CSV_DATEI}'.")