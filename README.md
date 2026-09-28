# VIDEO FACTORY V2

Pipeline : Script → Voice/Chatterbox → Audio Analysis → Alignment → Storyboard → Images → Animation → Subtitles → Montage → Render → QC.

## Règles
- VERIFIED uniquement après exécution avec preuve.
- UNKNOWN si non mesuré.
- Aucun mock présenté comme réel.
- ElevenLabs interdit.
- Chatterbox comme fournisseur vocal.
- Les backends visuels réels doivent être branchés sur Qwen/WAN.
- La validation finale produit un rapport machine.

## Contraintes
- 4 s ≤ scène ≤ 8 s.
- 60 s → 9 scènes, 9 images, 9 animations potentielles.
- Arrondi half-up compatible avec Math.round.
- Le nombre de scènes peut être élargi si nécessaire pour préserver scène ≤ 8 s.
- Échec explicite si la durée est trop courte pour 8 scènes de 4 s.

## Validation
```bash
python3 tools/inventory/scan_repo.py
python3 scripts/run_validation.py --scripts scripts/samples/s1.txt scripts/samples/s2.txt scripts/samples/s3.txt
```

Le dépôt ne déclare pas la pipeline GO avant exécution réelle.
