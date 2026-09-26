#!/usr/bin/env python3
"""
Déchiffrer — generic linguistic classifier G001..G007.

Purpose:
- classify observed messages against the seven supplied templates;
- preserve the original text;
- expose variants and structural features;
- count observed transitions between templates.

Important:
This module detects linguistic patterns only. A match does not establish
a hidden code, intent, surveillance, coordination, or secondary meaning.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from typing import Iterable


@dataclass(frozen=True)
class Classification:
    message: str
    template: str | None
    category: str
    polarity: str
    act: str
    confidence: float
    normalized: str


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().strip()
    text = re.sub(r"[\u2019']", "'", text)
    text = re.sub(r"[^a-z0-9'\s]", " ", text)
    return re.sub(r"\s+", " ", text)


def classify(message: str) -> Classification:
    n = normalize(message)

    # G005/G006 are checked before generic "il..." patterns because they
    # are discourse-level templates.
    if re.match(r"^on est (?:tous )?d accord\s*,?\s*il\b", n):
        return Classification(message, "G005", "accord + proposition",
                               "NEUTRAL", "VALIDATION", 1.0, n)

    if re.match(r"^on est (?:tous )?d accord que\b", n):
        return Classification(message, "G006", "accord + proposition",
                               "NEUTRAL", "VALIDATION", 1.0, n)

    if re.match(r"^il faut (?:l|la|le|les)\b", n):
        return Classification(message, "G007", "necessite + action",
                               "DIRECTIVE", "INJONCTION", 1.0, n)

    if re.match(r"^il\s+ecrit\s+(?:tres\s+)?bien\b", n):
        return Classification(message, "G001", "il + action + evaluation",
                               "POSITIVE", "JUGEMENT", 1.0, n)

    if re.match(r"^il\s+ecrit\s+(?:tres\s+)?mal\b", n):
        return Classification(message, "G002", "il + action + evaluation",
                               "NEGATIVE", "JUGEMENT", 1.0, n)

    if re.match(r"^(?:il est|c est)\s+(?:un\s+)?genie\b", n):
        return Classification(message, "G003", "il + etre + attribut",
                               "POSITIVE", "QUALIFICATION", 1.0, n)

    if re.match(r"^il est\s+(?:tres\s+)?mauvais\b", n):
        return Classification(message, "G004", "il + etre + attribut",
                               "NEGATIVE", "QUALIFICATION", 1.0, n)

    return Classification(message, None, "UNMATCHED",
                          "UNKNOWN", "UNKNOWN", 0.0, n)


def analyze(messages: Iterable[str]) -> dict:
    rows = [classify(m) for m in messages]
    templates = [r.template for r in rows if r.template]
    counts = Counter(templates)

    transitions = Counter()
    for a, b in zip(templates, templates[1:]):
        transitions[(a, b)] += 1

    return {
        "total_messages": len(rows),
        "matched_messages": len(templates),
        "unmatched_messages": len(rows) - len(templates),
        "template_counts": dict(sorted(counts.items())),
        "transitions": {
            f"{a}->{b}": n for (a, b), n in sorted(transitions.items())
        },
        "classifications": [asdict(r) for r in rows],
    }


GENERIC_BASE = {
    "G001": "Il écrit bien",
    "G002": "Il écrit mal",
    "G003": "Il est génie",
    "G004": "Il est mauvais",
    "G005": "On est d'accord, il...",
    "G006": "On est d'accord que...",
    "G007": "Il faut l'arrêter...",
}


if __name__ == "__main__":
    import json
    import sys

    messages = sys.argv[1:] or list(GENERIC_BASE.values())
    print(json.dumps(analyze(messages), ensure_ascii=False, indent=2))
