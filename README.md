# traducteur-non-fiable

## Déchiffrer — base générique G001 → G007

Le dépôt contient le premier moteur déterministe de classification des sept gabarits linguistiques définis pour la base de test :

- **G001** — « Il écrit bien »
- **G002** — « Il écrit mal »
- **G003** — « Il est génie »
- **G004** — « Il est mauvais »
- **G005** — « On est d'accord, il… »
- **G006** — « On est d'accord que… »
- **G007** — « Il faut l'arrêter… »

Le moteur `dechiffrer_g001_g007.py` :

1. conserve le message original ;
2. normalise la forme pour la comparaison ;
3. classe les occurrences dans G001–G007 ;
4. conserve les messages non classés comme `UNMATCHED` ;
5. calcule les fréquences ;
6. calcule les transitions observées entre gabarits.

### Principe de preuve

Une classification linguistique ne constitue pas une preuve d'un code caché, d'une intention ou d'une coordination. Toute hypothèse secondaire doit être testée séparément sur un corpus réel et, lorsque possible, comparée à un corpus témoin.

### Exécution

    python3 dechiffrer_g001_g007.py

Ou avec des messages réels :

    python3 dechiffrer_g001_g007.py "Il écrit bien" "On est d'accord, il écrit mal" "Il faut l'arrêter"
