# Guide Structure Pygame - Rockstar Bros

Ce fichier explique en détail la philosophie de structure Pygame recommandée pour la piscine.

---

## Principe général

Dans Pygame (une **bibliothèque**, pas un moteur), **c'est vous qui écrivez la boucle principale**. Il n'y a pas de "framework" qui impose une structure. Donc il faut s'en créer une pour éviter le chaos.

---

## Architecture en scènes

### Pourquoi des scènes ?

Un jeu a plusieurs "états" (menu, jeu, pause, game over). Sans organisation, on finit avec un `main.py` de 1000 lignes avec plein de `if current_state == "menu"`.

**Solution** : Une classe par écran du jeu.

### Interface commune (scenes/base.py)

```python
class Scene:
    """Toutes les scènes héritent de cette classe"""
    
    def __init__(self):
        self.next_scene = None  # Pour dire à main.py quelle scène charger
        self.quit = False       # Pour quitter le jeu
    
    def handle_event(self, event):
        """Gérer UN événement (clavier, souris, etc.)"""
        pass
    
    def update(self, dt):
        """Mettre à jour la logique (appelé à chaque frame)"""
        pass
    
    def draw(self, screen):
        """Dessiner sur l'écran (appelé après update)"""
        pass
    
    def enter(self):
        """Appelé quand on arrive sur cette scène (optionnel)"""
        pass
    
    def exit(self):
        """Appelé quand on quitte cette scène (optionnel)"""
        pass
```

### Exemple concret : MenuScene

```python
class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.Font(None, 64)
        self.options = ["PLAY", "QUIT"]
        self.selected = 0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                if self.selected == 0:
                    self.next_scene = "gameplay"  # Signal à main.py
                elif self.selected == 1:
                    self.quit = True
    
    def update(self, dt):
        # Pas de logique complexe dans un menu
        pass
    
    def draw(self, screen):
        screen.fill((20, 20, 30))
        
        # Titre
        title = self.font.render("ROCKSTAR BROS", True, (255, 255, 255))
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Options
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (200, 200, 200)
            text = self.font.render(option, True, color)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 300 + i*80))
```

---

## Main.py : le chef d'orchestre

### Rôle strict de main.py

**✅ Ce qu'il DOIT faire** :
1. Initialiser Pygame (`pygame.init()`)
2. Créer la fenêtre (`screen = pygame.display.set_mode(...)`)
3. Créer le `Clock` pour gérer les FPS
4. Créer un dictionnaire des scènes disponibles
5. Boucle principale :
   - Calculer `dt` (delta time)
   - Récupérer événements (`pygame.event.get()`)
   - Passer événements à la scène active
   - Appeler `update(dt)` de la scène
   - Appeler `draw(screen)` de la scène
   - `pygame.display.flip()`
   - Gérer changement de scène si `current_scene.next_scene` est défini
6. Quitter proprement (`pygame.quit()`)

**❌ Ce qu'il NE DOIT PAS faire** :
- Logique de jeu (mouvement, collisions, score, etc.)
- Créer des entités directement
- Gérer l'UI
- Charger des assets (sauf si ressources globales partagées)

### Template main.py

```python
import pygame
from settings import WIDTH, HEIGHT, FPS
from scenes.menu import MenuScene
from scenes.gameplay import GameplayScene
from scenes.game_over import GameOverScene
from scenes.victory import VictoryScene

def main():
    # Initialisation
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Rockstar Bros")
    clock = pygame.time.Clock()
    
    # Dictionnaire des scènes
    scenes = {
        "menu": MenuScene(),
        "gameplay": GameplayScene(),
        "game_over": GameOverScene(),
        "victory": VictoryScene(),
    }
    
    # Scène de départ
    current_scene = scenes["menu"]
    current_scene.enter()
    
    # Boucle principale
    running = True
    while running:
        # Delta time (en secondes)
        dt = clock.tick(FPS) / 1000.0
        
        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                current_scene.handle_event(event)
        
        # Update
        current_scene.update(dt)
        
        # Draw
        screen.fill((0, 0, 0))  # Optionnel si scènes gèrent leur fond
        current_scene.draw(screen)
        pygame.display.flip()
        
        # Changement de scène
        if current_scene.quit:
            running = False
        elif current_scene.next_scene:
            next_key = current_scene.next_scene
            current_scene.exit()
            current_scene = scenes[next_key]
            current_scene.enter()
            current_scene.next_scene = None  # Reset
    
    pygame.quit()

if __name__ == "__main__":
    main()
```

**Total : ~60 lignes.** Si votre `main.py` dépasse 100 lignes, quelque chose ne va pas.

---

## Settings.py : le panneau de contrôle

### Rôle de settings.py

**✅ Uniquement des constantes** :
- Dimensions fenêtre (`WIDTH`, `HEIGHT`)
- FPS
- Couleurs (RGB tuples)
- Vitesses (joueur, ennemis, projectiles)
- Forces (gravité, saut)
- HP (joueur, ennemis, boss)
- Chemins vers assets
- Config système rythme (BPM, etc.)

**❌ Pas de** :
- Classes
- Fonctions complexes
- Logique Pygame (pas de `pygame.init`, `pygame.display`, etc.)
- Imports de scènes ou entités

### Template settings.py

```python
from pathlib import Path

# === FENÊTRE ===
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "Rockstar Bros"

# === COULEURS ===
BG_COLOR = (25, 25, 30)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# === CHEMINS ===
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "images"
SND_DIR = ASSETS_DIR / "sounds"

# === JOUEUR ===
PLAYER_SPEED = 300  # pixels/seconde
PLAYER_JUMP_FORCE = 500
PLAYER_HP = 3
PLAYER_ATTACK_COOLDOWN = 0.35  # secondes

# === PHYSIQUE ===
GRAVITY = 1200  # pixels/seconde²
GROUND_Y = HEIGHT - 100

# === ENNEMIS ===
HATER_HP = 2
HATER_SPEED = 100
HATER_DAMAGE = 1

ROCKSTAR_HP = 3
ROCKSTAR_SPEED = 150
ROCKSTAR_DAMAGE = 1

BOSS_HP = 20
BOSS_SPEED = 200
BOSS_DAMAGE = 2

# === PROJECTILES ===
PROJECTILE_SPEED = 400
PROJECTILE_DAMAGE = 1
PROJECTILE_PERFECT_MULTIPLIER = 1.5

# === SYSTÈME RYTHME ===
BPM = 120
BEAT_DURATION = 60 / BPM  # Secondes
PERFECT_TIMING_WINDOW = 0.1  # ±0.1s autour du beat

# === NIVEAUX ===
LEVELS = {
    1: {
        "name": "Backstage",
        "background": IMG_DIR / "backgrounds" / "backstage.png",
        "enemies": ["hater"],
        "checkpoint_x": 400,
    },
    2: {
        "name": "Stage",
        "background": IMG_DIR / "backgrounds" / "stage.png",
        "enemies": ["hater", "rockstar"],
        "checkpoint_x": 600,
    },
    3: {
        "name": "Boss Arena",
        "background": IMG_DIR / "backgrounds" / "boss_arena.png",
        "enemies": [],
        "boss": True,
    },
}
```

---

## GameplayScene : le cœur du jeu

### Responsabilités

C'est ici que **TOUT le gameplay** se passe :
- Créer joueur, ennemis, projectiles, plateformes
- Gérer collisions
- Calculer score, combo
- Détecter victoire/défaite
- Afficher HUD

### Structure recommandée

```python
class GameplayScene(Scene):
    def __init__(self):
        super().__init__()
        
        # === GROUPES PYGAME ===
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        
        # === ENTITÉS ===
        self.player = None  # Créé dans enter()
        self.boss = None
        
        # === ÉTAT JEU ===
        self.level = 1
        self.score = 0
        self.combo = 0
        
        # === SYSTÈMES ===
        self.rhythm = RhythmSystem()
        
        # === UI ===
        self.font = pygame.font.Font(None, 32)
        self.load_ui_assets()
    
    def enter(self):
        """Appelé quand on commence le niveau"""
        self.setup_level(self.level)
    
    def setup_level(self, level_num):
        """Créer entités pour un niveau donné"""
        # Charger config niveau depuis settings.py
        config = LEVELS[level_num]
        
        # Créer joueur
        self.player = Player(100, GROUND_Y)
        self.all_sprites.add(self.player)
        
        # Créer ennemis
        if "hater" in config["enemies"]:
            hater = Hater(400, GROUND_Y)
            self.enemies.add(hater)
            self.all_sprites.add(hater)
        
        # Créer plateformes
        platform = Platform(300, 400, 200, 20)
        self.platforms.add(platform)
        self.all_sprites.add(platform)
        
        # Boss si niveau 3
        if config.get("boss"):
            self.boss = Boss(600, GROUND_Y)
            self.enemies.add(self.boss)
            self.all_sprites.add(self.boss)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                self.player_attack()
            elif event.key == pygame.K_k:
                self.player_ultimate()
            elif event.key == pygame.K_ESCAPE:
                self.next_scene = "pause"
    
    def update(self, dt):
        # Update entités
        self.all_sprites.update(dt)
        
        # Update système rythme
        self.rhythm.update(dt)
        
        # Collisions
        self.check_collisions()
        
        # Conditions fin
        if self.player.hp <= 0:
            self.next_scene = "game_over"
        elif self.boss and self.boss.hp <= 0:
            self.next_scene = "victory"
    
    def draw(self, screen):
        # Background
        screen.fill((40, 40, 50))  # Ou blit image
        
        # Entités
        self.all_sprites.draw(screen)
        
        # HUD
        self.draw_hud(screen)
        
        # Barre rythme
        self.rhythm.draw(screen)
    
    def check_collisions(self):
        """Gérer toutes les collisions"""
        # Projectiles ↔ Ennemis
        hits = pygame.sprite.groupcollide(
            self.projectiles,
            self.enemies,
            True,   # Détruire projectile
            False   # Ne pas détruire ennemi (on gère HP)
        )
        for projectile, enemies_hit in hits.items():
            for enemy in enemies_hit:
                damage = projectile.damage
                if self.rhythm.is_perfect_timing():
                    damage *= PROJECTILE_PERFECT_MULTIPLIER
                    self.combo += 1
                enemy.take_damage(damage)
                self.score += 10
        
        # Joueur ↔ Ennemis
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits and self.player.can_take_damage():
            self.player.take_damage(hits[0].damage)
            self.combo = 0
        
        # Joueur ↔ Plateformes
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.land_on(hits[0])
        
        # Joueur ↔ Collectibles
        hits = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        for collectible in hits:
            collectible.apply_effect(self.player)
            self.score += collectible.points
    
    def player_attack(self):
        """Créer projectile si cooldown OK"""
        if self.player.can_attack():
            direction = 1 if self.player.facing_right else -1
            projectile = Projectile(
                self.player.rect.centerx,
                self.player.rect.centery,
                direction
            )
            self.projectiles.add(projectile)
            self.all_sprites.add(projectile)
            self.player.attack()
    
    def draw_hud(self, screen):
        """Afficher vie, score, combo"""
        # Vie (guitares)
        for i in range(self.player.hp):
            screen.blit(self.heart_full, (10 + i*40, 10))
        for i in range(self.player.hp, PLAYER_HP):
            screen.blit(self.heart_empty, (10 + i*40, 10))
        
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH - 200, 10))
        
        # Combo
        if self.combo > 0:
            combo_text = self.font.render(f"Combo x{self.combo}", True, YELLOW)
            screen.blit(combo_text, (WIDTH // 2 - 50, 10))
```

**Note** : Ce fichier peut faire 200-300 lignes, c'est normal pour une piscine. Si ça dépasse 500, envisager de séparer en fichiers `entities/`.

---

## Système de sprites et groupes

### Pourquoi des sprites ?

**pygame.sprite.Sprite** fournit une structure standard :
- `self.image` : La Surface à afficher
- `self.rect` : Rectangle pour position ET collision

**pygame.sprite.Group** permet :
- `group.update(dt)` : Appeler `update()` sur tous les sprites
- `group.draw(screen)` : Dessiner tous les sprites automatiquement

### Exemple : Classe Enemy

```python
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, hp, speed):
        super().__init__()
        
        # Visuel
        self.image = pygame.image.load(IMG_DIR / "enemies" / "hater.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        
        # Stats
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.damage = 1
        
        # Comportement
        self.direction = 1  # 1 = droite, -1 = gauche
        self.patrol_timer = 0
        self.patrol_duration = 2.0
    
    def update(self, dt):
        # Patrouille
        self.patrol_timer += dt
        if self.patrol_timer >= self.patrol_duration:
            self.direction *= -1
            self.patrol_timer = 0
        
        self.rect.x += self.speed * self.direction * dt
        
        # Mort si HP <= 0
        if self.hp <= 0:
            self.kill()  # Retire du groupe automatiquement
    
    def take_damage(self, amount):
        self.hp -= amount
```

### Collisions avec groupes

```python
# Sprite vs Group
hits = pygame.sprite.spritecollide(player, enemies, False)
# Retourne liste d'ennemis touchant player

# Group vs Group
hits = pygame.sprite.groupcollide(projectiles, enemies, True, False)
# Retourne dict {projectile: [ennemis touchés]}
```

---

## Delta Time (dt) : indépendance des FPS

### Problème sans dt

```python
# ❌ MAUVAIS
player.rect.x += 5  # Bouge de 5 pixels par frame

# Si 60 FPS → 300 pixels/seconde
# Si 30 FPS → 150 pixels/seconde
# Gameplay différent selon machine !
```

### Solution avec dt

```python
# ✅ BON
PLAYER_SPEED = 300  # pixels par SECONDE

player.rect.x += PLAYER_SPEED * dt  # dt = fraction de seconde

# Si 60 FPS (dt ≈ 0.0167s) → 300 * 0.0167 = 5 pixels/frame
# Si 30 FPS (dt ≈ 0.0333s) → 300 * 0.0333 = 10 pixels/frame
# Même vitesse réelle !
```

### Obtenir dt

```python
# Dans main.py
dt = clock.tick(FPS) / 1000.0  # Convertir ms en secondes
```

### Utiliser dt partout

```python
# Mouvement
rect.x += velocity_x * dt
rect.y += velocity_y * dt

# Gravité
velocity_y += GRAVITY * dt

# Timers
cooldown_timer -= dt
if cooldown_timer <= 0:
    can_attack = True
```

---

## Système de coordonnées Pygame

```
(0,0) ────────────────────→ X (WIDTH)
  │
  │
  │
  │
  │
  ↓
  Y (HEIGHT)
```

- **(0, 0)** = coin supérieur gauche
- **X croissant** = vers la droite
- **Y croissant** = vers le BAS (inversé par rapport aux maths !)

### Positions des Rect

```python
rect = pygame.Rect(0, 0, 64, 64)

# Coins
rect.topleft = (x, y)      # Coin haut-gauche
rect.topright = (x, y)     # Coin haut-droite
rect.bottomleft = (x, y)   # Coin bas-gauche
rect.bottomright = (x, y)  # Coin bas-droite

# Centres
rect.center = (x, y)       # Centre complet
rect.centerx = x           # Centre horizontal
rect.centery = y           # Centre vertical
rect.midtop = (x, y)       # Milieu bord haut
rect.midbottom = (x, y)    # Milieu bord bas

# Côtés (valeurs scalaires)
rect.left = x
rect.right = x
rect.top = y
rect.bottom = y

# Dimensions
rect.width
rect.height
rect.size  # (width, height)
```

---

## Récapitulatif : Qui fait quoi ?

| Fichier | Responsabilité | Lignes typiques |
|---------|----------------|-----------------|
| `main.py` | Boucle principale, switch scènes | 50-70 |
| `settings.py` | Constantes globales | 50-100 |
| `scenes/base.py` | Interface Scene | 20-30 |
| `scenes/menu.py` | Menu, navigation | 50-80 |
| `scenes/gameplay.py` | **Tout le jeu** | 200-400 |
| `scenes/pause.py` | Menu pause | 40-60 |
| `scenes/game_over.py` | Écran défaite | 40-60 |
| `scenes/victory.py` | Écran victoire | 40-60 |
| `entities/player.py` | Logique joueur | 100-150 |
| `entities/enemies.py` | Classes ennemis | 150-200 |
| `entities/boss.py` | Boss (si complexe) | 100-200 |
| `systems/rhythm.py` | Système Guitar Hero | 80-120 |

**Total projet** : 1000-1500 lignes pour un jeu piscine complet. C'est raisonnable.

---

## Checklist structure propre

### ✅ Bon signe
- `main.py` < 100 lignes
- `settings.py` = que des constantes
- Chaque scène hérite de `Scene`
- Toutes les entités sont des `pygame.sprite.Sprite`
- Utilisation de `dt` partout
- Groupes pour organiser sprites
- Collisions via `sprite.spritecollide` ou `groupcollide`

### ❌ Mauvais signe
- `main.py` > 200 lignes
- Logique dans `settings.py`
- `if current_state == "menu"` partout dans main
- Mouvement sans `dt`
- Création d'entités directement dans `main.py`
- Calculs de collision manuels complexes

---

## Patterns anti-bug

### 1. Toujours initialiser les sprites correctement

```python
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # ← NE PAS OUBLIER
        self.image = ...
        self.rect = ...
```

### 2. Gérer assets manquants

```python
try:
    image = pygame.image.load(path).convert_alpha()
except (pygame.error, FileNotFoundError):
    # Placeholder
    image = pygame.Surface((64, 64))
    image.fill((255, 0, 255))  # Rose = "missing texture"
```

### 3. Clamp position dans écran

```python
# Empêcher sortie écran
rect.left = max(rect.left, 0)
rect.right = min(rect.right, WIDTH)
rect.top = max(rect.top, 0)
rect.bottom = min(rect.bottom, HEIGHT)
```

### 4. Détection sol fiable

```python
# Gravité
if not on_ground:
    velocity_y += GRAVITY * dt

# Mouvement vertical
rect.y += velocity_y * dt

# Check sol
if rect.bottom >= GROUND_Y:
    rect.bottom = GROUND_Y
    velocity_y = 0
    on_ground = True
else:
    on_ground = False
```

---

## Conseils finaux

1. **Commencer simple** : Joueur qui bouge + 1 plateforme
2. **Tester à chaque étape** : Ne pas coder 200 lignes avant de lancer
3. **Utiliser placeholders** : Rectangles colorés > attendre assets
4. **Respecter l'architecture** : Ne pas tout mettre dans `main.py`
5. **Commenter sections complexes** : Collisions, physique, boss AI

**Cette structure a fait ses preuves sur des dizaines de projets piscine. Elle fonctionne.**