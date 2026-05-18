# Bilan Carbone — PFE Louai Boubaker (E-Tafakna, 2026)

## Contexte général

| Paramètre | Valeur |
|---|---|
| Période | Février 2026 – Mai 2026 (3 mois) |
| Lieu | E-Tafakna, Tunis |
| Présence sur site | 2 jours/semaine → **26 jours** (13 semaines × 2) |
| Jours totaux de travail | **65 jours** (13 semaines × 5 j/semaine) |
| Référentiel | Base Carbone® ADEME, adaptée au contexte tunisien — Guide ISI v1.0, Avril 2026 |
| Unité | kg CO₂e (kilogrammes de CO₂ équivalent) |

---

## Résultat final

| # | Poste | kg CO₂e | % du total |
|---|---|---|---|
| 1 | Transport | **1 060.8** | 96.1% |
| 2 | Matériel Informatique | **14.9** | 1.3% |
| 3 | Infrastructure & Code | **25.6** | 2.3% |
| 4 | Matériel de Bureau | **2.4** | 0.2% |
| | **TOTAL** | **1 103.7** | 100% |

**Conclusion rapide :** Le transport domine à 96.1% à cause du trajet domicile–E-Tafakna (85 km aller simple en voiture seul). Tous les postes numériques réunis (GPU cloud, APIs, laptop) ne représentent que 2.3% du total.

---

## Poste 1 — Transport (1 060.8 kg CO₂e)

### Données de base
- Mode : voiture personnelle, conducteur seul (aucun copassager)
- Distance domicile → E-Tafakna : **85 km**
- Trajet aller-retour : 85 × 2 = **170 km/jour**
- Jours de présence : **26 jours**
- Distance totale : 26 × 170 = **4 420 km**

### Facteur d'émission
Le guide ISI distingue deux valeurs pour la voiture :

| Référence | FE (kg CO₂e/km/véhicule) | Note |
|---|---|---|
| Base ADEME | 0.19 | Contexte France |
| Ajusté Tunisie | **0.24** | Carburant tunisien, mix énergétique |

Pour 1 seul passager, le FE véhicule = FE passager (pas de division).

### Calcul
```
Émissions = Distance × FE
           = 4 420 km × 0.24 kg CO₂e/km
           = 1 060.8 kg CO₂e
```

---

## Poste 2 — Matériel Informatique (14.9 kg CO₂e)

### Contexte
L'ordinateur portable utilisé est **personnel et préexistant** (acheté avant le PFE). Le guide ISI prescrit dans ce cas le **scénario 2** : amortir l'empreinte de fabrication sur la durée de vie estimée et n'imputer que la fraction correspondant à la durée du PFE.

### Données officielles ASUS

| Paramètre | Valeur | Source |
|---|---|---|
| Modèle | ASUS TUF Gaming FA506N (RTX 3050, Ryzen 5 7000s, 32 Go, 15.6") | Déclaratif |
| Rapport PCF de référence | ASUS FA507NU (même série, même génération, même format 15.6") | ASUS ESG, ISO 14067:2018, fév. 2024 |
| PCF total cycle de vie | **336 kg CO₂e** | ASUS Product Carbon Footprint Report FA507NU |
| Phase fabrication | **71% = 238.6 kg CO₂e** | Même rapport (pie chart LCA) |
| Phase utilisation | 24.8% = 83.3 kg CO₂e | Non comptée ici (déjà dans Poste 3A) |
| Phase packaging & transport | 4.1% = 13.8 kg CO₂e | Inclus dans fabrication |
| Fin de vie | 0.1% = 0.3 kg CO₂e | Négligeable |
| Durée de vie officielle | **4 ans = 48 mois** | Déclaré par ASUS dans le rapport PCF |

> **Pourquoi utiliser FA507NU et pas FA506N ?**
> ASUS n'a pas publié de rapport PCF pour le FA506N spécifiquement. Le FA507NU est le modèle de la même gamme TUF A15, même génération Ryzen 7000, même écran 15.6", même poids (2.2 kg), fabriqué au même site (Chine). Les différences (GPU légèrement supérieur sur le NU) introduisent une légère surestimation, ce qui est conservateur.

> **Pourquoi utiliser seulement la phase fabrication (71%) et pas le total (336 kg) ?**
> Le total de 336 kg CO₂e inclut la phase d'utilisation (électricité pendant 4 ans = 83.3 kg CO₂e). Cette consommation est déjà comptée indépendamment dans le Poste 3A (laptop local 18.6 kg CO₂e). L'additionner ici créerait un double comptage.

### Calcul
```
Émissions = Phase fabrication × (Durée PFE / Durée de vie)
           = 238.6 × (3 / 48)
           = 238.6 × 0.0625
           = 14.9 kg CO₂e
```

---

## Poste 3 — Infrastructure & Code (25.6 kg CO₂e)

Ce poste regroupe 5 sous-composantes.

---

### 3A — Consommation locale du laptop (18.6 kg CO₂e)

Le laptop consomme de l'électricité du réseau tunisien toute la durée du PFE, y compris les jours de télétravail.

#### Données
| Paramètre | Valeur | Source |
|---|---|---|
| Puissance moyenne laptop | **0.075 kW** | Milieu de la plage 0.05–0.1 kW (ADEME) |
| Utilisation quotidienne | **7 h/jour** | Déclaratif |
| Jours de travail totaux | **65 jours** | 13 semaines × 5 j/semaine |
| Total heures | **455 h** | 65 × 7 |
| FE électricité Tunisie | **0.545 kg CO₂e/kWh** | Guide ISI (mix tunisien, forte part thermique) |

> **Pourquoi 0.545 et non 0.05 ?**
> La France a un réseau électrique bas-carbone (nucléaire → ~0.05 kg CO₂e/kWh). La Tunisie dépend à ~97% du gaz naturel et du pétrole → facteur ~10x plus élevé.

#### Calcul
```
Émissions = Puissance × Heures × FE électricité
           = 0.075 kW × 455 h × 0.545 kg CO₂e/kWh
           = 18.6 kg CO₂e
```

---

### 3B — Serveur cloud OVHcloud — Fine-tuning (0.18 kg CO₂e)

Le fine-tuning des deux modèles a été réalisé sur un GPU NVIDIA V100S (32 GiB VRAM) loué via OVHcloud AI Notebooks.

#### Données
| Paramètre | Valeur | Source |
|---|---|---|
| GPU | NVIDIA V100S, TDP 300W | Fiche technique NVIDIA |
| Puissance serveur estimée | **0.5 kW** | GPU (0.3 kW) + CPU/mémoire/ventilation (0.2 kW) |
| PUE OVHcloud | **1.30** | Guide ISI (tableau providers) |
| FE électricité France | **0.052 kg CO₂e/kWh** | RTE 2024, mix nucléaire français |
| Durée Gemma 4 E4B | **3 357 s = 0.93 h** | Logs d'entraînement OVHcloud |
| Durée Qwen3.5 9B | **15 223 s = 4.23 h** | Logs d'entraînement OVHcloud |

> **Pourquoi le FE France est si bas ?**
> La France produit ~70% de son électricité par le nucléaire, ce qui donne l'un des mix les plus bas-carbone d'Europe (~0.052 kg CO₂e/kWh vs ~0.545 pour la Tunisie). C'est précisément pourquoi le fine-tuning sur OVHcloud (datacenter France) est quasi-neutre en carbone.

#### Formule
```
Émissions = Puissance serveur × Heures × PUE × FE électricité
```

#### Calcul Gemma 4 E4B
```
= 0.5 × 0.93 × 1.30 × 0.052 = 0.032 kg CO₂e
```

#### Calcul Qwen3.5 9B
```
= 0.5 × 4.23 × 1.30 × 0.052 = 0.143 kg CO₂e
```

#### Total OVHcloud
```
0.032 + 0.143 = 0.175 ≈ 0.18 kg CO₂e
```

> **À titre de comparaison :** un seul aller-retour en voiture (1 jour de présence = 170 km) émet 170 × 0.24 = 40.8 kg CO₂e, soit **227× plus** que l'ensemble des deux entraînements GPU.

---

### 3C — APIs Cloud : GPT-4.1 et Gemini (3.1 kg CO₂e)

Deux services cloud externes ont été utilisés **uniquement pendant la phase de préparation du corpus** (pipeline offline), pas à l'inférence.

| Service | Usage | Requêtes estimées | FE/requête | Émissions |
|---|---|---|---|---|
| GPT-4.1 (Azure OpenAI) | Extraction d'articles + synthèse dataset | ~300 | 7 g CO₂e | 2.1 kg CO₂e |
| Gemini (Google Cloud Vertex AI) | OCR hybride PDF → texte | ~200 | 5 g CO₂e | 1.0 kg CO₂e |
| **Total** | | | | **3.1 kg CO₂e** |

> Les valeurs FE par requête (5–10 g CO₂e pour un grand modèle) sont tirées des estimations publiées par Goldman Sachs Research (2024) et IEA (2024) pour GPT-4-class models. Gemini est légèrement plus efficace.

---

### 3D — Transferts de données / réseau (1.2 kg CO₂e)

| Activité | Volume estimé |
|---|---|
| Téléchargement fichiers GGUF (2 modèles × ~5 Go) | 10 Go |
| Données d'entraînement + dépendances Python | 20 Go |
| Git push/pull + navigation de recherche | 30 Go |
| **Total** | **60 Go** |

```
Émissions = Volume × FE réseau
           = 60 Go × 0.02 kg CO₂e/Go
           = 1.2 kg CO₂e
```

> FE réseau : 0.02 kg CO₂e/Go (Guide ISI, estimation réseau fixe).

---

### 3E — Requêtes aux assistants IA (2.5 kg CO₂e)

L'utilisation de Claude Code et ChatGPT pour le développement (code, débogage, rédaction) représente un usage non négligeable.

```
~500 requêtes × 5 g CO₂e/requête = 2 500 g = 2.5 kg CO₂e
```

#### Total Poste 3
```
18.6 + 0.18 + 3.1 + 1.2 + 2.5 = 25.58 ≈ 25.6 kg CO₂e
```

---

## Poste 4 — Matériel de Bureau (2.4 kg CO₂e)

### Impression (127 pages)

| Élément | Quantité | FE | Émissions |
|---|---|---|---|
| Papier A4 (5 g/feuille) | 127 × 5g = 0.635 kg | 1.3 kg CO₂e/kg (ADEME) | 0.8 kg CO₂e |
| Encre/toner | 13 g (127p / 2500p par cartouche × 250g) | 3.5 kg CO₂e/kg | 0.1 kg CO₂e |
| **Sous-total impression** | | | **0.9 kg CO₂e** |

### Fournitures
- Cahiers, stylos, chemises ≈ 0.5 kg de matières
- FE fournitures mixtes : 3 kg CO₂e/kg (ADEME, plastiques + papeterie)
- Émissions : 0.5 × 3 = **1.5 kg CO₂e**

```
Total Poste 4 = 0.9 + 1.5 = 2.4 kg CO₂e
```

---

## Analyse et Propositions d'Amélioration

### Répartition des émissions
```
Transport        ████████████████████████████████████████████  1 060.8 kg  (96.1%)
Infrastructure   █                                                25.6 kg   (2.3%)
Matériel Info    ░                                                14.9 kg   (1.3%)
Bureau           ░                                                 2.4 kg   (0.2%)
                                                          TOTAL: 1 103.7 kg
```

### Leviers d'action (du plus au moins impactant)

#### 1. Transport — levier prioritaire (−96% de l'empreinte totale si résolu)

| Action | Réduction estimée |
|---|---|
| Passer de 2 à 1 jour/semaine sur site | −50% transport = −530 kg CO₂e |
| Télétravail total | −100% transport = −1 061 kg CO₂e |
| Covoiturage (2 personnes) | −50% du FE = −530 kg CO₂e |
| Transport en commun (bus longue distance) | FE 0.13 kg CO₂e/km·pers vs 0.24 → −46% |

> Un seul jour de télétravail supplémentaire par semaine économise plus de carbone que l'ensemble des postes numériques réunis.

#### 2. Infrastructure numérique — Green IT

- **Choix du datacenter :** OVHcloud France (0.052 kg CO₂e/kWh) était déjà optimal. Éviter les datacenters en Asie du Sud-Est ou au Moyen-Orient (0.5–0.8 kg CO₂e/kWh).
- **Sobriété :** Quantifier les modèles (GGUF q4_k_m) dès la phase de test, pas seulement en production. Réduire les itérations d'entraînement par un meilleur hyperparameter search préalable.
- **APIs :** Grouper les appels GPT-4.1 (batch processing) plutôt que d'envoyer des requêtes unitaires — réduit les émissions par appel et le coût.

#### 3. Matériel

- Prolonger la durée de vie du laptop (maintenance, nettoyage) : chaque année supplémentaire divise l'empreinte annuelle imputée.
- Éviter l'achat de nouveau matériel si le matériel existant est suffisant pour les tâches.

#### 4. Bureau

- Imprimer recto-verso (divise le nombre de feuilles par 2).
- Partager le rapport en PDF et n'imprimer qu'un seul exemplaire final.
- Utiliser du papier recyclé (FE ~0.8 kg CO₂e/kg vs 1.3 pour le papier neuf).

---

## Réflexion sur les choix techniques

Ce projet illustre un point souvent contre-intuitif : **dans un PFE à forte composante IA, les émissions numériques sont marginales par rapport aux déplacements physiques**.

- Le fine-tuning de deux LLMs sur GPU cloud (total : 5.16 heures de V100S) a émis **0.18 kg CO₂e** — moins qu'un trajet Tunis–Ariana en voiture.
- L'ensemble des postes numériques (GPU, APIs, laptop, données) représente **25.6 kg CO₂e**, soit **moins de 2.5% du total**.
- Le transport seul représente **1 061 kg CO₂e**, soit l'équivalent carbone de ~4 100 km de vol court-courrier ou ~12 mois de chauffage dans un appartement tunisien moyen.

La conclusion pratique est claire : **la sobriété numérique est une bonne pratique professionnelle**, mais pour un PFE en Tunisie avec un long trajet quotidien, la variable dominante est le déplacement physique. L'adoption du télétravail hybride est de loin le levier le plus efficace.
