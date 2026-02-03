"""
Rockstar Bros - Configuration et constantes globales
Toutes les constantes du jeu sont centralisees ici
"""

import pygame
from pathlib import Path

# =============================================================================
# ECRAN
# =============================================================================
WIDTH = 1280
HEIGHT = 720
FPS = 60
TITLE = "Rockstar Bros"

# =============================================================================
# COULEURS
# =============================================================================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (150, 0, 255)
ORANGE = (255, 150, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BG_COLOR = (25, 25, 35)

# Couleurs UI
UI_BG = (30, 30, 40, 200)
UI_BORDER = (100, 100, 120)
HEALTH_COLOR = (255, 50, 50)
COMBO_COLOR = (255, 200, 0)

# =============================================================================
# CHEMINS ASSETS
# =============================================================================
BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "images"
SND_DIR = ASSETS_DIR / "sounds"

# Sous-dossiers images
IMG_PLAYER_DIR = IMG_DIR / "player"
IMG_ENEMIES_DIR = IMG_DIR / "enemies"
IMG_UI_DIR = IMG_DIR / "ui"
IMG_BG_DIR = IMG_DIR / "backgrounds"
IMG_FX_DIR = IMG_DIR / "fx"
IMG_PLATFORMS_DIR = IMG_DIR / "platforms"

# Fonts
FONTS_DIR = ASSETS_DIR / "fonts"
FONT_METAL_MANIA = FONTS_DIR / "MetalMania-Regular.ttf"
FONT_ROAD_RAGE = FONTS_DIR / "Road_Rage.otf"

# =============================================================================
# JOUEUR
# =============================================================================
PLAYER_SPEED = 6
PLAYER_JUMP_FORCE = 18
PLAYER_MAX_HEALTH = 3
PLAYER_INVINCIBILITY_TIME = 1500  # ms apres degats
PLAYER_WIDTH = 64
PLAYER_HEIGHT = 96

# =============================================================================
# PHYSIQUE
# =============================================================================
GRAVITY = 0.8
MAX_FALL_SPEED = 20
GROUND_Y = HEIGHT - 100  # Sol par defaut

# =============================================================================
# ATTAQUES
# =============================================================================
PROJECTILE_SPEED = 12
PROJECTILE_COOLDOWN = 350  # ms entre chaque tir
PROJECTILE_WIDTH = 40
PROJECTILE_HEIGHT = 20
PROJECTILE_DAMAGE = 1

# Attaque ultime (sequence rythmique)
ULTIMATE_BASE_DAMAGE = 3  # Degats de base de l'ultime
ULTIMATE_DAMAGE_PER_PERFECT = 3  # Bonus par PERFECT
ULTIMATE_DAMAGE_PER_GOOD = 2  # Bonus par GOOD
ULTIMATE_DAMAGE_PER_OK = 1  # Bonus par OK
ULTIMATE_CHARGE_MAX = 100
ULTIMATE_CHARGE_PER_HIT = 15  # Charge gagnee en touchant un ennemi
ULTIMATE_CHARGE_PER_PICKUP = 25  # Charge gagnee avec mediator
ULTIMATE_NOTE_COUNT = 8  # Nombre de notes dans la sequence

# =============================================================================
# SYSTEME RYTHME (Guitar Hero) - UNIQUEMENT POUR L'ULTIME
# =============================================================================
# Vitesse des notes (plus c'est bas, plus c'est lent)
NOTE_FALL_SPEED = 4  # pixels par frame
NOTE_SPAWN_INTERVAL = 800  # ms entre chaque note (plus c'est haut, plus c'est lent)

# Zones de timing (distance en pixels depuis la ligne de frappe)
HIT_ZONE_PERFECT = 15  # pixels
HIT_ZONE_GOOD = 35  # pixels
HIT_ZONE_OK = 55  # pixels

# Dimensions des notes et pistes
NOTE_SIZE = 50  # taille des notes (cercles)
LANE_WIDTH = 80  # largeur de chaque piste
LANE_COUNT = 3  # 3 pistes (F, G, H)
TRACK_HEIGHT = 400  # hauteur de la zone de jeu
TRACK_WIDTH = LANE_WIDTH * LANE_COUNT  # largeur totale
TRACK_X = (WIDTH - TRACK_WIDTH) // 2  # position X centree
TRACK_Y = 150  # position Y du haut de la piste
HIT_LINE_Y = TRACK_Y + TRACK_HEIGHT - 60  # ligne de frappe

# Couleurs des pistes (F=rouge, G=jaune, H=bleu)
LANE_COLORS = [(255, 80, 80), (255, 220, 80), (80, 180, 255)]
LANE_KEYS = [pygame.K_f, pygame.K_g, pygame.K_h]  # Touches F, G, H

# =============================================================================
# ENNEMIS
# =============================================================================
# Hater (ennemi de base)
HATER_SPEED = 2
HATER_HEALTH = 2
HATER_DAMAGE = 1
HATER_WIDTH = 48
HATER_HEIGHT = 64
HATER_DETECTION_RANGE = 300
HATER_SCORE = 100

# Rockstar rival
RIVAL_SPEED = 3
RIVAL_HEALTH = 3
RIVAL_DAMAGE = 1
RIVAL_WIDTH = 56
RIVAL_HEIGHT = 80
RIVAL_DETECTION_RANGE = 400
RIVAL_SCORE = 200

# Boss
BOSS_HEALTH = 20
BOSS_DAMAGE = 2
BOSS_WIDTH = 128
BOSS_HEIGHT = 160
BOSS_SPEED = 2
BOSS_PROJECTILE_SPEED = 8
BOSS_ATTACK_COOLDOWN = 2000  # ms
BOSS_SHOCKWAVE_DAMAGE = 2
BOSS_SCORE = 1000

# Phases du boss (% de vie restante)
BOSS_PHASE_2_THRESHOLD = 0.6  # 60% vie
BOSS_PHASE_3_THRESHOLD = 0.3  # 30% vie

# =============================================================================
# COLLECTIBLES
# =============================================================================
PICKUP_NOTE_SCORE = 50
PICKUP_MEDIATOR_ULTIMATE = 25  # Charge ultime
PICKUP_AMPLI_DURATION = 5000  # ms de boost
PICKUP_WIDTH = 32
PICKUP_HEIGHT = 32

# =============================================================================
# NIVEAUX
# =============================================================================
LEVEL_NAMES = ["Coulisses", "Scene", "Boss Arena"]

# Checkpoints (positions X pour chaque niveau)
CHECKPOINT_POSITIONS = {
    1: [600, 1500],
    2: [800, 2000],
    3: []  # Pas de checkpoint dans l'arene boss
}

# Longueur des niveaux (en pixels)
LEVEL_LENGTHS = {
    1: 3000,
    2: 4000,
    3: 1280  # Arene fixe
}

# =============================================================================
# CAMERA
# =============================================================================
CAMERA_FOLLOW_SPEED = 0.1
CAMERA_DEAD_ZONE_X = 200  # Zone ou la camera ne bouge pas

# =============================================================================
# UI / HUD
# =============================================================================
HUD_MARGIN = 20
HUD_HEALTH_SIZE = 40
HUD_FONT_SIZE = 24
HUD_TITLE_FONT_SIZE = 48

# =============================================================================
# SONS (noms des fichiers)
# =============================================================================
SND_MUSIC_MENU = "menu_music.wav"
SND_MUSIC_LEVEL1 = "level1_music.wav"
SND_MUSIC_LEVEL2 = "level2_music.wav"
SND_MUSIC_BOSS = "boss_music.wav"
SND_ATTACK = "attack.wav"
SND_HIT = "hit.wav"
SND_JUMP = "jump.wav"
SND_PICKUP = "pickup.wav"
SND_HURT = "hurt.wav"
SND_DEATH = "death.wav"
SND_VICTORY = "victory.wav"
SND_BEAT = "beat.wav"

# =============================================================================
# IMAGES (noms des fichiers)
# =============================================================================
# Joueur 1
IMG_PLAYER1_IDLE = "player1_idle.png"
IMG_PLAYER1_RUN1 = "player1_run1.png"
IMG_PLAYER1_RUN2 = "player1_run2.png"
IMG_PLAYER1_JUMP = "player1_jump.png"
IMG_PLAYER1_ATTACK = "player1_attack.png"
IMG_PLAYER1_ULTIMATE = "player1_ultimate.png"
IMG_PLAYER1_CROUCH = "player1_crouch.png"

# Joueur 2
IMG_PLAYER2_IDLE = "player2_idle.png"
IMG_PLAYER2_RUN1 = "player2_run1.png"
IMG_PLAYER2_RUN2 = "player2_run2.png"
IMG_PLAYER2_JUMP = "player2_jump.png"
IMG_PLAYER2_ATTACK = "player2_attack.png"
IMG_PLAYER2_ULTIMATE = "player2_ultimate.png"
IMG_PLAYER2_CROUCH = "player2_crouch.png"

# Ennemis - Hater
IMG_HATER_IDLE = "hater_idle.png"
IMG_HATER_RUN = "hater_run.png"
IMG_HATER_RUN1 = "hater_run1.png"
IMG_HATER_ATTACK = "hater_attack.png"
IMG_HATER_DEAD = "hater_dead.png"
IMG_HATER_HIT = "hater_hit.png"

# Ennemis - Rival
IMG_RIVAL_IDLE = "rival_idle.png"
IMG_RIVAL_RUN1 = "rival_run1.png"
IMG_RIVAL_RUN2 = "rival_run2.png"
IMG_RIVAL_ATTACK = "rival_attack.png"
IMG_RIVAL_DEAD = "rival_dead.png"
IMG_RIVAL_HIT = "rival_hit.png"

# Ennemis - Boss
IMG_BOSS_IDLE = "boss_idle.png"
IMG_BOSS_RUN1 = "boss_run1.png"
IMG_BOSS_RUN2 = "boss_run2.png"
IMG_BOSS_JUMP = "boss_jump.png"
IMG_BOSS_ATTACK = "boss_attack.png"
IMG_BOSS_HIT = "boss_hit.png"

# Projectiles
IMG_PROJECTILE = "projectile.png"
IMG_BOSS_PROJECTILE = "boss_projectile.png"
IMG_SHOCKWAVE = "shockwave.png"

# UI
IMG_HEART_FULL = "heart_full.png"
IMG_HEART_EMPTY = "heart_empty.png"
IMG_RHYTHM_BAR = "rhythm_bar.png"
IMG_RHYTHM_CURSOR = "rhythm_cursor.png"
IMG_ULTIMATE_BAR = "ultimate_bar.png"

# Collectibles
IMG_NOTE = "note.png"
IMG_MEDIATOR = "mediator.png"
IMG_AMPLI = "ampli.png"

# Backgrounds
IMG_BG_MENU = "bg_menu.png"
IMG_BG_LEVEL1 = "bg_level1.png"
IMG_BG_LEVEL2 = "bg_level2.png"
IMG_BG_BOSS = "bg_boss.png"

# Ecrans speciaux (directement dans images/)
IMG_HOME = "home.png"
IMG_GAMEOVER = "gameover.png"
IMG_PAUSE = "pause.png"
IMG_WIN = "win.png"
IMG_LOGO = "logo.png"

# Plateformes
IMG_PLATFORM = "platform.png"
IMG_PLATFORM_SMALL = "platform_small.png"
IMG_GROUND = "ground.png"

# =============================================================================
# ETATS DU JEU
# =============================================================================
STATE_MENU = "menu"
STATE_CHARACTER_SELECT = "character_select"
STATE_GAMEPLAY = "gameplay"
STATE_PAUSE = "pause"
STATE_GAME_OVER = "game_over"
STATE_VICTORY = "victory"

# =============================================================================
# CONTROLES
# =============================================================================
CONTROLS = {
    "left": [pygame.K_LEFT, pygame.K_a],
    "right": [pygame.K_RIGHT, pygame.K_d],
    "jump": [pygame.K_SPACE, pygame.K_w, pygame.K_UP],
    "crouch": [pygame.K_DOWN, pygame.K_s],
    "attack": [pygame.K_j],
    "ultimate": [pygame.K_k],
    "pause": [pygame.K_ESCAPE],
    "confirm": [pygame.K_RETURN, pygame.K_SPACE],
    "debug_hitbox": [pygame.K_F1],
    "debug_skip": [pygame.K_F2],
    "debug_invincible": [pygame.K_F3],
}
