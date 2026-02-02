# Rockstar Bros - Contexte Projet

## Vue d'ensemble
Jeu de plateforme 2D inspiré de Mario avec une mécanique Guitar Hero intégrée. Le joueur incarne un guitariste traversant 3 niveaux (coulisses → scène → boss final) en combattant avec des ondes musicales.

**Deadline**: Projet de 5 jours (Piscine Python)
**Soutenance**: Jour 5 avec démo + code à livrer lundi 9 février 9h

## Stack technique
- **Langage**: Python 3
- **Framework**: Pygame
- **Architecture**: POO (Programmation Orientée Objet)
- **Structure**: Système de scènes (menu, gameplay, pause, game_over, victory)

## Fichiers clés du projet

### Core (racine)
- `main.py` - Boucle principale, gestion scènes, clock/FPS
- `settings.py` - Constantes globales (FPS, résolution, vitesses, chemins)

### Scènes (`/scenes`)
- `base.py` - Classe abstraite Scene (interface commune)
- `menu.py` - Écran menu (start/quit)
- `gameplay.py` - Cœur du jeu (joueur, ennemis, collisions, score)
- `pause.py` - Menu pause
- `game_over.py` - Écran défaite
- `victory.py` - Écran victoire

### Entités (`/entities` - optionnel si besoin de séparer)
- `player.py` - Classe joueur (mouvement, saut, attaque)
- `enemies.py` - Classes Hater et Rockstar
- `boss.py` - Boss final
- `projectile.py` - Ondes musicales

### Assets (`/assets`)
- `/images` - Tous les sprites (joueur, ennemis, décors, UI)
- `/sounds` - Sons et musiques

## Principes de structure Pygame (Piscine)

### Ce qui va dans `main.py`
```python
# ✅ À METTRE ICI
- pygame.init()
- Création fenêtre (screen)
- Clock / FPS
- Boucle principale (while running)
- pygame.event.get()
- Calcul dt (delta time)
- Switch de scènes
- pygame.display.flip()
- pygame.quit()
```

### Ce qui va dans `settings.py`
```python
# ✅ CONSTANTES GLOBALES UNIQUEMENT
WIDTH = 800
HEIGHT = 600
FPS = 60
PLAYER_SPEED = 8
JUMP_FORCE = 15
GRAVITY = 0.8

# Chemins
ASSETS_DIR = Path(__file__).parent / "assets"
IMG_DIR = ASSETS_DIR / "images"
SND_DIR = ASSETS_DIR / "sounds"

# Couleurs
BG_COLOR = (25, 25, 30)
WHITE = (255, 255, 255)
```

### Ce qui va dans les scènes
```python
# ✅ LOGIQUE MÉTIER
- Toute la logique de jeu
- Gestion des entités
- Collisions
- Score
- UI spécifique
- Transitions entre écrans

# ❌ PAS DE BOUCLE PRINCIPALE ICI
# Juste les méthodes : handle_event(), update(dt), draw(screen)
```

## Spécificités du projet

### 1. Système d'attaque rythmée
- Métronome interne (120 BPM simulé par timer)
- Barre visuelle type Guitar Hero
- Bonus dégâts si timing correct
- **Impératif**: Visible à l'écran (pas juste dans le code)

### 2. Deux personnages jouables
- Choix au menu
- Sprites différents mais gameplay identique
- 10 images sprites minimum

### 3. Trois niveaux
1. **Coulisses** (tutoriel) - 1 type ennemi, facile
2. **Scène** (challenge) - 2 types ennemis, pièges
3. **Boss** (arène) - Rockstar concurrente

### 4. Système de vie
- Joueur : 3 cœurs (icône guitare)
- Hater : 2 PV
- Rockstar : 3 PV
- Boss : 20 PV

### 5. UI/HUD obligatoires
- Vie (guitares)
- Score
- Combo (si timing activé)
- Barre Guitar Hero (métronome visible)

## Contraintes techniques

### Collisions
- Rectangulaires simples (AABB via pygame.Rect)
- Pas de moteur complexe
- `pygame.sprite.spritecollide()` suffit

### Physique
```python
# Gravité simple
velocity_y += GRAVITY
rect.y += velocity_y

# Saut
if on_ground and SPACE:
    velocity_y = -JUMP_FORCE

# Sol
if rect.bottom >= GROUND_Y:
    rect.bottom = GROUND_Y
    velocity_y = 0
    on_ground = True
```

### Sprites et Groups
```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = ...  # Surface
        self.rect = ...   # Rect pour collision/position
    
    def update(self, dt):
        # Logique mouvement
        pass

# Groupes pour gestion facilitée
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()

# Dans la boucle
all_sprites.update(dt)
all_sprites.draw(screen)
```

## Assets à créer (35-40 images max)

### Priorité HAUTE (MVP)
1. Joueur idle + run + jump (× 2 persos) = 6 images
2. Hater idle + hit = 2 images
3. Projectile onde = 1 image
4. Plateforme/sol simple = 1 image
5. Background coulisses = 1 image
6. UI vie (guitare pleine/vide) = 2 images
7. Barre Guitar Hero = 2 images

**Total MVP : ~15 images**

### Priorité MOYENNE
- Rockstar rival (idle + hit)
- Boss (idle + attaque + hit)
- Backgrounds scène + arène boss
- Collectibles (médiator, notes)
- Écrans menu/game_over/victory

### Priorité BASSE (si temps)
- Animations attaque (5 frames)
- Attaque ultime
- Plateformes mobiles
- Effets particules

## Workflow recommandé

### Jour 1 (Aujourd'hui)
1. ✅ Structure de base (main.py + settings.py + scenes/base.py)
2. ✅ Joueur qui bouge + saute
3. ✅ 1 plateforme + gravité
4. Assets placeholder (rectangles colorés)

### Jour 2
1. Attaque de base (projectile)
2. 1 ennemi Hater qui patrouille
3. Collisions joueur-ennemi-projectile
4. Système de vie basique

### Jour 3
1. Système Guitar Hero (barre + timing)
2. 3 niveaux (3 backgrounds + layouts différents)
3. Boss avec phases simples
4. Remplacement assets placeholder par vrais sprites

### Jour 4
1. UI/HUD complet
2. Sons (attaque, hit, musique)
3. Écrans menu/pause/game_over/victory
4. Polish et bugs

### Jour 5
1. Tests finaux
2. Préparation démo
3. Présentation orale

## Critères de réussite (Cahier des charges)

### Obligatoires
- ✅ Jouable du début à la fin
- ✅ Thème Guitar Hero visible (perso, attaques, barre rythme)
- ✅ Contrôles responsifs (pas de lag)
- ✅ Aucun bug bloquant (chutes infinies, collisions cassées)
- ✅ Code clair + constantes centralisées + commenté

### Bonus
- 2 personnages jouables
- Système de timing/combo fonctionnel
- Boss avec plusieurs phases
- Animations fluides
- Sons immersifs

## Commandes principales

### Contrôles joueur
- `←/→` : Déplacement gauche/droite
- `SPACE` : Saut
- `J` : Attaque musicale
- `K` : Attaque ultime (après jauge pleine)
- `ESC` : Pause

### Contrôles développement
- `F1` : Mode debug (afficher hitboxes)
- `F2` : Skip niveau (tests rapides)
- `F3` : Invincibilité (tests boss)

## Points d'attention pour Claude Code

1. **Toujours commencer par lire `settings.py`** pour les constantes
2. **Ne jamais mettre de logique métier dans `main.py`**
3. **Utiliser `dt` (delta time) pour tous les mouvements** (frame-rate independent)
4. **Respecter l'interface des scènes** (handle_event, update, draw)
5. **Grouper les sprites similaires** (all_sprites, enemies, projectiles)
6. **Assets manquants = rectangles colorés temporaires** (développement itératif)
7. **Commenter les sections complexes** (collisions, physique, boss AI)

## Structure minimale fonctionnelle

```
rockstar-bros/
├── main.py                 # 50 lignes max
├── settings.py             # Constantes uniquement
├── scenes/
│   ├── __init__.py
│   ├── base.py            # Interface Scene
│   ├── menu.py            # Simple : Start/Quit
│   └── gameplay.py        # Cœur du jeu (200-300 lignes OK pour piscine)
├── assets/
│   ├── images/
│   │   ├── player1_idle.png
│   │   ├── hater_idle.png
│   │   └── ...
│   └── sounds/
│       ├── attack.wav
│       └── music.mp3
└── README.md
```

**Pour une piscine de 5 jours, mieux vaut un jeu simple qui fonctionne qu'un jeu complexe buggé.**