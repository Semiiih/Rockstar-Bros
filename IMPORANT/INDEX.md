# 📚 Index Documentation - Rockstar Bros

**Guide de navigation dans la documentation**

---

## 🚀 Par où commencer ?

### Tu veux démarrer VITE ? (5 min)
→ **`QUICKSTART.md`** - Démarrage en 5 minutes

### Tu veux tout comprendre ? (1h)
→ Lis dans cet ordre :
1. `README.md` (5 min)
2. `.claude/project-context.md` (15 min)
3. `docs/CAHIER_DES_CHARGES.md` (20 min)
4. `docs/STRUCTURE.md` (15 min)

### Tu configures Claude Code ?
→ **`INSTALLATION.md`** - Guide d'installation complet

---

## 📁 Organisation des fichiers

```
rockstar-bros-docs/
│
├── 🚀 QUICKSTART.md              ← Démarrage rapide (5 min)
├── 📥 INSTALLATION.md            ← Installation pour Claude Code
├── 📖 README.md                  ← Vue d'ensemble projet
├── 📑 INDEX.md                   ← Ce fichier
│
├── .claude/                      ← Documentation pour Claude Code
│   ├── project-context.md        ← ⭐ PRINCIPAL - Vue complète
│   ├── architecture.md           ← Architecture détaillée
│   └── asset-tracker.md          ← Liste des assets
│
└── docs/                         ← Documentation détaillée
    ├── CAHIER_DES_CHARGES.md     ← Spécifications complètes
    ├── STRUCTURE.md              ← Guide structure Pygame
    └── CONVENTIONS.md            ← Conventions de code
```

---

## 📖 Guide par fichier

### 🔥 Les essentiels (à lire absolument)

#### `QUICKSTART.md`
**Quand** : Tout de suite  
**Durée** : 5 min  
**Contenu** :
- Démarrage ultra-rapide
- Premières commandes Claude Code
- Plan d'action Jour 1
- Checklist avant de commencer

#### `README.md`
**Quand** : En premier  
**Durée** : 5 min  
**Contenu** :
- Vue d'ensemble du jeu
- Contrôles
- Installation rapide
- Structure du projet
- Timeline 5 jours

#### `.claude/project-context.md` ⭐
**Quand** : Juste après le README  
**Durée** : 15 min  
**Contenu** :
- Concept complet du projet
- Stack technique
- Fichiers clés et leur rôle
- Spécificités du projet (Guitar Hero, etc.)
- Assets prioritaires
- Workflow jour par jour
- Points d'attention critiques

**C'est LE fichier le plus important. Claude Code le lit automatiquement.**

---

### 🏗️ Architecture et technique

#### `.claude/architecture.md`
**Quand** : Avant de coder  
**Durée** : 15 min  
**Contenu** :
- Arborescence complète du projet
- Flux de données entre fichiers
- Responsabilités par fichier (qui fait quoi)
- Templates de code
- Patterns recommandés
- Points critiques (delta time, gravité, etc.)

**Claude Code utilise ce fichier pour structurer le code.**

#### `docs/STRUCTURE.md`
**Quand** : Si tu veux comprendre Pygame  
**Durée** : 15 min  
**Contenu** :
- Philosophie structure Pygame
- Architecture en scènes (pourquoi/comment)
- Rôle exact de main.py
- Rôle exact de settings.py
- Système sprites et groups
- Delta time expliqué
- Système de coordonnées

**Guide pédagogique sur Pygame.**

#### `docs/CONVENTIONS.md`
**Quand** : Avant de coder sérieusement  
**Durée** : 10 min  
**Contenu** :
- Nommage (variables, classes, fichiers)
- Organisation du code
- Commentaires et docstrings
- Gestion constantes
- Patterns recommandés
- Debug et tests
- Checklist avant rendu

**Pour garder un code propre.**

---

### 📋 Spécifications et planning

#### `docs/CAHIER_DES_CHARGES.md`
**Quand** : Pour référence  
**Durée** : 20 min  
**Contenu** :
- Concept détaillé
- Loop de gameplay
- Contrôles complets
- Système d'attaque musicale
- Ennemis et boss
- Système de vie/UI
- Niveaux détaillés
- Timeline 5 jours
- Critères de réussite
- Contraintes techniques

**Document de référence complet.**

#### `.claude/asset-tracker.md`
**Quand** : Jour 3-4 (assets)  
**Durée** : 10 min  
**Contenu** :
- Liste complète 35-40 images
- Priorités (MVP vs complet)
- Dimensions recommandées
- Outils de création
- Placeholders temporaires
- Checklist par catégorie

**Pour gérer la création des sprites.**

---

### 🛠️ Installation et setup

#### `INSTALLATION.md`
**Quand** : Au tout début  
**Durée** : 5 min  
**Contenu** :
- Installation étape par étape
- Comment placer les fichiers
- Vérification que tout fonctionne
- Ordre de lecture recommandé
- Premiers pas avec Claude Code
- Dépannage

**Guide d'installation complet.**

---

## 🎯 Parcours par profil

### Je débute avec Pygame
1. ✅ `README.md` - Vue d'ensemble
2. ✅ `docs/STRUCTURE.md` - Comprendre Pygame
3. ✅ `.claude/project-context.md` - Vue complète projet
4. ✅ `QUICKSTART.md` - Lancer le code
5. 📖 `docs/CONVENTIONS.md` - Bonnes pratiques

### Je connais Pygame
1. ✅ `README.md` - Vue d'ensemble
2. ✅ `.claude/project-context.md` - Contexte projet
3. ✅ `.claude/architecture.md` - Architecture
4. ✅ `QUICKSTART.md` - Démarrer
5. 📖 `docs/CAHIER_DES_CHARGES.md` - Specs complètes

### Je configure Claude Code
1. ✅ `INSTALLATION.md` - Setup complet
2. ✅ `.claude/project-context.md` - Pour que Claude Code comprenne
3. ✅ `QUICKSTART.md` - Premières commandes
4. 📖 Tous les autres (Claude Code les lira automatiquement)

### Je veux juste coder MAINTENANT
1. ✅ `QUICKSTART.md` - GO !
2. 📖 Consulte les autres si besoin

---

## 🔍 Trouver une info spécifique

### "Comment structurer mon code ?"
→ `.claude/architecture.md` section "Responsabilités par fichier"  
→ `docs/STRUCTURE.md` entier

### "Quelles sont les règles de nommage ?"
→ `docs/CONVENTIONS.md` section "Nommage"

### "Qu'est-ce que je mets dans settings.py ?"
→ `.claude/project-context.md` section "Ce qui va dans settings.py"  
→ `docs/STRUCTURE.md` section "settings.py"

### "Comment fonctionne le système Guitar Hero ?"
→ `.claude/project-context.md` section "Système d'attaque rythmée"  
→ `docs/CAHIER_DES_CHARGES.md` section "Système d'attaque musicale"  
→ `.claude/architecture.md` section "systems/rhythm.py"

### "Quels assets créer en priorité ?"
→ `.claude/asset-tracker.md` section "Priorités de développement"  
→ `.claude/project-context.md` section "Assets à créer"

### "Qu'est-ce que je dois faire jour 1 ?"
→ `QUICKSTART.md` section "Plan d'action (Jour 1)"  
→ `README.md` section "Objectifs par jour"  
→ `.claude/project-context.md` section "Workflow recommandé"

### "Comment utiliser delta time (dt) ?"
→ `docs/STRUCTURE.md` section "Delta Time (dt)"  
→ `.claude/architecture.md` section "Points critiques"

### "Le jeu crash, comment débugger ?"
→ `QUICKSTART.md` section "Debug rapide"  
→ `docs/CONVENTIONS.md` section "Debug et tests"

---

## 📊 Statistiques

**Total documentation** : ~15,000 mots  
**Temps lecture complète** : ~2h  
**Temps lecture essentiel** : ~30 min

**Fichiers par priorité** :

**🔴 Critique (à lire absolument)** :
- `QUICKSTART.md`
- `README.md`
- `.claude/project-context.md`

**🟡 Important (à lire avant de coder sérieusement)** :
- `.claude/architecture.md`
- `docs/STRUCTURE.md`
- `INSTALLATION.md`

**🟢 Référence (consulter au besoin)** :
- `docs/CAHIER_DES_CHARGES.md`
- `docs/CONVENTIONS.md`
- `.claude/asset-tracker.md`

---

## 🎓 Comment utiliser cette doc avec Claude Code

### Automatique
Claude Code lit automatiquement :
- `.claude/project-context.md` au démarrage
- `README.md` pour la vue d'ensemble
- Les autres fichiers quand nécessaire

### Référence explicite
Tu peux mentionner un fichier :
```
"En suivant .claude/architecture.md, crée la classe Player"
```

### Mise à jour
Tu peux modifier ces fichiers. Claude Code les relira.

---

## 🆘 Besoin d'aide ?

1. **Cherche dans l'index** (ce fichier) la section pertinente
2. **Lis le fichier recommandé**
3. **Demande à Claude Code** : "Explique-moi [concept] selon la doc"

---

## ✅ Checklist utilisation

Avant de coder :
- [ ] J'ai lu `QUICKSTART.md`
- [ ] J'ai lu `README.md`
- [ ] J'ai lu `.claude/project-context.md`
- [ ] J'ai installé les fichiers selon `INSTALLATION.md`
- [ ] Je sais où trouver les infos (grâce à cet INDEX)

**Tout est ✅ ? Let's code ! 🚀**

---

**Ce fichier est ton GPS dans la documentation. Utilise-le ! 🧭**