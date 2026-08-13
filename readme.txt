# Erhebungsskript zur Bachelorarbeit

**Von SEO zu GEO: Eine empirische Untersuchung zum Einfluss technischer
SEO-Faktoren auf die Zitationshäufigkeit von B2B-Websites in generativen
Sprachmodellen**

Hochschule Offenburg, Fakultät Wirtschaft, 2026
Autor: Carlos Hauss

## Überblick

Die Skripte übergeben die Prompts an die Programmierschnittstellen von Anthropic
und OpenAI, speichert die Antworten und extrahiert die darin ausgewiesenen
Quellen als URLs. Die verwendeten Modelle und sämtliche Parameter der Abfrage
sind im Skript direkt einsehbar hinterlegt.

**Erhebungszeitraum:** 07.08.2026 – 10.08.2026

## Aufbau

| Datei | Funktion |
|---|---|
| `skript-Anthropic.py` & `skript-ChatGPT.py` | Abfrage der LLM-APIs, Extraktion der Quellen |
| `domain-rating-fetcher.py` | Abfrage der Domain Rates via Ahrefs API, Extraktion der Scores |
| `ergebnisse_*-----*.csv/` | Ergebnisdateien (nicht Bestandteil des Repositorys) |

## Einrichtung

Python 3.11.9, Abhängigkeiten mit Versionsnummern in `requirements.txt`.

```bash
python3.11 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Zugangsdaten

Die API-Schlüssel werden über Umgebungsvariablen eingelesen und sind nicht
Bestandteil dieses Repositorys. Vorlage siehe `.env.example`:

```
ANTHROPIC_API_KEY=...
OPENAI_API_KEY=...
```

## Ausführung

```bash
python erhebung.py
```

## Hinweis zur Reproduzierbarkeit

Die Antworten generativer Systeme hängen von den zum Abrufzeitpunkt
verfügbaren Webinhalten sowie von der Anbieterkonfiguration ab. Eine exakte
Replikation der Ergebnisse zu einem späteren Zeitpunkt ist daher nicht zu
erwarten.

## Lizenz

MIT (siehe LICENSE)