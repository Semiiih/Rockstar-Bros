# 🎸 Rockstar Bros

Jeu de plateforme 2D avec mécanique Guitar Hero intégré.

**Projet Piscine Python - 5 jours**  
**Deadline finale** : Lundi 9 février 2026, 9h

---

## 📋 Vue d'ensemble

Tu incarnes un guitariste qui traverse 3 niveaux (coulisses → scène → boss final) en combattant des ennemis avec des ondes musicales. Le twist : un système de timing rythmé inspiré de Guitar Hero qui multiplie les dégâts si tu attaques au bon moment !

### Caractéristiques
- ✅ 2 personnages jouables
- ✅ 3 niveaux distincts
- ✅ Système de combat rythmé (Guitar Hero)
- ✅ Boss final avec plusieurs phases
- ✅ Score et combo
- ✅ Sons et musiques

---

## 🎮 Contrôles

| Touche | Action |
|--------|--------|
| `←` / `→` | Déplacement |
| `ESPACE` | Saut |
| `J` | Attaque musicale |
| `K` | Attaque ultime (jauge pleine) |
| `ESC` | Pause |

### Commandes debug (si activées)
| Touche | Action |
|--------|--------|
| `F1` | Afficher hitboxes |
| `F2` | Skip niveau |
| `F3` | Mode invincible |

---

## 🚀 Installation et lancement

### Prérequis
- Python 3.8 ou supérieur
- Pygame 2.x

### Installation

```bash
# Cloner le repo
git clone https://github.com/votre-nom/rockstar-bros.git
cd rockstar-bros

# Installer les dépendances
pip install pygame

# Lancer le jeu
python main.py
```

---

## 📁 Structure du projet

```
rockstar-bros/
├── .claude/                  # Documentation pour Claude Code
│   ├── project-context.md    # ⭐ Contexte principal
│   ├── architecture.md       # Architecture technique
│   └── asset-tracker.md      # Liste des assets
├── main.py                   # Entry point
├── settings.py               # Constantes globales
├── scenes/                   # États du jeu
│   ├── base.py
│   ├── menu.py
│   ├── gameplay.py
│   ├── pause.py
│   ├── game_over.py
│   └── victory.py
├── entities/                 # Entités (optionnel)
│   ├── player.py
│   ├── enemies.py
│   └── boss.py
├── systems/                  # Systèmes utilitaires (optionnel)
│   └── rhythm.py
├── assets/                   # Ressources
│   ├── images/
│   └── sounds/
├── docs/                     # Documentation
│   ├── CAHIER_DES_CHARGES.md
│   ├── STRUCTURE.md
│   └── CONVENTIONS.md
└── README.md                 # Ce fichier
```

---

## 📚 Documentation

### Pour Claude Code

Si tu utilises Claude Code, commence par lire ces fichiers dans l'ordre :

1. **`.claude/project-context.md`** - Vue d'ensemble complète du projet
2. **`.claude/architecture.md`** - Architecture technique détaillée
3. **`.claude/asset-tracker.md`** - Liste des assets à créer

### Pour les développeurs

- **`docs/CAHIER_DES_CHARGES.md`** - Spécifications complètes du jeu
- **`docs/STRUCTURE.md`** - Guide de structure Pygame
- **`docs/CONVENTIONS.md`** - Conventions de code

---

## 🎯 Objectifs par jour

### Jour 1 (Aujourd'hui)
- [x] Structure de base (main.py, settings.py, scenes/)
- [ ] Joueur qui bouge + saute
- [ ] Gravité fonctionnelle
- [ ] 1 plateforme

### Jour 2
- [ ] Attaque de base (projectile)
- [ ] 1 ennemi Hater (patrouille)
- [ ] Collisions
- [ ] Système de vie

### Jour 3
- [ ] Système Guitar Hero (barre + timing)
- [ ] 3 niveaux (backgrounds + layouts)
- [ ] Boss avec phases
- [ ] Remplacer placeholders par sprites

### Jour 4
- [ ] UI/HUD complet
- [ ] Sons et musiques
- [ ] Écrans (menu, pause, game over, victory)
- [ ] Polish

### Jour 5
- [ ] Tests finaux
- [ ] Préparation démo
- [ ] Soutenance

---

## 🎨 Assets

### Priorités

**MVP (Minimum Viable Product)** - ~15 images :
- Joueur (idle + run) × 2 persos
- 1 ennemi (idle)
- Projectile
- Plateforme
- Background simple
- UI vie

**Complet** - 35-40 images :
- Voir `asset-tracker.md` pour liste détaillée

### Style recommandé
- Pixel art rétro (plus rapide à produire)
- Couleurs vives
- Thème musical omniprésent

---

## 🐛 Debug

### Activer le mode debug

Dans `settings.py` :
```python
DEBUG_MODE = True
```

### Fonctionnalités debug
- `F1` : Afficher hitboxes (rectangles verts)
- `F2` : Passer au niveau suivant
- `F3` : Mode invincible
- Affichage FPS en haut à gauche

---

## 📝 Critères de réussite

### Obligatoires ✅
- ✅ Jouable du début à la fin
- ✅ Thème Guitar Hero visible
- ✅ Contrôles responsifs
- ✅ Aucun bug bloquant
- ✅ Code propre et commenté

### Bonus ⭐
- 2 personnages jouables
- Système rythme fonctionnel
- Boss avec phases
- Animations fluides
- Sons immersifs

---

## 🎓 Stack technique

- **Langage** : Python 3.8+
- **Framework** : Pygame 2.x
- **Architecture** : POO (classes, héritage)
- **Patterns** : Système de scènes, sprites/groups, delta time

---

## 👥 Équipe

Groupe 3 - Piscine Python 2026

---

## 📄 Licence

Projet éducatif - Piscine Python

---

## 🙏 Remerciements

- Pascal Escalière & Virginie Sans (encadrants)
- Assets : [sources si utilisées]
- Inspiration : Mario, Guitar Hero

---

## 📞 Support

Pour toute question sur le projet :
1. Consulter la documentation dans `/docs`
2. Lire les fichiers dans `/.claude` pour Claude Code
3. Contacter les encadrants

---

**Bon courage ! 🎸🎮**