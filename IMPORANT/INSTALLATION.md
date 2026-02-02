# 📥 Installation de la documentation pour Claude Code

## 🎯 Objectif

Ces fichiers vont permettre à Claude Code de **comprendre instantanément** ton projet Rockstar Bros et de t'aider efficacement.

---

## 📂 Structure des fichiers fournis

```
rockstar-bros-docs/
├── .claude/                      # Documentation pour Claude Code
│   ├── project-context.md        # ⭐ FICHIER PRINCIPAL - Vue d'ensemble
│   ├── architecture.md           # Architecture technique détaillée
│   └── asset-tracker.md          # Liste des assets à créer
├── docs/                         # Documentation générale
│   ├── CAHIER_DES_CHARGES.md    # Spécifications complètes
│   ├── STRUCTURE.md             # Guide structure Pygame
│   └── CONVENTIONS.md           # Conventions de code
├── README.md                     # Vue d'ensemble projet
└── INSTALLATION.md              # Ce fichier
```

---

## 🚀 Installation (3 étapes simples)

### Étape 1 : Créer la structure de ton projet

Dans le dossier où tu veux créer ton jeu :

```bash
mkdir rockstar-bros
cd rockstar-bros
```

### Étape 2 : Copier les fichiers de documentation

Copie **tout le contenu** du dossier `rockstar-bros-docs` que je t'ai fourni :

```bash
# Depuis le dossier rockstar-bros/
cp -r /chemin/vers/rockstar-bros-docs/.claude .
cp -r /chemin/vers/rockstar-bros-docs/docs .
cp /chemin/vers/rockstar-bros-docs/README.md .
```

Ton projet devrait maintenant ressembler à ça :

```
rockstar-bros/
├── .claude/         ← Nouveaux fichiers
├── docs/            ← Nouveaux fichiers
└── README.md        ← Nouveau fichier
```

### Étape 3 : Lancer Claude Code

```bash
# Dans le dossier rockstar-bros/
claude-code
```

---

## ✅ Vérification

Pour vérifier que tout est bien en place :

```bash
# Dans rockstar-bros/
ls -la .claude/
```

Tu devrais voir :
- `project-context.md`
- `architecture.md`
- `asset-tracker.md`

---

## 🎓 Comment Claude Code va utiliser ces fichiers

### Automatiquement au démarrage

Quand tu lances Claude Code, il lit automatiquement :
1. **`.claude/project-context.md`** - Pour comprendre le projet
2. Le **`README.md`** - Pour la vue d'ensemble

### Quand tu lui demandes de l'aide

Par exemple, si tu dis :
> "Aide-moi à créer la classe Player"

Claude Code va :
1. Lire `.claude/architecture.md` pour voir comment structurer la classe
2. Consulter `docs/CONVENTIONS.md` pour le style de code
3. Vérifier `docs/STRUCTURE.md` pour l'intégration dans le projet

**Tu n'as rien à faire** - Claude Code gère tout automatiquement !

---

## 📋 Ordre de lecture recommandé (pour toi)

Si tu veux comprendre le projet avant de coder :

1. **`README.md`** (5 min) - Vue d'ensemble
2. **`.claude/project-context.md`** (10 min) - Contexte complet
3. **`docs/CAHIER_DES_CHARGES.md`** (15 min) - Toutes les specs
4. **`docs/STRUCTURE.md`** (10 min) - Comment organiser le code
5. **`.claude/architecture.md`** (15 min) - Architecture détaillée

**Total : ~55 minutes** pour tout comprendre.

---

## 🎯 Premiers pas avec Claude Code

Une fois les fichiers en place :

### 1. Démarre Claude Code
```bash
claude-code
```

### 2. Commence par les fondations

**Demande à Claude Code** :
> "Crée-moi la structure de base : main.py, settings.py et le dossier scenes/ avec base.py"

Claude va automatiquement :
- Lire les fichiers de documentation
- Créer les fichiers avec la bonne structure
- Suivre les conventions du projet

### 3. Continue étape par étape

**Demandes suivantes** :
> "Crée la classe Player dans entities/player.py avec mouvement et saut"

> "Ajoute le système de gravité"

> "Crée un ennemi Hater qui patrouille"

---

## 💡 Astuces pour bien utiliser Claude Code

### ✅ Bonnes pratiques

1. **Commandes claires et spécifiques**
   > ❌ "Fais le jeu"
   > ✅ "Crée la classe Player avec mouvement gauche/droite et saut"

2. **Itérer progressivement**
   - Commence par le joueur qui bouge
   - Puis ajoute le saut
   - Puis la gravité
   - Puis les ennemis, etc.

3. **Tester après chaque étape**
   > "Crée main.py pour tester le joueur"

4. **Référencer la doc si besoin**
   > "En suivant le guide dans .claude/architecture.md, crée la scène gameplay"

### 🎯 Claude Code connaît déjà

Grâce aux fichiers fournis, Claude Code sait **déjà** :
- ✅ Que c'est un jeu plateforme 2D
- ✅ Qu'il y a un système Guitar Hero
- ✅ Qu'il faut 3 niveaux + 1 boss
- ✅ Comment structurer le code (scènes, entités, etc.)
- ✅ Quelles sont les constantes (vitesses, HP, etc.)
- ✅ Quels assets créer

**Tu n'as pas besoin de tout réexpliquer à chaque fois !**

---

## 🐛 Dépannage

### Problème : Claude Code ne trouve pas les fichiers

**Solution** : Vérifie que tu es dans le bon dossier
```bash
pwd  # Doit afficher .../rockstar-bros
ls .claude/  # Doit lister les 3 fichiers .md
```

### Problème : Claude Code ne suit pas la structure

**Solution** : Mentionne explicitement la doc
> "En suivant .claude/architecture.md, crée..."

### Problème : Tu veux modifier la doc

**C'est normal !** Ces fichiers sont faits pour être adaptés. Tu peux :
- Modifier les constantes dans `.claude/project-context.md`
- Ajouter des notes dans `.claude/asset-tracker.md`
- Adapter les specs dans `docs/CAHIER_DES_CHARGES.md`

Claude Code relira les fichiers à chaque fois.

---

## 📞 Si tu es bloqué

1. **Relis les docs** - Souvent la réponse est dedans
2. **Demande à Claude Code** - "Explique-moi comment fonctionne le système de scènes"
3. **Teste progressivement** - Commence simple, ajoute progressivement
4. **Utilise les placeholders** - Rectangles colorés en attendant les vrais sprites

---

## 🎊 C'est prêt !

Tu as maintenant :
- ✅ Toute la documentation nécessaire
- ✅ Claude Code qui comprend ton projet
- ✅ Un plan de développement clair
- ✅ Des conventions de code à suivre

**Il ne reste plus qu'à coder ! 🚀**

---

## 📝 Checklist finale

Avant de commencer à coder, vérifie que :

- [ ] Le dossier `.claude/` existe avec 3 fichiers
- [ ] Le dossier `docs/` existe avec 3 fichiers
- [ ] Le fichier `README.md` est à la racine
- [ ] Tu as lu au moins le `README.md` et `.claude/project-context.md`
- [ ] Claude Code est installé et fonctionne

**Si tout est ✅, tu peux commencer ! Bon courage ! 🎸🎮**