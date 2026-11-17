# DaZ – Deutsch-Trainer mit Englisch als Brückensprache

Web-App für eine Schülerin (Klasse 11), die Deutsch neu lernt und Englisch spricht. Läuft auf dem iPad als Icon auf dem Home-Bildschirm.
Basiert auf dem Wortkasten (Paula/Emil), angepasst auf Deutsch als Zielsprache.

**Adresse:** https://peldajonas-cell.github.io/DaZ/
Auf dem iPad in Safari öffnen → Teilen → „Zum Home-Bildschirm“.

## Was die Schülerin sieht (Oberfläche auf Englisch)
- **Today:** tägliche Runde mit Karteikasten (Fach 1–5, Intervalle 1/2/4/7/14 Tage).
- **Phrases:** Sätze für den Schulalltag. Antippen liest den deutschen Satz vor, „Show“ zeigt ihn groß auf dem Bildschirm.
- **Practise:** Lektion und Modus frei wählen (verschiebt keine Fächer).

- **Settings** (oben rechts, ohne PIN): „My progress“ (gelernte Wörter, Trefferquote, Lernzeit, Lerntage, schwierige Wörter mit „Practise these words“, Stand pro Modus) und „Settings“ (Übungen pro Runde, neue Wörter pro Runde, Sicherungscode, Zurücksetzen).

Kein Foto-Upload, keine eigenen Wörter: Neue Vokabeln kommen nur über dieses Repository.

## Lernmodi
Leicht: Flashcard, Multiple choice, Match pairs, **der/die/das**.
Schwer (starten, wenn ein leichter Modus Fach 2 erreicht): Understand, Type it, Listen & write, Fill the gap, Build the sentence, **Plural**, **Verb forms**.

Beim Eintippen gilt:
- Nomen nur mit Artikel richtig. Fehlender oder falscher Artikel zählt als falsch, mit Hinweis.
- Fehlende Umlaute (a statt ä, ss statt ß) und Kleinschreibung zählen als richtig, mit Hinweis.

## Einstellungen
Die Schülerin stellt selbst ein: Übungen pro Runde (Standard 25) und neue Wörter pro Runde (Standard 8).
Keine Konten, keine Namen, keine Synchronisation. Der Lernstand liegt nur im localStorage des iPads (Schlüssel `wortkasten-daz.v1`).

## Aufbau
```
src/app.html            Quelle
index.html              python3 tools/build_index.py
lektionen/*.txt         Vokabeln (basics.txt = Grundwortschatz)
lektionen/saetze.txt    Phrasebook
lektionen.json          python3 tools/build_lessons.py
icon.png                Home-Bildschirm-Icon (orange)
```

### Vokabel-Format
```
# Lektion: Biologie: Die Zelle
Deutsch ; Englisch ; Satz Deutsch ; Satz Englisch ; Formen
die Zelle ; cell ; Die Zelle ist sehr klein. ; The cell is very small. ; die Zellen
teilen ; to divide ; Die Zellen können sich teilen. ; Cells can divide.
gehen ; to go ; Wir gehen in die Mensa. ; We go to the canteen. ; gehen - ging - ist gegangen
```
- Lektionsname „Gruppe: Thema“. Die Startseite gruppiert nach dem Teil vor dem Doppelpunkt (z. B. „Basics“, „Biologie“).
- Nomen immer mit Artikel. Formen: Plural (ein Eintrag) oder drei Verbformen, getrennt mit „ - “ (mit Leerzeichen).
- Das Zielwort (ohne Artikel) muss wörtlich im deutschen Satz stehen, sonst gibt es keinen Lückensatz. Mit „wir“ steht das Verb im Infinitiv: „Wir lernen …“.
- Mehrere richtige Antworten mit „/“. Kein „;“ innerhalb eines Feldes.
- Veröffentlichte Lektionen nicht umbenennen, sonst geht der Lernstand verloren.

### Phrasebook-Format
```
# Thema: In class
Ich verstehe das nicht. ; I don't understand that.
```

## Neue Lektion
Fotos der Arbeitsblätter (macht die Lehrkraft) → Claude erstellt Vokabeln mit Sätzen auf A1/A2-Niveau → `lektionen/<fach>.txt` ergänzen → `python3 tools/build_lessons.py` → commit + push. Beim nächsten Öffnen lädt die App die neuen Wörter.
