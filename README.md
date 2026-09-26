# DECHIFFRER — moteur G001 → G007

Version actuelle du **Prompt Maître — Déchiffrer** : analyse structurale fondée sur les preuves.

## Pipeline

`COMPRENDRE → STRUCTURER → NORMALISER → EXTRAIRE → RELIER → HYPOTHÉSER → CONTREDIRE → TESTER → DÉCHIFFRER → VALIDER`

### G001 — INGESTION
Structure les observations : ID, source, contenu, contexte, date, auteur, relations, fiabilité.

### G002 — NORMALISATION
Normalise les formulations sans supprimer leur forme originale.

### G003 — EXTRACTION
Détecte répétitions, oppositions, causalités affirmées, jugements, présupposés, consensus, injonctions et contradictions.

### G004 — RECONSTRUCTION
Relie les éléments par la chaîne :

`SOURCE → OBSERVATION → MOTIF → HYPOTHÈSE → CONSÉQUENCE`

### G005 — CONTRADICTION
Cherche activement les éléments qui peuvent invalider chaque hypothèse.

### G006 — DÉCHIFFREMENT
Construit la structure minimale compatible avec les données sans inventer de signification cachée.

### G007 — VALIDATION
Associe chaque conclusion à son niveau de preuve et à un test de falsification.

## Statuts

- `VERIFIED`
- `SUPPORTED`
- `CONVERGENT`
- `UNVERIFIED`
- `CONTRADICTED`
- `UNKNOWN`

## Formulations de base

- G001 — « Il écrit bien »
- G002 — « Il écrit mal »
- G003 — « Il est génie »
- G004 — « Il est mauvais »
- G005 — « On est d'accord, il… »
- G006 — « On est d'accord que… »
- G007 — « Il faut l'arrêter… »

## Exécution

```bash
python3 dechiffrer_g001_g007.py
```

Corpus JSONL :

```bash
python3 dechiffrer_g001_g007.py --jsonl corpus.jsonl --output rapport.json
```

Le moteur ne transforme jamais une répétition en preuve de vérité, d'intention, de coordination ou de causalité.
