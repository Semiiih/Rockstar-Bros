# Architecture technique - Rockstar Bros

## Arborescence complète du projet

```
rockstar-bros/
│
├── .claude/                          # Documentation pour Claude Code
│   ├── project-context.md            # ⭐ Contexte principal (lire en premier)
│   ├── architecture.md               # Ce fichier
│   └── asset-tracker.md              # Liste assets + statut
│
├── main.py                           # 🎮 Entry point + game loop
├── settings.py                       # ⚙️ Constantes globales
├── settings.py                       # ⚙️ Constantes globales
│
├── scenes/                           # 📦 États du jeu
│   ├── __init__.py
│   ├── base.py                       # Classe abstraite Scene
│   ├── menu.py                       # Menu principal
│   ├── character_select.py           # Choix personnage (optionnel)
│   ├── gameplay.py                   # ⭐ Jeu principal
│   ├── pause.py                      # Menu pause
│   ├── game_over.py                  # Écran défaite
│   └── victory.py                    # Écran victoire
│
├── entities/                         # 🎭 Entités du jeu (optionnel si gameplay.py trop gros)
│   ├── __init__.py
│   ├── player.py                     # Classe Player
│   ├── enemies.py                    # Hater + Rockstar
│   ├── boss.py                       # Boss final
│   ├── projectile.py                 # Ondes musicales
│   └── platform.py                   # Plateformes (si mobiles)
│
├── systems/                          # 🔧 Systèmes utilitaires (optionnel)
│   ├── __init__.py
│   ├── rhythm.py                     # Système Guitar Hero
│   ├── collision.py                  # Helpers collision avancés
│   └── camera.py                     # Caméra (si scrolling horizontal)
│
├── ui/                               # 🎨 Interface utilisateur (optionnel)
│   ├── __init__.py
│   ├── hud.py                        # Barre vie, score, combo
│   └── rhythm_bar.py                 # Barre Guitar Hero
│
├── assets/                           # 📁 Ressources externes
│   ├── images/
│   │   ├── player/
│   │   │   ├── hero1_idle.png
│   │   │   ├── hero1_run_1.png
│   │   │   ├── hero1_run_2.png
│   │   │   ├── hero1_jump.png
│   │   │   ├── hero1_attack_1.png
│   │   │   ├── hero2_idle.png
│   │   │   └── ...
│   │   ├── enemies/
│   │   │   ├── hater_idle.png
│   │   │   ├── hater_hit.png
│   │   │   ├── rockstar_idle.png
│   │   │   └── rockstar_hit.png
│   │   ├── boss/
│   │   │   ├── boss_idle.png
│   │   │   ├── boss_attack.png
│   │   │   ├── boss_projectile.png
│   │   │   └── boss_shockwave.png
│   │   ├── attacks/
│   │   │   ├── sound_wave.png
│   │   │   ├── ultimate.png
│   │   │   └── impact.png
│   │   ├── platforms/
│   │   │   ├── crate.png
│   │   │   ├── amp.png
│   │   │   └── flight_case.png
│   │   ├── backgrounds/
│   │   │   ├── backstage.png
│   │   │   ├── stage.png
│   │   │   └── boss_arena.png
│   │   ├── collectibles/
│   │   │   ├── pick.png
│   │   │   ├── note.png
│   │   │   └── amp_bonus.png
│   │   ├── ui/
│   │   │   ├── heart_full.png         # Icône guitare pleine
│   │   │   ├── heart_empty.png        # Icône guitare vide
│   │   │   ├── rhythm_bar_bg.png      # Fond barre Guitar Hero
│   │   │   ├── rhythm_cursor.png      # Curseur métronome
│   │   │   └── rhythm_zone.png        # Zone parfaite
│   │   └── screens/
│   │       ├── menu_bg.png
│   │       ├── pause_bg.png
│   │       ├── gameover_bg.png
│   │       └── victory_bg.png
│   │
│   └── sounds/
│       ├── music/
│       │   ├── menu.mp3
│       │   ├── level1.mp3
│       │   ├── level2.mp3
│       │   └── boss.mp3
│       ├── sfx/
│       │   ├── jump.wav
│       │   ├── attack.wav
│       │   ├── hit.wav
│       │   ├── perfect_hit.wav        # Timing parfait
│       │   ├── collect.wav
│       │   └── ui_click.wav
│       └── rhythm/
│           └── metronome_tick.wav
│
├── docs/                             # 📚 Documentation projet
│   ├── CAHIER_DES_CHARGES.md         # Cahier des charges complet
│   ├── STRUCTURE.md                  # Guide structure Pygame
│   └── CONVENTIONS.md                # Conventions de code
│
└── README.md                         # Vue d'ensemble + installation
└── START.md                         # Vue d'ensemble + installation

```

---

## Flux de données et interactions

### 1. Démarrage application

```
main.py
  ↓
pygame.init()
  ↓
Charger settings.py (FPS, résolution, chemins)
  ↓
Créer screen (fenêtre)
  ↓
Initialiser scène = MenuScene
  ↓
Lancer game loop
```

### 2. Game Loop (main.py)

```python
while running:
    # 1. Timing
    dt = clock.tick(FPS) / 1000  # Secondes
    
    # 2. Événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        current_scene.handle_event(event)
    
    # 3. Update logique
    current_scene.update(dt)
    
    # 4. Rendu
    screen.fill(BG_COLOR)
    current_scene.draw(screen)
    pygame.display.flip()
    
    # 5. Changement de scène
    if current_scene.next_scene:
        current_scene = scenes[current_scene.next_scene]
        current_scene.enter()
```

### 3. Scène Gameplay (cœur du jeu)

```
GameplayScene.update(dt)
  ↓
1. Player.update(dt)
   - Input clavier (←/→/SPACE/J)
   - Appliquer gravité
   - Déplacer rect
   - Gérer animations
  ↓
2. Enemies.update(dt)
   - Patrouille ou suivi joueur
   - Animations
  ↓
3. Projectiles.update(dt)
   - Mouvement
   - Détruire si hors écran
  ↓
4. Rhythm system.update(dt)
   - Avancer métronome
   - Détecter zone parfaite
  ↓
5. Collisions
   - Joueur ↔ Ennemis (dégâts)
   - Projectiles ↔ Ennemis (tuer)
   - Joueur ↔ Sol (atterrissage)
   - Joueur ↔ Collectibles (bonus)
  ↓
6. Vérifier conditions fin
   - Vie joueur = 0 → game_over
   - Boss mort → victory
   - Checkpoints
```

### 4. Changement de scène

```python
# Dans une scène
self.next_scene = "game_over"  # Signal au main

# Dans main.py
if current_scene.next_scene:
    new_scene_key = current_scene.next_scene
    current_scene.exit()  # Nettoyage
    current_scene = scenes[new_scene_key]
    current_scene.enter()  # Init nouvelle scène
```

---

## Responsabilités par fichier

### `main.py` (50 lignes max)
```python
# ✅ RESPONSABILITÉS
- pygame.init() / pygame.quit()
- Créer fenêtre (screen)
- Gérer clock.tick(FPS)
- Boucle while running
- Appeler current_scene.handle_event / update / draw
- Gérer switch de scènes

# ❌ INTERDICTIONS
- Aucune logique métier
- Pas de calculs de gameplay
- Pas de création d'entités directement
```

### `settings.py` (constantes uniquement)
```python
# ✅ À METTRE
WIDTH, HEIGHT, FPS
PLAYER_SPEED, JUMP_FORCE, GRAVITY
Couleurs (BG_COLOR, WHITE, etc.)
Chemins (ASSETS_DIR, IMG_DIR, SND_DIR)
Config ennemis (HATER_HP, ROCKSTAR_HP, BOSS_HP)
Config timing (BPM, PERFECT_TIMING_WINDOW)

# ❌ PAS DE
- Classes
- Fonctions complexes
- Logique Pygame (pas de pygame.init, etc.)
```

### `scenes/base.py` (interface)
```python
class Scene:
    """Classe abstraite pour toutes les scènes"""
    
    def __init__(self):
        self.next_scene = None
        self.quit = False
    
    def handle_event(self, event):
        """Gérer input utilisateur"""
        pass
    
    def update(self, dt):
        """Logique de la scène (appelé chaque frame)"""
        pass
    
    def draw(self, screen):
        """Rendu visuel (appelé après update)"""
        pass
    
    def enter(self):
        """Appelé quand on arrive sur la scène"""
        pass
    
    def exit(self):
        """Appelé quand on quitte la scène"""
        pass
```

### `scenes/gameplay.py` (200-300 lignes OK)
```python
# ✅ RESPONSABILITÉS
- Créer joueur, ennemis, plateformes
- Gérer collisions (sprite.spritecollide)
- Calculer score/combo
- Gérer vie joueur/ennemis
- Détecter conditions victoire/défaite
- Afficher HUD (vie, score, barre rythme)
- Gérer niveau actuel (1/2/3)

# STRUCTURE RECOMMANDÉE
class GameplayScene(Scene):
    def __init__(self):
        # Groupes
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        
        # Entités
        self.player = Player(x, y)
        self.all_sprites.add(self.player)
        
        # État jeu
        self.score = 0
        self.combo = 0
        self.level = 1
        
        # Système rythme
        self.rhythm = RhythmSystem()
        
        # UI
        self.font = pygame.font.Font(None, 36)
        self.load_ui_sprites()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                self.player_attack()
            elif event.key == pygame.K_ESCAPE:
                self.next_scene = "pause"
    
    def update(self, dt):
        # Update entités
        self.all_sprites.update(dt)
        
        # Update rythme
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
        screen.blit(self.bg, (0, 0))
        
        # Entités
        self.all_sprites.draw(screen)
        
        # HUD
        self.draw_hud(screen)
        self.rhythm.draw(screen)
    
    def check_collisions(self):
        # Projectiles ↔ Ennemis
        hits = pygame.sprite.groupcollide(
            self.projectiles, 
            self.enemies, 
            True,  # Détruire projectile
            False  # Ne pas détruire ennemi (on gère HP)
        )
        for projectile, enemies_hit in hits.items():
            for enemy in enemies_hit:
                enemy.take_damage(projectile.damage)
                self.score += 10
        
        # Joueur ↔ Ennemis
        hits = pygame.sprite.spritecollide(
            self.player, 
            self.enemies, 
            False
        )
        if hits:
            self.player.take_damage(1)
```

### `entities/player.py`
```python
# ✅ RESPONSABILITÉS
- Mouvement (gauche/droite)
- Saut + gravité
- Attaque (créer projectile)
- Gestion HP/animations
- Détection sol

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, character=1):
        super().__init__()
        self.character = character
        self.load_sprites()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (x, y)
        
        # Stats
        self.hp = 3
        self.max_hp = 3
        self.speed = PLAYER_SPEED
        self.jump_force = JUMP_FORCE
        
        # Physique
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        
        # État
        self.facing_right = True
        self.can_attack = True
        self.attack_cooldown = 0
    
    def update(self, dt):
        self.handle_input()
        self.apply_gravity(dt)
        self.move(dt)
        self.check_ground()
        self.update_cooldowns(dt)
        self.animate()
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        self.velocity_x = 0
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing_right = True
        
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -self.jump_force
            self.on_ground = False
    
    def attack(self):
        if self.can_attack:
            # Créer projectile (géré par gameplay.py)
            self.can_attack = False
            self.attack_cooldown = 0.35  # secondes
            return True
        return False
```

### `systems/rhythm.py`
```python
# ✅ RESPONSABILITÉS
- Calculer position métronome (BPM)
- Détecter si dans zone parfaite
- Fournir multiplicateur dégâts

class RhythmSystem:
    def __init__(self, bpm=120):
        self.bpm = bpm
        self.beat_duration = 60 / bpm  # Secondes par beat
        self.time = 0
        self.perfect_window = 0.1  # ±0.1s autour du beat
        
        # Position curseur sur barre (0 à 1)
        self.cursor_position = 0
    
    def update(self, dt):
        self.time += dt
        
        # Position dans le beat actuel (0 à 1)
        beat_progress = (self.time % self.beat_duration) / self.beat_duration
        self.cursor_position = beat_progress
    
    def is_perfect_timing(self):
        """Retourne True si proche d'un beat"""
        # Le beat est à 0 (ou 1)
        return self.cursor_position < self.perfect_window or \
               self.cursor_position > (1 - self.perfect_window)
    
    def get_damage_multiplier(self):
        """1.5x si timing parfait, sinon 1.0x"""
        return 1.5 if self.is_perfect_timing() else 1.0
    
    def draw(self, screen):
        # Barre en haut de l'écran
        bar_rect = pygame.Rect(WIDTH//4, 20, WIDTH//2, 30)
        pygame.draw.rect(screen, (50, 50, 50), bar_rect)
        
        # Zone parfaite (centre)
        perfect_zone_width = bar_rect.width * (2 * self.perfect_window)
        perfect_rect = pygame.Rect(
            bar_rect.centerx - perfect_zone_width // 2,
            bar_rect.y,
            perfect_zone_width,
            bar_rect.height
        )
        pygame.draw.rect(screen, (0, 255, 0), perfect_rect)
        
        # Curseur
        cursor_x = bar_rect.x + (bar_rect.width * self.cursor_position)
        pygame.draw.circle(screen, (255, 255, 0), (int(cursor_x), bar_rect.centery), 5)
```

---

## Patterns de code recommandés

### Pattern 1 : Sprite de base
```python
class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def update(self, dt):
        pass  # Logique spécifique
```

### Pattern 2 : Collision avec callback
```python
def check_projectile_hits(projectiles, enemies):
    hits = pygame.sprite.groupcollide(projectiles, enemies, True, False)
    for projectile, enemies_hit in hits.items():
        for enemy in enemies_hit:
            enemy.take_damage(projectile.damage)
            projectile.on_hit()  # Son, effet particules, etc.
```

### Pattern 3 : State machine simple (animations)
```python
class Player:
    def update(self, dt):
        # Déterminer état
        if not self.on_ground:
            state = "jump"
        elif abs(self.velocity_x) > 0:
            state = "run"
        else:
            state = "idle"
        
        # Charger sprite correspondant
        self.image = self.sprites[state][self.frame_index]
```

### Pattern 4 : Timer avec delta time
```python
class Enemy:
    def __init__(self):
        self.patrol_timer = 0
        self.patrol_duration = 2.0  # 2 secondes
        self.direction = 1
    
    def update(self, dt):
        self.patrol_timer += dt
        if self.patrol_timer >= self.patrol_duration:
            self.direction *= -1  # Inverser
            self.patrol_timer = 0
        
        self.rect.x += self.speed * self.direction * dt
```

---

## Points critiques à ne pas oublier

### ⚠️ Delta Time (dt) obligatoire
```python
# ❌ MAUVAIS (dépend des FPS)
player.rect.x += 5

# ✅ BON (indépendant des FPS)
player.rect.x += PLAYER_SPEED * dt  # dt en secondes
```

### ⚠️ Gravité et saut
```python
# Dans update(dt)
if not on_ground:
    velocity_y += GRAVITY * dt * 60  # Ajuster échelle
    rect.y += velocity_y

# Détection sol
if rect.bottom >= GROUND_Y:
    rect.bottom = GROUND_Y
    velocity_y = 0
    on_ground = True
```

### ⚠️ Clamp position dans écran
```python
# Empêcher joueur de sortir
player.rect.left = max(player.rect.left, 0)
player.rect.right = min(player.rect.right, WIDTH)
```

### ⚠️ Assets manquants
```python
# Fallback si image introuvable
try:
    image = pygame.image.load(path).convert_alpha()
except pygame.error:
    # Créer rectangle coloré temporaire
    image = pygame.Surface((32, 32))
    image.fill((255, 0, 255))  # Rose = placeholder
```

---

## Ordre de développement recommandé

1. **main.py + settings.py** (structure de base)
2. **scenes/base.py + menu.py** (navigation simple)
3. **Player avec mouvement + saut** (gameplay.py minimal)
4. **1 plateforme + gravité fonctionnelle**
5. **1 ennemi Hater qui patrouille**
6. **Projectile + collision ennemi**
7. **Système HP + game over**
8. **Barre Guitar Hero (rhythm.py)**
9. **3 niveaux + boss**
10. **UI/HUD complet**
11. **Sons**
12. **Polish + assets finaux**

---

**Ce fichier doit être relu AVANT de toucher au code. Il décrit comment tout s'interconnecte.**