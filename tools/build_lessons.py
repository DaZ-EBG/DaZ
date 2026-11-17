#!/usr/bin/env python3
"""Baut lektionen.json aus den Textdateien in lektionen/.

Vokabeln (alle *.txt außer saetze.txt):
  # Lektion: <Gruppe>: <Thema>
  Deutsch ; Englisch ; Satz Deutsch ; Satz Englisch ; Formen
- Nomen immer mit Artikel: "der Tisch".
- Formen: bei Nomen der Plural ("die Tische"), bei starken Verben
  drei Formen mit " - " getrennt ("gehen - ging - ist gegangen").
- Mehrere richtige Antworten mit "/" trennen.

Phrasebook (saetze.txt):
  # Thema: <Name>
  Deutsch ; Englisch

Die IDs bleiben stabil, solange Lektionsname und deutsches Wort gleich bleiben.
Damit bleibt der Lernstand auf dem iPad erhalten.
"""
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def slug(s):
    s = s.lower().replace("–", "-").replace("—", "-").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def rows(path):
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        m = re.match(r"^#+\s*(?:Lektion\s*:|Thema\s*:)?\s*(.+)$", line, re.I)
        if m:
            yield n, "head", m.group(1).strip()
        else:
            yield n, "row", [p.strip() for p in (line.split("\t") if "\t" in line else line.split(";"))]

def parse(path):
    lessons, cur = [], None
    for n, kind, val in rows(path):
        if kind == "head":
            cur = {"name": val, "words": []}; lessons.append(cur); continue
        parts = val
        if len(parts) < 2 or not parts[0] or not parts[1]:
            sys.exit(f"{path.name}:{n}: Zeile braucht mindestens 'Deutsch ; Englisch'")
        if cur is None:
            sys.exit(f"{path.name}:{n}: Vokabel vor der ersten '# Lektion:'-Zeile")
        w = {"de": parts[0], "en": parts[1], "sDe": parts[2] if len(parts) > 2 else "", "sEn": parts[3] if len(parts) > 3 else ""}
        if len(parts) > 4 and parts[4]:
            f = [x.strip() for x in re.split(r"\s+[–-]\s+", parts[4]) if x.strip()]
            if len(f) not in (1, 3):
                sys.exit(f"{path.name}:{n}: Formen: 1 (Plural) oder 3 (Verb) erwartet, gefunden {len(f)}")
            w["forms"] = f
        cur["words"].append(w)
    return lessons

def phrases(path):
    cats, cur = [], None
    for n, kind, val in rows(path):
        if kind == "head":
            cur = {"name": val, "items": []}; cats.append(cur); continue
        if len(val) < 2 or cur is None:
            sys.exit(f"{path.name}:{n}: Satz braucht 'Deutsch ; Englisch' unter einer '# Thema:'-Zeile")
        cur["items"].append({"de": val[0], "en": val[1]})
    return cats

def main():
    out, ph = [], []
    for path in sorted((ROOT / "lektionen").glob("*.txt")):
        if path.stem == "saetze":
            ph = phrases(path); continue
        for les in parse(path):
            lid = slug(les["name"])
            seen = set()
            for w in les["words"]:
                base = f"{lid}--{slug(w['de'].split('/')[0])}"
                wid, k = base, 2
                while wid in seen:
                    wid, k = f"{base}-{k}", k + 1
                seen.add(wid)
                w["id"] = wid
            out.append({"id": lid, "name": les["name"], "words": [dict(id=w.pop("id"), **w) for w in les["words"]]})
    (ROOT / "lektionen.json").write_text(json.dumps({"version": 1, "lessons": out, "phrases": ph}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(out)} Lektionen, {sum(len(l['words']) for l in out)} Vokabeln, {sum(len(c['items']) for c in ph)} Sätze")

if __name__ == "__main__":
    main()
