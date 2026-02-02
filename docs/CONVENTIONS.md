# Conventions de code - Rockstar Bros

## Nommage

### Variables et fonctions : `snake_case`
```python
player_speed = 300
jump_force = 500

def check_collisions():
    pass

def calculate_damage(base, multiplier):
    pass
```

### Classes : `PascalCase`
```python
class Player:
    pass

class GameplayScene:
    pass

class RhythmSystem:
    pass
```

### Constantes : `UPPER_SNAKE_CASE`
```python
WIDTH = 800
HEIGHT = 600
PLAYER_MAX_HP = 3
PERFECT_TIMING_WINDOW = 0.1
```

### Fichiers : `snake_case.py`
```
main.py
settings.py
rhythm_system.py
```

---

## Organisation du code

### Imports

Ordre recommandé :
```python
# 1. Standard library
import random
from pathlib import Path

# 2. Third-party
import pygame

# 3. Local
from settings import WIDTH, HEIGHT, PLAYER_SPEED
from scenes.base import Scene
```

### Structure d'une classe

```python
class Player(pygame.sprite.Sprite):
    """Classe joueur avec mouvement et attaque"""
    
    def __init__(self, x, y):
        """
        Initialise le joueur.
        
        Args:
            x: Position X initiale
            y: Position Y initiale
        """
        super().__init__()
        
        # === VISUEL ===
        self.image = ...
        self.rect = ...
        
        # === STATS ===
        self.hp = PLAYER_HP
        self.speed = PLAYER_SPEED
        
        # === ÉTAT ===
        self.velocity_x = 0
        self.velocity_y = 0
        self.facing_right = True
        self.on_ground = False
    
    # === MÉTHODES PUBLIQUES ===
    
    def update(self, dt):
        """Update logique (appelé chaque frame)"""
        self._handle_input()
        self._apply_physics(dt)
        self._update_animation()
    
    def take_damage(self, amount):
        """Prendre des dégâts"""
        self.hp -= amount
        if self.hp <= 0:
            self.kill()
    
    # === MÉTHODES PRIVÉES ===
    
    def _handle_input(self):
        """Gérer input clavier (privé)"""
        keys = pygame.key.get_pressed()
        # ...
    
    def _apply_physics(self, dt):
        """Appliquer gravité et mouvement"""
        # ...
```

---

## Commentaires

### Docstrings (classes et fonctions publiques)

```python
def calculate_damage(base_damage, is_perfect_timing):
    """
    Calcule les dégâts finaux d'une attaque.
    
    Args:
        base_damage (int): Dégâts de base du projectile
        is_perfect_timing (bool): True si attaque au bon moment
    
    Returns:
        float: Dégâts finaux (avec multiplicateur si timing parfait)
    """
    multiplier = PROJECTILE_PERFECT_MULTIPLIER if is_perfect_timing else 1.0
    return base_damage * multiplier
```

### Commentaires inline (pour clarifier)

```python
# ✅ BON : Explique POURQUOI, pas QUOI
if rect.bottom >= GROUND_Y:
    rect.bottom = GROUND_Y
    velocity_y = 0
    on_ground = True  # Nécessaire pour autoriser le prochain saut

# ❌ MAUVAIS : Redondant
on_ground = True  # Met on_ground à True
```

### Sections de code

Pour structurer un gros fichier :
```python
class GameplayScene(Scene):
    def __init__(self):
        # === GROUPES ===
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # === ENTITÉS ===
        self.player = None
        self.boss = None
        
        # === ÉTAT JEU ===
        self.score = 0
        self.level = 1
        
        # === SYSTÈMES ===
        self.rhythm = RhythmSystem()
```

---

## Gestion des constantes

### ✅ Utiliser settings.py

```python
# settings.py
PLAYER_SPEED = 300
JUMP_FORCE = 500

# player.py
from settings import PLAYER_SPEED, JUMP_FORCE

class Player:
    def __init__(self):
        self.speed = PLAYER_SPEED
        self.jump_force = JUMP_FORCE
```

### ❌ Éviter les valeurs magiques

```python
# ❌ MAUVAIS
if self.combo > 5:  # Pourquoi 5 ?
    bonus = 1.5     # Pourquoi 1.5 ?

# ✅ BON
COMBO_THRESHOLD = 5
COMBO_BONUS_MULTIPLIER = 1.5

if self.combo > COMBO_THRESHOLD:
    bonus = COMBO_BONUS_MULTIPLIER
```

---

## Gestion des assets

### Chemins relatifs via settings.py

```python
# settings.py
from pathlib import Path

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "images"

# Utilisation
player_img_path = IMG_DIR / "player" / "hero1_idle.png"
```

### Fallback si asset manquant

```python
def load_image(path, fallback_color=(255, 0, 255)):
    """
    Charge une image avec fallback si introuvable.
    
    Args:
        path: Chemin vers l'image
        fallback_color: Couleur du placeholder (rose par défaut)
    
    Returns:
        pygame.Surface
    """
    try:
        return pygame.image.load(path).convert_alpha()
    except (pygame.error, FileNotFoundError):
        # Créer placeholder
        surf = pygame.Surface((64, 64))
        surf.fill(fallback_color)
        return surf
```

---

## Gestion des erreurs

### Try/except pour ressources externes

```python
# ✅ BON
try:
    font = pygame.font.Font("assets/fonts/custom.ttf", 32)
except (pygame.error, FileNotFoundError):
    font = pygame.font.Font(None, 32)  # Police par défaut
```

### Assertions pour vérifier l'état

```python
def setup_level(self, level_num):
    assert 1 <= level_num <= 3, f"Niveau invalide : {level_num}"
    
    config = LEVELS[level_num]
    # ...
```

---

## Patterns recommandés

### 1. Éviter répétition avec dict

```python
# ❌ MAUVAIS
if enemy_type == "hater":
    hp = 2
    speed = 100
elif enemy_type == "rockstar":
    hp = 3
    speed = 150

# ✅ BON
ENEMY_STATS = {
    "hater": {"hp": 2, "speed": 100},
    "rockstar": {"hp": 3, "speed": 150},
}

stats = ENEMY_STATS[enemy_type]
hp = stats["hp"]
speed = stats["speed"]
```

### 2. Timer avec delta time

```python
class Enemy:
    def __init__(self):
        self.patrol_timer = 0
        self.patrol_duration = 2.0
    
    def update(self, dt):
        self.patrol_timer += dt
        
        if self.patrol_timer >= self.patrol_duration:
            self.direction *= -1  # Inverser
            self.patrol_timer = 0  # Reset
```

### 3. State machine simple

```python
class Player:
    def get_current_animation(self):
        """Retourne nom animation selon état"""
        if not self.on_ground:
            return "jump"
        elif abs(self.velocity_x) > 0:
            return "run"
        else:
            return "idle"
    
    def update_animation(self):
        anim_name = self.get_current_animation()
        self.image = self.animations[anim_name][self.frame_index]
```

---

## Debug et tests

### Mode debug avec flag

```python
# settings.py
DEBUG_MODE = True  # Activer/désactiver facilement

# gameplay.py
if DEBUG_MODE:
    # Afficher hitboxes
    pygame.draw.rect(screen, (0, 255, 0), self.player.rect, 2)
    
    # Afficher FPS
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, (255, 255, 0))
    screen.blit(fps_text, (10, 50))
```

### Raccourcis debug

```python
def handle_event(self, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F1:
            self.debug_mode = not self.debug_mode
        elif event.key == pygame.K_F2 and DEBUG_MODE:
            self.skip_level()  # Passer niveau
        elif event.key == pygame.K_F3 and DEBUG_MODE:
            self.player.invincible = not self.player.invincible
```

---

## Performance

### Éviter calculs inutiles

```python
# ❌ MAUVAIS (calcule chaque frame)
for sprite in sprites:
    distance = ((sprite.rect.x - player.rect.x)**2 + 
                (sprite.rect.y - player.rect.y)**2)**0.5
    if distance < 200:
        # ...

# ✅ BON (évite racine carrée)
for sprite in sprites:
    dx = sprite.rect.x - player.rect.x
    dy = sprite.rect.y - player.rect.y
    distance_squared = dx*dx + dy*dy
    
    if distance_squared < 200*200:  # Comparer carrés
        # ...
```

### Limiter créations d'objets

```python
# ❌ MAUVAIS (crée tuple chaque frame)
def draw(self, screen):
    pos = (self.rect.x, self.rect.y)
    screen.blit(self.image, pos)

# ✅ BON (utilise rect directement)
def draw(self, screen):
    screen.blit(self.image, self.rect)
```

---

## Git (si utilisé)

### .gitignore recommandé

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/

# Pygame
*.wav~
*.ogg~

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Assets temporaires
assets/temp/
```

### Messages de commit

```bash
# ✅ BON
git commit -m "Ajout système de saut avec gravité"
git commit -m "Fix collision joueur-plateforme"
git commit -m "Ajout barre Guitar Hero avec timing"

# ❌ MAUVAIS
git commit -m "update"
git commit -m "fix bug"
git commit -m "ajout trucs"
```

---

## Checklist avant rendu

### Code
- [ ] Pas de `print()` debug oubliés
- [ ] Tous les imports utilisés
- [ ] Pas de variables inutilisées
- [ ] Constantes dans `settings.py`
- [ ] Commentaires sur parties complexes

### Structure
- [ ] `main.py` < 100 lignes
- [ ] Scènes héritent de `Scene`
- [ ] Sprites héritent de `pygame.sprite.Sprite`
- [ ] Utilisation de `dt` pour mouvements

### Fonctionnalités
- [ ] Jeu jouable début à fin
- [ ] Pas de crash/freeze
- [ ] FPS stable (afficher avec F1 en debug)
- [ ] Tous assets nécessaires présents (ou placeholders)

### Polish
- [ ] README.md avec instructions
- [ ] Pas de warnings/erreurs console
- [ ] Sons fonctionnels (si présents)
- [ ] UI lisible et claire

---

## Ressources

### Documentation officielle
- Pygame : https://www.pygame.org/docs/
- Python : https://docs.python.org/3/

### Tutoriels recommandés
- Real Python - Pygame : https://realpython.com/pygame-a-primer/
- Clear Code (YouTube) : Pygame tutorials

### Assets gratuits
- OpenGameArt.org
- Itch.io (assets gratuits)
- Kenney.nl (sprites CC0)

---

**Ces conventions aident à maintenir un code propre et professionnel. Suivez-les autant que possible !**