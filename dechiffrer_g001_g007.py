#!/usr/bin/env python3
"""
DECHIFFRER — Prompt Maître G001..G007
Evidence-first structural analysis of a corpus.

The engine distinguishes observations from hypotheses and conclusions.
It never treats repetition, consensus, or correlation as proof.
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

STATUSES = ("VERIFIED", "SUPPORTED", "CONVERGENT", "UNVERIFIED", "CONTRADICTED", "UNKNOWN")

GENERIC_BASE = {
    "G001": "Il écrit bien",
    "G002": "Il écrit mal",
    "G003": "Il est génie",
    "G004": "Il est mauvais",
    "G005": "On est d'accord, il...",
    "G006": "On est d'accord que...",
    "G007": "Il faut l'arrêter...",
}

@dataclass(frozen=True)
class Observation:
    id: str
    source: str
    content: str
    context: str | None
    date: str | None
    author: str | None
    reliability: str
    motif: str | None
    status: str

def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().replace("’", "'")
    text = re.sub(r"[^a-z0-9'\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def detect_motif(text: str) -> str | None:
    n = normalize(text)
    patterns = [
        ("G005", r"^on est (?:tous )?d accord\s*,?\s*il\b"),
        ("G006", r"^on est (?:tous )?d accord que\b"),
        ("G007", r"^il faut (?:l|la|le|les)\b"),
        ("G001", r"^il\s+ecrit\s+(?:tres\s+)?bien\b"),
        ("G002", r"^il\s+ecrit\s+(?:tres\s+)?mal\b"),
        ("G003", r"^(?:il est|c est)\s+(?:un\s+)?genie\b"),
        ("G004", r"^il est\s+(?:tres\s+)?mauvais\b"),
    ]
    for motif, pattern in patterns:
        if re.match(pattern, n):
            return motif
    return None

def load_jsonl(path: Path) -> list[Observation]:
    rows = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        content = str(item.get("content", ""))
        rows.append(Observation(
            id=str(item.get("id", f"OBS-{i:04d}")),
            source=str(item.get("source", path.name)),
            content=content,
            context=item.get("context"),
            date=item.get("date"),
            author=item.get("author"),
            reliability=str(item.get("reliability", "UNKNOWN")),
            motif=detect_motif(content),
            status="VERIFIED" if content else "UNKNOWN",
        ))
    return rows

def from_messages(messages: Iterable[str]) -> list[Observation]:
    return [
        Observation(
            id=f"OBS-{i:04d}", source="cli", content=m, context=None,
            date=None, author=None, reliability="USER_SUPPLIED",
            motif=detect_motif(m), status="VERIFIED" if m else "UNKNOWN",
        )
        for i, m in enumerate(messages, 1)
    ]

def evidence_level(rows: list[Observation], motif: str) -> str:
    matches = [r for r in rows if r.motif == motif]
    if not matches:
        return "UNKNOWN"
    sources = {r.source for r in matches}
    if len(matches) >= 3 and len(sources) >= 2:
        return "CONVERGENT"
    if len(matches) >= 2:
        return "SUPPORTED"
    return "VERIFIED"

def analyze(rows: list[Observation]) -> dict:
    counts = Counter(r.motif for r in rows if r.motif)
    unmatched = [r.id for r in rows if not r.motif]
    sequence = [r.motif for r in rows if r.motif]
    transitions = Counter(zip(sequence, sequence[1:]))

    explicit = []
    for motif, count in sorted(counts.items()):
        explicit.append({
            "motif": motif,
            "label": GENERIC_BASE[motif],
            "occurrences": count,
            "sources": sorted({r.source for r in rows if r.motif == motif}),
            "status": evidence_level(rows, motif),
        })

    hypotheses = []
    for motif, count in sorted(counts.items()):
        hypotheses.append({
            "id": f"H-{motif}",
            "statement": f"{motif} is a recurrent structural pattern in the supplied corpus.",
            "supporting_observations": count,
            "status": evidence_level(rows, motif),
            "falsification_test": "Repeat on an independent corpus and compare the same normalized pattern.",
        })

    contradictions = []
    for a, b in transitions:
        if {a, b} in ({ "G001", "G002" }, { "G003", "G004" }):
            contradictions.append({
                "pair": [a, b],
                "type": "POLARITY_OPPOSITION",
                "meaning": "The corpus contains opposing evaluations; neither side is established as true by repetition alone.",
                "status": "VERIFIED",
            })

    return {
        "1_STRUCTURE_OBSERVEE": {
            "total": len(rows),
            "matched": len(rows) - len(unmatched),
            "unmatched": len(unmatched),
            "principle": "Observed linguistic structure only; hidden intent is not inferred.",
        },
        "2_MOTIFS_RECURRENT": explicit,
        "3_RELATIONS": {
            "graph": "SOURCE -> OBSERVATION -> MOTIF -> HYPOTHESIS -> CONSEQUENCE",
            "transitions": {f"{a}->{b}": n for (a, b), n in sorted(transitions.items())},
        },
        "4_HYPOTHESES": hypotheses,
        "5_CONTRADICTIONS": contradictions,
        "6_PREUVES": {
            "verified_observations": [asdict(r) for r in rows],
            "rule": "A repetition is evidence of recurrence, not proof of truth, intent, causality, or coordination.",
        },
        "7_DONNEES_MANQUANTES": [
            "Corpus réel complet si la base de test n'est pas le corpus cible.",
            "Provenance et contexte de chaque observation.",
            "Dates et séquence temporelle lorsque l'ordre compte.",
            "Corpus témoin indépendant pour mesurer la spécificité des motifs.",
        ] if unmatched or not rows else [
            "Corpus témoin indépendant pour mesurer la spécificité des motifs.",
            "Contexte/provenance complémentaire lorsque absent.",
        ],
        "8_TESTS_A_EFFECTUER": [
            "Rejouer l'analyse sur un corpus indépendant.",
            "Comparer la fréquence des motifs avec un corpus témoin.",
            "Tester les contradictions et les formulations voisines.",
            "Vérifier toute relation causale avec une observation indépendante.",
        ],
        "9_STRUCTURE_DECHIFFREE": {
            "minimal_structure": "G001..G007 are normalized linguistic templates with evaluative, consensus, and directive forms.",
            "limitations": "No hidden meaning, intention, coordination, or causality is established by this pipeline alone.",
        },
        "10_NIVEAU_DE_VALIDATION": (
            "VERIFIED" if rows else "UNKNOWN"
        ),
    }

def main() -> None:
    parser = argparse.ArgumentParser(description="DECHIFFRER — analyse G001..G007 fondée sur les preuves")
    parser.add_argument("messages", nargs="*", help="Messages à analyser")
    parser.add_argument("--jsonl", type=Path, help="Corpus JSONL: id, source, content, context, date, author, reliability")
    parser.add_argument("--output", type=Path, help="Écrire le rapport JSON")
    args = parser.parse_args()

    if args.jsonl:
        rows = load_jsonl(args.jsonl)
    elif args.messages:
        rows = from_messages(args.messages)
    else:
        rows = from_messages(GENERIC_BASE.values())

    report = analyze(rows)
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    print(payload)
    if args.output:
        args.output.write_text(payload + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
