"""
Rockstar Bros - Scene de gameplay
Coeur du jeu: gestion du niveau, collisions, systeme rythme
"""

import pygame
import random
import math
from scenes.base import Scene
from entities import Player, Projectile, Enemy, Boss, Platform, Pickup
from level_loader import get_loader
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, RED, GREEN, BLUE, PURPLE, ORANGE, GRAY, DARK_GRAY,
    STATE_PAUSE, STATE_GAME_OVER, STATE_VICTORY, STATE_LEVEL_SELECT, STATE_MENU, CONTROLS,
    GROUND_Y,
    PLAYER_MAX_HEALTH, PLAYER_WIDTH, PLAYER_HEIGHT,
    PROJECTILE_SPEED,
    ULTIMATE_CHARGE_MAX, ULTIMATE_CHARGE_PER_HIT,
    ULTIMATE_BASE_DAMAGE, ULTIMATE_DAMAGE_PER_PERFECT, ULTIMATE_DAMAGE_PER_GOOD,
    ULTIMATE_DAMAGE_PER_OK, ULTIMATE_CHARGE_PER_PICKUP, ULTIMATE_NOTE_COUNT,
    NOTE_FALL_SPEED, NOTE_SPAWN_INTERVAL,
    HIT_ZONE_PERFECT, HIT_ZONE_GOOD, HIT_ZONE_OK,
    NOTE_SIZE, LANE_WIDTH, LANE_COUNT, TRACK_HEIGHT, TRACK_WIDTH,
    TRACK_X, TRACK_Y, HIT_LINE_Y, LANE_COLORS, LANE_KEYS,
    # Ennemis
    HATER_SPEED, HATER_HEALTH, HATER_DAMAGE, HATER_WIDTH, HATER_HEIGHT,
    HATER_DETECTION_RANGE, HATER_SCORE,
    RIVAL_SPEED, RIVAL_HEALTH, RIVAL_DAMAGE, RIVAL_WIDTH, RIVAL_HEIGHT,
    RIVAL_DETECTION_RANGE, RIVAL_SCORE,
    BOSS_HEALTH, BOSS_DAMAGE, BOSS_WIDTH, BOSS_HEIGHT, BOSS_SPEED,
    BOSS_PROJECTILE_SPEED, BOSS_ATTACK_COOLDOWN, BOSS_SHOCKWAVE_DAMAGE, BOSS_SCORE,
    BOSS_PHASE_2_THRESHOLD, BOSS_PHASE_3_THRESHOLD,
    # Collectibles
    PICKUP_NOTE_SCORE, PICKUP_MEDIATOR_ULTIMATE, PICKUP_AMPLI_DURATION,
    PICKUP_WIDTH, PICKUP_HEIGHT,
    # Niveaux
    LEVEL_NAMES, LEVEL_LENGTHS,
    # Images
    IMG_DIR, IMG_PLAYER_DIR, IMG_ENEMIES_DIR, IMG_BG_DIR, IMG_UI_DIR, IMG_FX_DIR,
    IMG_PLAYER1_IDLE, IMG_PLAYER1_RUN1, IMG_PLAYER1_RUN2, IMG_PLAYER1_JUMP, IMG_PLAYER1_ATTACK,
    IMG_PLAYER2_IDLE, IMG_PLAYER2_RUN1, IMG_PLAYER2_RUN2, IMG_PLAYER2_JUMP, IMG_PLAYER2_ATTACK,
    IMG_PLAYER1_ULTIMATE, IMG_PLAYER2_ULTIMATE,
    IMG_HATER_IDLE, IMG_RIVAL_IDLE, IMG_BOSS_IDLE, IMG_BOSS_ATTACK,
    IMG_PROJECTILE, IMG_BOSS_PROJECTILE,
    IMG_BG_LEVEL1, IMG_BG_LEVEL2, IMG_BG_BOSS,
    IMG_HEART_FULL, IMG_HEART_EMPTY, IMG_BOSS_INTRO,
    FONT_METAL_MANIA, FONT_ROAD_RAGE,
    HUD_MARGIN, HUD_HEALTH_SIZE,
    # Sons
    SND_DIR, SND_MUSIC_LEVEL1, SND_MUSIC_LEVEL2, SND_MUSIC_BOSS, SND_MUSIC_BOSS_INTRO, SND_VICTORY, SND_DEATH, SND_JUMP, SND_PLAYER_SHOOT, SND_ENEMY_DEATH, SND_BONUS_PICKUP,
    # Plateformes
    IMG_PLATFORMS_DIR, IMG_PLATFORM, IMG_PLATFORM_SMALL, IMG_GROUND,
)


# =============================================================================
# CLASSES ENTITES
# =============================================================================

class Player(pygame.sprite.Sprite):
    """Classe du joueur"""

    def __init__(self, character_id, x, y, scene=None):
        super().__init__()
        self.character_id = character_id
        self.scene = scene  # Reference a la scene pour jouer les sons

        # Images
        self.images = {}
        self._load_images()

        # Sprite de base
        self.image = self._get_placeholder((PLAYER_WIDTH, PLAYER_HEIGHT), PURPLE)
        self.rect = self.image.get_rect(midbottom=(x, y))

        # Physique
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True

        # Combat
        self.health = PLAYER_MAX_HEALTH
        self.invincible = False
        self.invincible_timer = 0
        self.attack_cooldown = 0
        self.ultimate_charge = 0

        # Animation
        self.anim_frame = 0
        self.anim_timer = 0
        self.state = "idle"  # idle, run, jump, attack, ultimate
        self.attack_anim_timer = 0  # Timer pour garder l'animation d'attaque

        # Debug
        self.debug_invincible = False

    def _load_images(self):
        """Charge les images du joueur"""
        if self.character_id == 1:
            img_files = {
                "idle": IMG_PLAYER1_IDLE,
                "run1": IMG_PLAYER1_RUN1,
                "run2": IMG_PLAYER1_RUN2,
                "jump": IMG_PLAYER1_JUMP,
                "attack": IMG_PLAYER1_ATTACK,
                "ultimate": IMG_PLAYER1_ULTIMATE,
            }
        else:
            img_files = {
                "idle": IMG_PLAYER2_IDLE,
                "run1": IMG_PLAYER2_RUN1,
                "run2": IMG_PLAYER2_RUN2,
                "jump": IMG_PLAYER2_JUMP,
                "attack": IMG_PLAYER2_ATTACK,
                "ultimate": IMG_PLAYER2_ULTIMATE,
            }

        for key, filename in img_files.items():
            try:
                path = IMG_PLAYER_DIR / filename
                img = pygame.image.load(str(path)).convert_alpha()
                self.images[key] = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
            except (pygame.error, FileNotFoundError):
                self.images[key] = None

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        return surf

    def _get_current_image(self):
        """Retourne l'image correspondant a l'etat actuel"""
        if self.state == "ultimate":
            img = self.images.get("ultimate")
            if img is None:
                # Fallback: placeholder special pour l'ultime
                color = (255, 200, 0) if self.character_id == 1 else (255, 150, 50)
                img = self._get_placeholder((PLAYER_WIDTH, PLAYER_HEIGHT), color)
        elif self.state == "jump":
            img = self.images.get("jump")
        elif self.state == "run":
            frame_key = "run1" if self.anim_frame == 0 else "run2"
            img = self.images.get(frame_key)
        elif self.state == "attack":
            img = self.images.get("attack")
        else:
            img = self.images.get("idle")

        if img is None:
            color = PURPLE if self.character_id == 1 else ORANGE
            img = self._get_placeholder((PLAYER_WIDTH, PLAYER_HEIGHT), color)

        # Flip si regarde a gauche
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        return img

    def handle_input(self, keys):
        """Gere les inputs du joueur"""
        self.velocity_x = 0

        # Deplacement horizontal
        move_left = any(keys[k] for k in CONTROLS["left"])
        move_right = any(keys[k] for k in CONTROLS["right"])

        if move_left:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
        if move_right:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True

        # Saut
        jump = any(keys[k] for k in CONTROLS["jump"])
        if jump and self.on_ground:
            self.velocity_y = -PLAYER_JUMP_FORCE
            self.on_ground = False
            # Jouer le son de saut
            if self.scene:
                self.scene._play_sound(SND_JUMP)

    def update(self, dt, platforms):
        """Met a jour le joueur"""
        dt_ms = dt * 1000

        # Gravite
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED

        # Mouvement
        self.rect.x += self.velocity_x
        self._check_horizontal_collisions(platforms)

        self.rect.y += self.velocity_y
        self._check_vertical_collisions(platforms)

        # Cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt_ms

        if self.invincible:
            self.invincible_timer -= dt_ms
            if self.invincible_timer <= 0:
                self.invincible = False

        # Animation
        self._update_animation(dt_ms)

        # Mise a jour de l'image
        self.image = self._get_current_image()

    def _check_horizontal_collisions(self, platforms):
        """Verifie les collisions horizontales"""
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right

    def _check_vertical_collisions(self, platforms):
        """Verifie les collisions verticales"""
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
        # Plus de sol invisible - le joueur peut tomber dans le vide!

    def _update_animation(self, dt_ms):
        """Met a jour l'animation"""
        # Gerer le timer d'animation d'attaque
        if self.attack_anim_timer > 0:
            self.attack_anim_timer -= dt_ms
            if self.attack_anim_timer > 0:
                self.state = "attack"
                return  # Garder l'etat attack pendant le timer

        # Determiner l'etat (si pas en attaque)
        if self.state == "ultimate":
            return  # Garder l'etat ultimate pendant la sequence
        elif not self.on_ground:
            self.state = "jump"
        elif self.velocity_x != 0:
            self.state = "run"
        else:
            self.state = "idle"

        # Animation de course
        if self.state == "run":
            self.anim_timer += dt_ms
            if self.anim_timer >= 150:  # Change frame toutes les 150ms
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 2

    def can_attack(self):
        """Verifie si le joueur peut attaquer"""
        return self.attack_cooldown <= 0

    def attack(self):
        """Lance une attaque"""
        self.attack_cooldown = PROJECTILE_COOLDOWN
        self.state = "attack"
        self.attack_anim_timer = 300  # Animation d'attaque pendant 300ms

    def take_damage(self, amount=1):
        """Le joueur prend des degats"""
        if self.invincible or self.debug_invincible:
            return False

        self.health -= amount
        self.invincible = True
        self.invincible_timer = PLAYER_INVINCIBILITY_TIME

        return True

    def heal(self, amount=1):
        """Soigne le joueur"""
        self.health = min(self.health + amount, PLAYER_MAX_HEALTH)

    def add_ultimate_charge(self, amount):
        """Ajoute de la charge ultime"""
        self.ultimate_charge = min(self.ultimate_charge + amount, ULTIMATE_CHARGE_MAX)

    def can_use_ultimate(self):
        """Verifie si l'ultime est disponible"""
        return self.ultimate_charge >= ULTIMATE_CHARGE_MAX

    def use_ultimate(self):
        """Utilise l'attaque ultime"""
        self.ultimate_charge = 0


class Projectile(pygame.sprite.Sprite):
    """Projectile du joueur (onde sonore)"""

    def __init__(self, x, y, direction, damage_multiplier=1.0):
        super().__init__()
        self.image = self._get_placeholder((PROJECTILE_WIDTH, PROJECTILE_HEIGHT), YELLOW)
        self._load_image()
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction  # 1 = droite, -1 = gauche
        self.speed = PROJECTILE_SPEED
        self.damage = int(PROJECTILE_DAMAGE * damage_multiplier)

    def _load_image(self):
        """Charge l'image du projectile"""
        try:
            path = IMG_FX_DIR / IMG_PROJECTILE
            img = pygame.image.load(str(path)).convert_alpha()
            self.image = pygame.transform.scale(img, (PROJECTILE_WIDTH, PROJECTILE_HEIGHT))
        except (pygame.error, FileNotFoundError):
            pass

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.ellipse(surf, color, (0, 0, size[0], size[1]))
        return surf

    def update(self, dt):
        """Met a jour le projectile"""
        self.rect.x += self.speed * self.direction

        # Supprime si hors ecran (avec marge pour camera)
        if self.rect.right < -100 or self.rect.left > WIDTH + 2000:
            self.kill()


class BossProjectile(pygame.sprite.Sprite):
    """Projectile du boss"""

    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = self._get_placeholder((30, 30), RED)
        self.rect = self.image.get_rect(center=(x, y))

        # Calcul direction vers la cible
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            self.vel_x = (dx / dist) * BOSS_PROJECTILE_SPEED
            self.vel_y = (dy / dist) * BOSS_PROJECTILE_SPEED
        else:
            self.vel_x = -BOSS_PROJECTILE_SPEED
            self.vel_y = 0

        self.damage = BOSS_DAMAGE

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (size[0]//2, size[1]//2), size[0]//2)
        return surf

    def update(self, dt):
        """Met a jour le projectile"""
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Supprime si hors ecran
        if (self.rect.right < -50 or self.rect.left > WIDTH + 50 or
            self.rect.bottom < -50 or self.rect.top > HEIGHT + 50):
            self.kill()


class Enemy(pygame.sprite.Sprite):
    """Classe de base pour les ennemis"""

    def __init__(self, x, y, enemy_type="hater"):
        super().__init__()
        self.enemy_type = enemy_type

        # Config selon type
        if enemy_type == "hater":
            self.width = HATER_WIDTH
            self.height = HATER_HEIGHT
            self.speed = HATER_SPEED
            self.max_health = HATER_HEALTH
            self.damage = HATER_DAMAGE
            self.detection_range = HATER_DETECTION_RANGE
            self.score_value = HATER_SCORE
            self.color = RED
            self.img_file = IMG_HATER_IDLE
        else:  # rival
            self.width = RIVAL_WIDTH
            self.height = RIVAL_HEIGHT
            self.speed = RIVAL_SPEED
            self.max_health = RIVAL_HEALTH
            self.damage = RIVAL_DAMAGE
            self.detection_range = RIVAL_DETECTION_RANGE
            self.score_value = RIVAL_SCORE
            self.color = ORANGE
            self.img_file = IMG_RIVAL_IDLE

        self.health = self.max_health
        self.image = self._get_placeholder((self.width, self.height), self.color)
        self._load_image()
        self.rect = self.image.get_rect(midbottom=(x, y))

        # Comportement
        self.facing_right = False
        self.patrol_direction = -1
        self.patrol_distance = 100
        self.start_x = x
        self.hit_flash = 0

        # Physique (pour tomber dans les trous)
        self.velocity_y = 0
        self.on_ground = False

    def _load_image(self):
        """Charge l'image de l'ennemi"""
        try:
            path = IMG_ENEMIES_DIR / self.img_file
            img = pygame.image.load(str(path)).convert_alpha()
            self.image = pygame.transform.scale(img, (self.width, self.height))
        except (pygame.error, FileNotFoundError):
            pass

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        return surf

    def update(self, dt, player_rect, platforms=None):
        """Met a jour l'ennemi"""
        dt_ms = dt * 1000

        # Flash de degats
        if self.hit_flash > 0:
            self.hit_flash -= dt_ms

        # Appliquer la gravite
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED

        # Mouvement vertical
        self.rect.y += self.velocity_y
        self.on_ground = False

        # Collision avec le sol uniquement (pas les plateformes en hauteur)
        if platforms:
            for platform in platforms:
                # Les ennemis ne peuvent marcher que sur le sol, pas sur les plateformes
                if platform.is_ground and self.rect.colliderect(platform.rect):
                    if self.velocity_y > 0:  # Tombe
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.on_ground = True

        # Mouvement horizontal seulement si au sol
        if self.on_ground:
            # Distance au joueur
            dist_to_player = abs(self.rect.centerx - player_rect.centerx)

            if dist_to_player < self.detection_range:
                # Poursuit le joueur
                if player_rect.centerx < self.rect.centerx:
                    self.rect.x -= self.speed
                    self.facing_right = False
                else:
                    self.rect.x += self.speed
                    self.facing_right = True
            else:
                # Patrouille
                self.rect.x += self.speed * self.patrol_direction
                if abs(self.rect.x - self.start_x) > self.patrol_distance:
                    self.patrol_direction *= -1
                    self.facing_right = self.patrol_direction > 0

    def take_damage(self, amount):
        """L'ennemi prend des degats"""
        self.health -= amount
        self.hit_flash = 100
        return self.health <= 0

    def draw(self, screen, camera_x):
        """Dessine l'ennemi avec effets"""
        img = self.image
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        # Flash blanc si touche
        if self.hit_flash > 0:
            flash_surf = img.copy()
            flash_surf.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_ADD)
            img = flash_surf

        draw_rect = self.rect.move(-camera_x, 0)
        screen.blit(img, draw_rect)


class Boss(pygame.sprite.Sprite):
    """Boss final - Rockstar concurrente"""

    def __init__(self, x, y):
        super().__init__()
        self.image = self._get_placeholder((BOSS_WIDTH, BOSS_HEIGHT), (200, 0, 100))
        self._load_image()
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.max_health = BOSS_HEALTH
        self.health = self.max_health
        self.damage = BOSS_DAMAGE
        self.speed = BOSS_SPEED
        self.score_value = BOSS_SCORE

        # Comportement
        self.phase = 1
        self.facing_right = False
        self.attack_cooldown = BOSS_ATTACK_COOLDOWN
        self.attack_timer = self.attack_cooldown
        self.current_attack = None
        self.hit_flash = 0

        # Mouvement
        self.move_timer = 0
        self.move_direction = -1

    def _load_image(self):
        """Charge l'image du boss"""
        try:
            path = IMG_ENEMIES_DIR / IMG_BOSS_IDLE
            img = pygame.image.load(str(path)).convert_alpha()
            self.image = pygame.transform.scale(img, (BOSS_WIDTH, BOSS_HEIGHT))
        except (pygame.error, FileNotFoundError):
            pass

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        # Ajouter des details
        pygame.draw.rect(surf, (255, 255, 255), (20, 30, 30, 20))  # oeil gauche
        pygame.draw.rect(surf, (255, 255, 255), (BOSS_WIDTH - 50, 30, 30, 20))  # oeil droit
        return surf

    def update(self, dt, player_rect, projectiles_group):
        """Met a jour le boss"""
        dt_ms = dt * 1000

        # Flash de degats
        if self.hit_flash > 0:
            self.hit_flash -= dt_ms

        # Determiner la phase selon les PV
        health_ratio = self.health / self.max_health
        if health_ratio <= BOSS_PHASE_3_THRESHOLD:
            self.phase = 3
        elif health_ratio <= BOSS_PHASE_2_THRESHOLD:
            self.phase = 2

        # Regarder vers le joueur
        self.facing_right = player_rect.centerx > self.rect.centerx

        # Mouvement
        self.move_timer += dt_ms
        if self.move_timer > 2000:
            self.move_timer = 0
            self.move_direction *= -1

        # Deplacement vers le joueur (lent)
        if abs(self.rect.centerx - player_rect.centerx) > 150:
            if player_rect.centerx < self.rect.centerx:
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed

        # Attaques
        self.attack_timer -= dt_ms
        if self.attack_timer <= 0:
            self._perform_attack(player_rect, projectiles_group)
            # Cooldown plus court en phase avancee
            cooldown_modifier = 1.0 - (self.phase - 1) * 0.2
            self.attack_timer = self.attack_cooldown * cooldown_modifier

    def _perform_attack(self, player_rect, projectiles_group):
        """Execute une attaque"""
        attack_type = random.choice(["projectile", "projectile", "shockwave"])

        if attack_type == "projectile":
            # Tire des projectiles
            num_projectiles = self.phase  # Plus de projectiles en phase avancee
            for i in range(num_projectiles):
                offset_y = (i - num_projectiles // 2) * 30
                proj = BossProjectile(
                    self.rect.centerx,
                    self.rect.centery + offset_y,
                    player_rect.centerx,
                    player_rect.centery
                )
                projectiles_group.add(proj)

    def take_damage(self, amount):
        """Le boss prend des degats"""
        self.health -= amount
        self.hit_flash = 100
        return self.health <= 0

    def draw(self, screen, camera_x):
        """Dessine le boss avec effets"""
        img = self.image
        if self.facing_right:
            img = pygame.transform.flip(img, True, False)

        # Flash blanc si touche
        if self.hit_flash > 0:
            flash_surf = img.copy()
            flash_surf.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_ADD)
            img = flash_surf

        draw_rect = self.rect.move(-camera_x, 0)
        screen.blit(img, draw_rect)

        # Barre de vie du boss
        bar_width = BOSS_WIDTH
        bar_height = 10
        bar_x = draw_rect.centerx - bar_width // 2
        bar_y = draw_rect.top - 20

        # Fond
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        # Vie
        health_width = int((self.health / self.max_health) * bar_width)
        health_color = RED if self.phase == 3 else ORANGE if self.phase == 2 else GREEN
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        # Bordure
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)


class Platform(pygame.sprite.Sprite):
    """Plateforme / sol"""

    def __init__(self, x, y, width, height, is_ground=False):
        super().__init__()
        self.is_ground = is_ground
        self.width = width
        self.height = height

        # Creer le placeholder par defaut
        color = (80, 60, 40) if is_ground else (100, 80, 60)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        pygame.draw.rect(self.image, (60, 40, 20), (0, 0, width, height), 3)

        # Charger l'image si disponible
        self._load_image()

        self.rect = self.image.get_rect(topleft=(x, y))

    def _load_image(self):
        """Charge l'image de la plateforme"""
        try:
            if self.is_ground:
                img_file = IMG_GROUND
            elif self.width <= 120:
                img_file = IMG_PLATFORM_SMALL
            else:
                img_file = IMG_PLATFORM

            path = IMG_PLATFORMS_DIR / img_file
            img = pygame.image.load(str(path)).convert_alpha()
            self.image = pygame.transform.scale(img, (self.width, self.height))
        except (pygame.error, FileNotFoundError):
            pass  # Garder le placeholder


class Pickup(pygame.sprite.Sprite):
    """Collectible (note, mediator, ampli)"""

    def __init__(self, x, y, pickup_type="note"):
        super().__init__()
        self.pickup_type = pickup_type

        # Couleur selon type
        if pickup_type == "note":
            color = YELLOW
        elif pickup_type == "mediator":
            color = PURPLE
        else:  # ampli
            color = GREEN

        self.image = self._get_placeholder((PICKUP_WIDTH, PICKUP_HEIGHT), color)
        self._load_image()
        self.rect = self.image.get_rect(center=(x, y))

        # Animation flottante
        self.base_y = y
        self.float_offset = 0
        self.float_speed = 2

    def _load_image(self):
        """Charge l'image du pickup"""
        img_map = {
            "note": IMG_NOTE,
            "mediator": IMG_MEDIATOR,
            "ampli": IMG_AMPLI,
        }
        try:
            path = IMG_UI_DIR / img_map.get(self.pickup_type, IMG_NOTE)
            img = pygame.image.load(str(path)).convert_alpha()
            self.image = pygame.transform.scale(img, (PICKUP_WIDTH, PICKUP_HEIGHT))
        except (pygame.error, FileNotFoundError):
            pass

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        if self.pickup_type == "note":
            # Forme de note de musique
            pygame.draw.circle(surf, color, (size[0]//3, size[1]*2//3), size[0]//3)
            pygame.draw.line(surf, color, (size[0]//2, size[1]*2//3), (size[0]//2, 5), 3)
        else:
            pygame.draw.rect(surf, color, (0, 0, size[0], size[1]), border_radius=5)
        return surf

    def update(self, dt):
        """Met a jour le pickup (animation)"""
        self.float_offset += self.float_speed * dt
        self.rect.centery = self.base_y + math.sin(self.float_offset * 3) * 5


# =============================================================================
# SCENE GAMEPLAY
# =============================================================================

class GameplayScene(Scene):
    """Scene principale du jeu"""

    def __init__(self, game):
        super().__init__(game)

        # Groupes de sprites
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.boss_projectiles = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()

        # Entites principales
        self.player = None
        self.boss = None

        # Camera
        self.camera_x = 0

        # Niveau et stage
        self.current_level_id = 1
        self.current_stage_id = 1
        self.level_data = None
        self.stage_data = None
        self.level_width = 3000

        # Loader de niveaux
        self.loader = get_loader()

        # Systeme ULTIME (Guitar Hero - notes qui tombent)
        self.ultimate_active = False
        self.ultimate_notes = []  # Liste des notes actives: {"lane": 0-2, "y": position}
        self.ultimate_notes_spawned = 0
        self.ultimate_spawn_timer = 0
        self.ultimate_results = []  # Liste des resultats ("PERFECT", "GOOD", "OK", "MISS")
        self.ultimate_total_damage = 0
        self.ultimate_lane_pressed = [False, False, False]  # Etat des touches F, G, H

        # Feedback timing
        self.timing_feedback = ""
        self.timing_feedback_timer = 0

        # UI
        self.font = None
        self.font_big = None

        # Background
        self.background = None

        # Debug
        self.debug_hitboxes = False

        # Celebration (apres avoir battu le boss)
        self.celebration_active = False
        self.celebration_timer = 0

        # Animation de mort du boss
        self.boss_death_active = False
        self.boss_death_timer = 0
        self.boss_death_image = None
        self.boss_death_pos = (0, 0)
        self.boss_death_alpha = 255
        self.boss_death_zoom = 1.0
        self.target_camera_x = 0

        # Menu de victoire apres mort du boss
        self.victory_menu_active = False
        self.victory_menu_selected = 0
        self.victory_menu_options = ["Continuer", "Retour"]

        # Transition vers boss (image intro combat final)
        self.boss_intro_active = False
        self.boss_intro_timer = 0
        self.boss_intro_image = None
        self.boss_intro_duration = 6000  # 6 secondes en ms
        self.boss_intro_sound = None  # Stock du sound object si on utilise le fallback
        self.boss_intro_channel = None  # Channel pour la musique du boss
        self.level_music_sound = None  # Stock du sound object pour les musiques de niveau
        self.level_music_channel = None  # Channel pour la musique de niveau

        # Affichage des degats
        self.damage_numbers = []  # Liste: {"x", "y", "damage", "timer", "color"}

        # Animation timer pour effets visuels
        self.animation_time = 0

    def enter(self, **kwargs):
        """Initialisation a l'entree dans le niveau"""
        # Charger les polices - Road Rage pour le HUD, Metal Mania pour les gros textes
        try:
            self.font = pygame.font.Font(str(FONT_ROAD_RAGE), 26)
            self.font_big = pygame.font.Font(str(FONT_METAL_MANIA), 48)
        except (pygame.error, FileNotFoundError):
            self.font = pygame.font.Font(None, 26)
            self.font_big = pygame.font.Font(None, 48)

        # Recuperer les donnees du jeu et du niveau/stage
        self.current_level_id = kwargs.get('level_id', self.game.game_data.get("selected_level", 1))
        self.current_stage_id = kwargs.get('stage_id', self.game.game_data.get("current_stage", 1))
        character_id = self.game.game_data["selected_character"]

        # Charger les donnees du niveau et du stage depuis JSON
        self.level_data = self.loader.load_level(self.current_level_id)
        if self.level_data:
            self.stage_data = self.loader.get_stage(self.current_level_id, self.current_stage_id)
        else:
            print(f"Error: Could not load level {self.current_level_id}")
            self.game.change_scene(STATE_LEVEL_SELECT)
            return

        # Reset des groupes
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.player_projectiles.empty()
        self.boss_projectiles.empty()
        self.pickups.empty()

        # Obtenir la position de spawn du joueur depuis le stage
        spawn_x = 100
        spawn_y = GROUND_Y
        if self.stage_data:
            spawn_data = self.stage_data.get('player_spawn', {})
            spawn_x = spawn_data.get('x', 100)
            spawn_y = spawn_data.get('y', GROUND_Y)

        # Creer le joueur
        self.player = Player(character_id, spawn_x, spawn_y)
        # Si c'est le premier stage d'un niveau, remettre les vies au max
        if self.current_stage_id == 1:
            self.player.health = PLAYER_MAX_HEALTH
            self.game.game_data["lives"] = PLAYER_MAX_HEALTH
            self.player.ultimate_charge = 0
            self.game.game_data["ultimate_charge"] = 0
        else:
            self.player.health = self.game.game_data["lives"]
            self.player.ultimate_charge = self.game.game_data.get("ultimate_charge", 0)
        self.all_sprites.add(self.player)

        # Charger le stage depuis la config
        self._load_stage()

        # Reset camera
        self.camera_x = 0

        # Reset rythme
        self.beat_timer = 0
        self.combo = 0

        # Reset celebration
        self.celebration_active = False
        self.celebration_timer = 0

        # Reset boss death animation
        self.boss_death_active = False
        self.boss_death_timer = 0
        self.boss_death_alpha = 255
        self.boss_death_zoom = 1.0
        self.victory_menu_active = False
        self.victory_menu_selected = 0

        # Charger l'image de mort du boss
        try:
            boss_death_path = IMG_ENEMIES_DIR / "boss_death.png"
            self.boss_death_image = pygame.image.load(str(boss_death_path)).convert_alpha()
        except (pygame.error, FileNotFoundError):
            self.boss_death_image = None

        # Reset affichage des degats
        self.damage_numbers = []

        # Jouer la musique du niveau
        self._play_stage_music()

    def _play_level_music(self):
        """Charge et joue la musique du niveau actuel"""
        # Pour le niveau 3, la musique est deja lancee par l'intro du boss
        if self.current_level == 3:
            return
        
        # Arreter la musique precedente
        pygame.mixer.music.stop()
        if self.level_music_sound:
            self.level_music_sound.stop()
        if self.level_music_channel:
            self.level_music_channel.stop()
        self.level_music_sound = None
        self.level_music_channel = None
        
        music_files = {
            1: SND_MUSIC_LEVEL1,
            2: SND_MUSIC_LEVEL2,
        }
        try:
            music_file = music_files.get(self.current_level, SND_MUSIC_LEVEL1)
            music_path = SND_DIR / music_file
            music_path_str = str(music_path)
            print(f"Tentative de chargement musique niveau: {music_path_str}")
            pygame.mixer.music.load(music_path_str)
            pygame.mixer.music.set_volume(0.4)  # Volume un peu plus fort
            pygame.mixer.music.play(-1)  # -1 = boucle infinie
            print(f"Musique du niveau {self.current_level} lancee")
        except Exception as e:
            print(f"Impossible de charger la musique du niveau: {e}")
            # Fallback: essayer comme Sound au lieu de Music
            try:
                self.level_music_sound = pygame.mixer.Sound(music_path_str)
                self.level_music_sound.set_volume(0.4)
                # Utiliser un channel pour jouer avec boucle et STOCKER le channel
                self.level_music_channel = pygame.mixer.find_channel()
                if self.level_music_channel:
                    self.level_music_channel.play(self.level_music_sound, loops=-1)
                    print(f"Musique du niveau {self.current_level} lancee avec Sound (fallback)")
                else:
                    print("Aucun channel disponible")
            except Exception as e2:
                print(f"Fallback aussi echoue: {e2}")

    def _load_stage(self):
        """Charge le stage actuel depuis la config JSON"""
        if not self.stage_data:
            print("Error: No stage data")
            return

        # Obtenir la largeur du stage
        self.level_width = self.stage_data.get('width', 3000)

        # Charger le background
        self._load_background()

        # Charger les segments de sol
        for segment in self.stage_data.get('ground_segments', []):
            x = segment.get('x', 0)
            y = segment.get('y', GROUND_Y)
            width = segment.get('width', 1000)
            height = HEIGHT - y + 100
            ground = Platform(x, y, width, height, is_ground=True)
            self.platforms.add(ground)

        # Charger les plateformes
        for plat_data in self.stage_data.get('platforms', []):
            x = plat_data.get('x', 0)
            y = plat_data.get('y', 400)
            width = plat_data.get('width', 150)
            height = plat_data.get('height', 30)
            plat = Platform(x, y, width, height)
            self.platforms.add(plat)

        # Charger les ennemis
        for enemy_data in self.stage_data.get('enemies', []):
            x = enemy_data.get('x', 0)
            etype = enemy_data.get('type', 'hater')
            y = GROUND_Y  # Les ennemis spawns sur le sol par defaut
            enemy = Enemy(x, y, etype)
            self.enemies.add(enemy)

        # Charger les pickups
        for pickup_data in self.stage_data.get('pickups', []):
            x = pickup_data.get('x', 0)
            y = pickup_data.get('y', 400)
            ptype = pickup_data.get('type', 'note')
            pickup = Pickup(x, y, ptype)
            self.pickups.add(pickup)

        # Charger le boss si c'est un stage de boss
        boss_data = self.stage_data.get('boss')
        if boss_data:
            boss_x = boss_data.get('x', WIDTH - 200)
            self.boss = Boss(boss_x, GROUND_Y)
            self.enemies.add(self.boss)

    def _load_background(self):
        """Charge le background du stage"""
        if not self.stage_data:
            return

        try:
            bg_file = self.stage_data.get('background')
            if bg_file:
                path = IMG_BG_DIR / bg_file
                self.background = pygame.image.load(str(path)).convert()
                self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load background: {e}")
            self.background = None


    def handle_event(self, event):
        """Gere les evenements"""
        if event.type == pygame.KEYDOWN:
            # Menu de victoire apres mort du boss
            if self.victory_menu_active:
                if event.key == pygame.K_UP:
                    self.victory_menu_selected = (self.victory_menu_selected - 1) % len(self.victory_menu_options)
                elif event.key == pygame.K_DOWN:
                    self.victory_menu_selected = (self.victory_menu_selected + 1) % len(self.victory_menu_options)
                elif event.key in CONTROLS["confirm"]:
                    if self.victory_menu_selected == 0:  # Continuer -> map des niveaux
                        self._complete_stage()
                    else:  # Retour -> lobby (menu principal)
                        self.game.change_scene(STATE_MENU)
                return

            # Pause (pas pendant l'ultime ou la mort du boss)
            if event.key in CONTROLS["pause"] and not self.ultimate_active and not self.boss_death_active:
                self.game.change_scene(STATE_PAUSE)
                return

            # Debug
            if event.key in CONTROLS["debug_hitbox"]:
                self.debug_hitboxes = not self.debug_hitboxes
            if event.key in CONTROLS["debug_skip"]:
                self._complete_stage()
            if event.key in CONTROLS["debug_invincible"]:
                self.player.debug_invincible = not self.player.debug_invincible

            # Pendant la sequence ultime: F, G, H pour les 3 pistes
            if self.ultimate_active:
                for i, key in enumerate(LANE_KEYS):
                    if event.key == key:
                        self._ultimate_hit_lane(i)
                return

            # Attaque normale
            if event.key in CONTROLS["attack"]:
                self._player_attack()

            # Lancer l'ultime
            if event.key in CONTROLS["ultimate"]:
                self._player_ultimate()

        elif event.type == pygame.KEYUP:
            # Relacher les touches pendant l'ultime
            if self.ultimate_active:
                for i, key in enumerate(LANE_KEYS):
                    if event.key == key:
                        self.ultimate_lane_pressed[i] = False

    def _player_attack(self):
        """Le joueur attaque - attaque simple sans timing"""
        if not self.player.can_attack():
            return
        if self.ultimate_active:
            return  # Pas d'attaque normale pendant l'ultime
        if self.player.is_crouching:
            return  # Pas d'attaque quand accroupi

        # Creer le projectile (degats fixes)
        direction = 1 if self.player.facing_right else -1
        proj_x = self.player.rect.centerx + (30 * direction)
        proj = Projectile(proj_x, self.player.rect.centery, direction, 1.0)
        self.player_projectiles.add(proj)
        
        # Jouer le son de tir
        self._play_sound(SND_PLAYER_SHOOT)

        self.player.attack()

    def _player_ultimate(self):
        """Le joueur utilise son ultime - demarre la sequence Guitar Hero"""
        if not self.player.can_use_ultimate():
            return
        if self.ultimate_active:
            return  # Deja en cours

        # Consommer la charge
        self.player.use_ultimate()

        # Demarrer la sequence Guitar Hero
        self.ultimate_active = True
        self.ultimate_notes = []
        self.ultimate_notes_spawned = 0
        self.ultimate_spawn_timer = 0
        self.ultimate_results = []
        self.ultimate_total_damage = ULTIMATE_BASE_DAMAGE
        self.ultimate_lane_pressed = [False, False, False]
        self.player.state = "ultimate"

    def _ultimate_hit_lane(self, lane):
        """Le joueur appuie sur une touche (F=0, G=1, H=2)"""
        if not self.ultimate_active:
            return
        if self.ultimate_lane_pressed[lane]:
            return  # Deja appuye

        self.ultimate_lane_pressed[lane] = True

        # Chercher la note la plus proche sur cette piste
        closest_note = None
        closest_dist = float('inf')

        for note in self.ultimate_notes:
            if note["lane"] == lane:
                dist = abs(note["y"] - HIT_LINE_Y)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_note = note

        # Verifier le timing
        if closest_note and closest_dist <= HIT_ZONE_OK:
            # Determiner le resultat
            if closest_dist <= HIT_ZONE_PERFECT:
                result = "PERFECT!"
                self.ultimate_total_damage += ULTIMATE_DAMAGE_PER_PERFECT
            elif closest_dist <= HIT_ZONE_GOOD:
                result = "GOOD!"
                self.ultimate_total_damage += ULTIMATE_DAMAGE_PER_GOOD
            else:
                result = "OK"
                self.ultimate_total_damage += ULTIMATE_DAMAGE_PER_OK

            self.ultimate_results.append(result)
            self.timing_feedback = result
            self.timing_feedback_timer = 800  # Plus long pour etre lisible

            # Supprimer la note
            self.ultimate_notes.remove(closest_note)
        else:
            # Appui sans note = pas de penalite, juste ignorer
            pass

    def _finish_ultimate(self):
        """Termine la sequence ultime et lance l'attaque"""
        self.ultimate_active = False
        self.player.state = "attack"
        self.player.attack_anim_timer = 500  # Animation d'attaque pendant 500ms

        # Creer le projectile ultime avec les degats accumules
        direction = 1 if self.player.facing_right else -1

        # Projectile principal puissant - utilise l'image ultimate du joueur
        proj = Projectile(
            self.player.rect.centerx,
            self.player.rect.centery,
            direction,
            self.ultimate_total_damage
        )
        proj.speed = PROJECTILE_SPEED * 1.5

        # Utiliser l'image ultimate du joueur pour le projectile
        ult_img = self.player.images.get("ultimate")
        if ult_img:
            # Agrandir l'image pour l'effet visuel
            proj.image = pygame.transform.scale(ult_img, (PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2))
            if direction < 0:
                proj.image = pygame.transform.flip(proj.image, True, False)
        else:
            # Fallback: placeholder colore
            proj.image = pygame.Surface((PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2), pygame.SRCALPHA)
            color = (255, 200, 0) if self.player.character_id == 1 else (255, 150, 50)
            proj.image.fill(color)

        proj.rect = proj.image.get_rect(center=proj.rect.center)
        self.player_projectiles.add(proj)

        # Afficher les degats totaux
        self.timing_feedback = f"DAMAGE: {self.ultimate_total_damage}!"
        self.timing_feedback_timer = 2000  # Plus long pour etre lisible

    def update(self, dt):
        """Met a jour le gameplay"""
        dt_ms = dt * 1000

        # Timer pour animations visuelles (toujours actif)
        self.animation_time += dt

        # Pendant l'intro du boss: animation seulement
        if self.boss_intro_active:
            self._update_boss_intro(dt_ms)
            return

        # Pendant l'ultime: TOUT EST FIGE sauf la sequence Guitar Hero
        if self.ultimate_active:
            self._update_ultimate_sequence(dt_ms)
            # Feedback timer uniquement
            if self.timing_feedback_timer > 0:
                self.timing_feedback_timer -= dt_ms
            return  # Ne pas mettre a jour le reste du jeu

        # Pendant la celebration: animation seulement
        if self.celebration_active:
            self._update_celebration(dt_ms)
            return

        # Input joueur normal
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        # Mise a jour des entites
        self.player.update(dt, self.platforms)

        for proj in self.player_projectiles:
            proj.update(dt, self.camera_x)

        for proj in self.boss_projectiles:
            proj.update(dt)

        for pickup in self.pickups:
            pickup.update(dt)

        # Mise a jour des ennemis
        # Liste des ennemis normaux pour eviter les collisions entre eux
        normal_enemies = [e for e in self.enemies if not isinstance(e, Boss)]
        for enemy in self.enemies:
            if isinstance(enemy, Boss):
                enemy.update(dt, self.player.rect, self.boss_projectiles)
            else:
                enemy.update(dt, self.player.rect, self.platforms, normal_enemies)

        # Empecher les ennemis de se chevaucher
        self._resolve_enemy_collisions()

        # Verifier les chutes dans le vide
        self._check_fall_death()

        # Collisions
        self._check_collisions()

        # Camera
        self._update_camera()

        # Feedback timer
        if self.timing_feedback_timer > 0:
            self.timing_feedback_timer -= dt_ms

        # Mise a jour des nombres de degats flottants
        self._update_damage_numbers(dt_ms)

        # Verifier fin de niveau
        self._check_level_end()

        # Verifier game over
        if self.player.health <= 0:
            self._stop_all_music()  # Arreter toute la musique
            self.game.game_data["score"] = self.game.game_data.get("score", 0)
            self.game.change_scene(STATE_GAME_OVER)

    def _update_ultimate_sequence(self, dt_ms):
        """Met a jour la sequence Guitar Hero avec notes qui tombent"""
        # Spawn de nouvelles notes
        self.ultimate_spawn_timer += dt_ms
        if self.ultimate_spawn_timer >= NOTE_SPAWN_INTERVAL:
            if self.ultimate_notes_spawned < ULTIMATE_NOTE_COUNT:
                self.ultimate_spawn_timer = 0
                # Creer une note sur une piste aleatoire
                lane = random.randint(0, LANE_COUNT - 1)
                self.ultimate_notes.append({
                    "lane": lane,
                    "y": TRACK_Y  # Commence en haut
                })
                self.ultimate_notes_spawned += 1

        # Faire tomber les notes
        notes_to_remove = []
        for note in self.ultimate_notes:
            note["y"] += NOTE_FALL_SPEED

            # Note ratee (passee sous la ligne de frappe)
            if note["y"] > HIT_LINE_Y + HIT_ZONE_OK + NOTE_SIZE:
                notes_to_remove.append(note)
                self.ultimate_results.append("MISS")
                self.timing_feedback = "MISS"
                self.timing_feedback_timer = 800  # Plus long pour etre lisible

        for note in notes_to_remove:
            self.ultimate_notes.remove(note)

        # Verifier si la sequence est terminee
        if self.ultimate_notes_spawned >= ULTIMATE_NOTE_COUNT and len(self.ultimate_notes) == 0:
            self._finish_ultimate()

    def _check_fall_death(self):
        """Verifie si des entites sont tombees dans le vide"""
        fall_limit = HEIGHT + 50  # En dessous de l'ecran

        # Joueur tombe dans le vide
        if self.player.rect.top > fall_limit:
            self._play_sound(SND_DEATH)  # Jouer le son de mort
            self.player.health = 0  # Mort instantanee

        # Ennemis tombent dans le vide
        for enemy in list(self.enemies):
            if enemy.rect.top > fall_limit:
                enemy.kill()

    def _resolve_enemy_collisions(self):
        """Empeche les ennemis de se chevaucher"""
        # Filtrer les ennemis vivants seulement (pas le boss, pas les morts)
        enemies_list = [e for e in self.enemies if not isinstance(e, Boss) and not e.is_dead]

        # Distance minimale entre ennemis pour eviter l'oscillation
        min_separation = 10

        for i, enemy1 in enumerate(enemies_list):
            for enemy2 in enemies_list[i + 1:]:
                # Calculer la distance entre les centres
                dist_x = abs(enemy1.rect.centerx - enemy2.rect.centerx)
                min_dist = (enemy1.rect.width + enemy2.rect.width) // 2 + min_separation

                # Si trop proches (meme sans chevauchement strict)
                if dist_x < min_dist and enemy1.rect.colliderect(enemy2.rect.inflate(min_separation * 2, 0)):
                    # Calculer combien il faut pousser
                    push_amount = (min_dist - dist_x) // 2 + 1

                    # Pousser les ennemis dans des directions opposees
                    if enemy1.rect.centerx < enemy2.rect.centerx:
                        enemy1.rect.x -= push_amount
                        enemy2.rect.x += push_amount
                    else:
                        enemy1.rect.x += push_amount
                        enemy2.rect.x -= push_amount

    def _add_damage_number(self, x, y, damage, color=YELLOW):
        """Ajoute un nombre de degats flottant"""
        self.damage_numbers.append({
            "x": x,
            "y": y,
            "damage": damage,
            "timer": 1500,  # 1.5 secondes d'affichage
            "color": color,
            "offset_y": 0,
        })

    def _update_damage_numbers(self, dt_ms):
        """Met a jour les nombres de degats flottants"""
        for dmg in self.damage_numbers[:]:
            dmg["timer"] -= dt_ms
            dmg["offset_y"] -= 1.5  # Monte vers le haut
            if dmg["timer"] <= 0:
                self.damage_numbers.remove(dmg)

    def _check_collisions(self):
        """Verifie toutes les collisions"""
        # Projectiles joueur -> Ennemis
        for proj in self.player_projectiles:
            for enemy in self.enemies:
                if proj.rect.colliderect(enemy.rect):
                    proj.kill()
                    is_dead = enemy.take_damage(proj.damage)
                    self.player.add_ultimate_charge(ULTIMATE_CHARGE_PER_HIT)

                    # Afficher les degats infliges
                    self._add_damage_number(
                        enemy.rect.centerx,
                        enemy.rect.top,
                        proj.damage,
                        YELLOW
                    )

                    if is_dead:
                        self.game.game_data["score"] += enemy.score_value
                        self._play_sound(SND_ENEMY_DEATH)  # Son de mort d'ennemi
                        if isinstance(enemy, Boss):
                            self.boss = None
                        enemy.kill()
                    break

        # Projectiles boss -> Joueur
        for proj in self.boss_projectiles:
            if proj.rect.colliderect(self.player.rect):
                proj.kill()
                if self.player.take_damage(proj.damage):
                    self.game.game_data["lives"] = self.player.health

        # Ennemis -> Joueur (contact)
        for enemy in self.enemies:
            if hasattr(enemy, 'is_dead') and enemy.is_dead:
                continue  # Ignorer les ennemis morts
            if self.player.rect.colliderect(enemy.rect):
                # Verifier si le joueur saute sur la tete de l'ennemi (pas le boss)
                if (not isinstance(enemy, Boss) and
                    self.player.velocity_y > 0 and
                    self.player.rect.bottom <= enemy.rect.top + 30):
                    # Tuer l'ennemi en sautant dessus
                    enemy.is_dead = True
                    enemy.state = "dead"
                    self.game.game_data["score"] += enemy.score_value
                    # Afficher "STOMP!" ou les degats
                    self._add_damage_number(
                        enemy.rect.centerx,
                        enemy.rect.top,
                        enemy.max_health,
                        ORANGE
                    )
                    # Faire rebondir le joueur
                    self.player.velocity_y = -10
                    self.player.rect.bottom = enemy.rect.top
                else:
                    # Collision normale - le joueur prend des degats
                    if self.player.take_damage(enemy.damage):
                        self.game.game_data["lives"] = self.player.health
                        # Decaler le joueur de quelques pixels pour eviter la superposition
                        # Direction: vers le dos du joueur (oppose a la direction qu'il regarde)
                        if self.player.rect.centerx < enemy.rect.centerx:
                            # Ennemi a droite, decaler le joueur a gauche
                            self.player.rect.x -= 5
                        else:
                            # Ennemi a gauche, decaler le joueur a droite
                            self.player.rect.x += 5

        # Joueur -> Pickups
        for pickup in self.pickups:
            if self.player.rect.colliderect(pickup.rect):
                self._collect_pickup(pickup)
                pickup.kill()

    def _collect_pickup(self, pickup):
        """Collecte un pickup"""
        self._play_sound(SND_BONUS_PICKUP)  # Son de collecte de bonus
        
        if pickup.pickup_type == "note":
            self.game.game_data["score"] += PICKUP_NOTE_SCORE
        elif pickup.pickup_type == "mediator":
            self.player.add_ultimate_charge(PICKUP_MEDIATOR_ULTIMATE)
        elif pickup.pickup_type == "ampli":
            # Boost temporaire (a implementer si besoin)
            self.game.game_data["score"] += PICKUP_NOTE_SCORE * 2
        elif pickup.pickup_type == "health":
            # Soigne le joueur d'un coeur
            self.player.heal(1)
            self.game.game_data["lives"] = self.player.health

    def _update_camera(self):
        """Met a jour la position de la camera"""
        # La camera suit le joueur
        target_x = self.player.rect.centerx - WIDTH // 3

        # Limiter aux bords du niveau
        target_x = max(0, min(target_x, self.level_width - WIDTH))

        # Lissage
        self.camera_x += (target_x - self.camera_x) * 0.1

    def _play_sound(self, sound_file):
        """Joue un son"""
        try:
            sound_path = SND_DIR / sound_file
            sound = pygame.mixer.Sound(str(sound_path))
            sound.set_volume(0.25)  # Volume reduit (0.25 = 25%) pour les effets sonores
            sound.play()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Impossible de jouer le son: {e}")

    def _stop_all_music(self):
        """Arrete toute la musique (music et sound des niveaux/boss et leurs channels)"""
        # Arreter mixer.music
        pygame.mixer.music.stop()
        
        # Arreter les sounds et channels stockes
        if self.level_music_sound:
            self.level_music_sound.stop()
        if self.level_music_channel:
            self.level_music_channel.stop()
        if self.boss_intro_sound:
            self.boss_intro_sound.stop()
        if self.boss_intro_channel:
            self.boss_intro_channel.stop()

    def _check_level_end(self):
        """Verifie si le stage est termine"""
        if self.celebration_active:
            return  # Deja en celebration

        # Verifier si c'est un stage de boss
        is_boss_stage = self.stage_data and self.stage_data.get('is_boss_stage', False)

        if is_boss_stage:
            # Stage boss - victoire si boss mort
            if self.boss is None or self.boss not in self.enemies:
                self._start_celebration()
        else:
            # Stages normaux - atteindre la fin
            if self.player.rect.right >= self.level_width - 50:
                self._complete_stage()

    def _start_celebration(self):
        """Demarre l'animation de mort du boss avec zoom"""
        self.celebration_active = True
        self.celebration_timer = 0

        # Demarrer l'animation de mort du boss
        self.boss_death_active = True
        self.boss_death_timer = 0
        self.boss_death_alpha = 255
        self.boss_death_zoom = 1.0

        # Position du boss pour l'animation (centre de l'ecran)
        if self.boss:
            self.boss_death_pos = (self.boss.rect.centerx, self.boss.rect.centery)
            # Camera cible pour centrer sur le boss
            self.target_camera_x = self.boss.rect.centerx - WIDTH // 2
            self.target_camera_x = max(0, min(self.target_camera_x, self.level_width - WIDTH))
        else:
            self.boss_death_pos = (WIDTH // 2 + self.camera_x, HEIGHT // 2)
            self.target_camera_x = self.camera_x

        # Arreter la musique du boss
        self._stop_all_music()
        
        # Jouer la musique de victoire
        try:
            music_path = SND_DIR / SND_VICTORY
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Impossible de charger la musique de victoire: {e}")

    def _start_boss_intro(self):
        """Demarre l'ecran d'intro avant le combat final"""
        self.boss_intro_active = True
        self.boss_intro_timer = 0
        self.boss_intro_sound = None  # Reset le son precedent
        self.boss_intro_channel = None
        
        # Charger l'image d'intro
        try:
            img_path = IMG_DIR / IMG_BOSS_INTRO
            self.boss_intro_image = pygame.image.load(str(img_path)).convert()
            self.boss_intro_image = pygame.transform.scale(self.boss_intro_image, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Impossible de charger l'image du boss intro: {e}")
            self.boss_intro_image = None
        
        # Arreter la musique precedente (mixer.music ET level_music_sound et tous les channels)
        self._stop_all_music()
        try:
            music_path = SND_DIR / SND_MUSIC_BOSS_INTRO
            music_path_str = str(music_path)
            print(f"Tentative de chargement: {music_path_str}")
            pygame.mixer.music.load(music_path_str)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # -1 = boucle infinie
            print(f"Musique du combat final lancee")
        except Exception as e:
            print(f"Impossible de charger la musique du combat final: {e}")
            # Fallback: essayer comme Sound au lieu de Music
            try:
                self.boss_intro_sound = pygame.mixer.Sound(music_path_str)
                self.boss_intro_sound.set_volume(0.5)
                # Utiliser un channel pour jouer avec boucle et STOCKER le channel
                self.boss_intro_channel = pygame.mixer.find_channel()
                if self.boss_intro_channel:
                    self.boss_intro_channel.play(self.boss_intro_sound, loops=-1)
                    print(f"Musique du combat final lancee avec Sound (fallback)")
                else:
                    print("Aucun channel disponible")
            except Exception as e2:
                print(f"Fallback aussi echoue: {e2}")

    def _update_boss_intro(self, dt_ms):
        """Met a jour l'animation d'intro du boss"""
        self.boss_intro_timer += dt_ms
        
        # Si 6 secondes sont ecoulees, lancer le boss
        if self.boss_intro_timer >= self.boss_intro_duration:
            self.boss_intro_active = False
            self.game.game_data["current_level"] = 3
            self.enter()

    def _update_celebration(self, dt_ms):
        """Met a jour l'animation de mort du boss"""
        self.celebration_timer += dt_ms
        self.boss_death_timer += dt_ms

        # Phase 1: Zoom smooth sur le boss (0-2000ms)
        if self.boss_death_timer < 2000:
            # Zoom progressif de 1.0 a 1.5
            progress = self.boss_death_timer / 2000
            self.boss_death_zoom = 1.0 + progress * 0.5

            # Deplacement smooth de la camera vers le boss
            camera_diff = self.target_camera_x - self.camera_x
            self.camera_x += camera_diff * 0.05

        # Phase 2: Fade out du boss (2000-4000ms)
        elif self.boss_death_timer < 4000:
            progress = (self.boss_death_timer - 2000) / 2000
            self.boss_death_alpha = int(255 * (1 - progress))
            self.boss_death_zoom = 1.5

        # Phase 3: Dezoom et affichage du menu (4000-5000ms)
        elif self.boss_death_timer < 5000:
            progress = (self.boss_death_timer - 4000) / 1000
            self.boss_death_zoom = 1.5 - progress * 0.5
            self.boss_death_alpha = 0

        # Phase 4: Afficher le menu de victoire
        else:
            self.boss_death_active = False
            self.victory_menu_active = True

    def _complete_stage(self):
        """Complete le stage actuel et passe au suivant ou au niveau suivant"""
        # Sauvegarder l'etat du joueur
        self.game.game_data["lives"] = self.player.health
        self.game.game_data["ultimate_charge"] = self.player.ultimate_charge

        # Obtenir le nombre total de stages dans ce niveau
        total_stages = len(self.level_data.get('stages', [])) if self.level_data else 3

        if self.current_stage_id < total_stages:
            if self.current_level == 2:
                # Transition vers le boss avec image intro
                self._start_boss_intro()
            else:
                # Passer au stage suivant du meme niveau
            self.current_stage_id += 1 normalement
                self.game.game_data["current_stage"] = self.current_stage_id
                self.enter(level_id=self.current_level_id, stage_id=self.current_stage_id)
        else:
            # Niveau complete! Marquer comme complete et calculer les etoiles
            if self.current_level_id not in self.game.game_data["completed_levels"]:
                self.game.game_data["completed_levels"].append(self.current_level_id)

            # Calculer les etoiles basees sur le score
            score = self.game.game_data.get("score", 0)
            stars = self.loader.get_stars_count(self.current_level_id, score)
            self.game.game_data["level_stars"][self.current_level_id] = max(
                stars,
                self.game.game_data["level_stars"].get(self.current_level_id, 0)
            )

            # Aller directement a la map des niveaux
            self.game.change_scene(STATE_LEVEL_SELECT)

    def draw(self, screen):
        """Dessine le gameplay"""
        # Background
        if self.background:
            # Parallax simple
            bg_offset = int(self.camera_x * 0.3) % WIDTH
            screen.blit(self.background, (-bg_offset, 0))
            screen.blit(self.background, (WIDTH - bg_offset, 0))
        else:
            self._draw_placeholder_bg(screen)

        # Plateformes
        for platform in self.platforms:
            draw_rect = platform.rect.move(-self.camera_x, 0)
            if draw_rect.right > 0 and draw_rect.left < WIDTH:
                screen.blit(platform.image, draw_rect)

        # Pickups
        for pickup in self.pickups:
            draw_rect = pickup.rect.move(-self.camera_x, 0)
            if draw_rect.right > 0 and draw_rect.left < WIDTH:
                screen.blit(pickup.image, draw_rect)

        # Ennemis
        for enemy in self.enemies:
            if isinstance(enemy, Boss):
                enemy.draw(screen, self.camera_x)
            else:
                enemy.draw(screen, self.camera_x)

        # Projectiles
        for proj in self.player_projectiles:
            draw_rect = proj.rect.move(-self.camera_x, 0)
            screen.blit(proj.image, draw_rect)

        for proj in self.boss_projectiles:
            draw_rect = proj.rect.move(-self.camera_x, 0)
            screen.blit(proj.image, draw_rect)

        # Joueur
        player_draw_rect = self.player.rect.move(-self.camera_x, 0)
        # Effet de clignotement si invincible
        if self.player.invincible:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                screen.blit(self.player.image, player_draw_rect)
        else:
            screen.blit(self.player.image, player_draw_rect)

        # Nombres de degats flottants
        self._draw_damage_numbers(screen)

        # Debug hitboxes
        if self.debug_hitboxes:
            self._draw_debug_hitboxes(screen)

        # HUD
        self._draw_hud(screen)

        # Barre Guitar Hero (UNIQUEMENT pendant l'ultime)
        if self.ultimate_active:
            self._draw_ultimate_overlay(screen)
            self._draw_rhythm_bar(screen)

        # Feedback timing
        if self.timing_feedback_timer > 0:
            self._draw_timing_feedback(screen)

        # Celebration (apres avoir battu le boss)
        if self.celebration_active:
            self._draw_celebration(screen)

        # Boss intro (transition avant combat final)
        if self.boss_intro_active:
            self._draw_boss_intro(screen)

    def _draw_boss_intro(self, screen):
        """Dessine l'ecran d'intro du boss"""
        if self.boss_intro_image:
            screen.blit(self.boss_intro_image, (0, 0))
        else:
            # Fond noir si pas d'image
            screen.fill((0, 0, 0))
            # Afficher un texte si pas d'image
            font = pygame.font.Font(None, 48)
            text = font.render("COMBAT FINAL", True, YELLOW)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

    def _draw_celebration(self, screen):
        """Dessine l'animation de mort du boss et le menu de victoire"""
        # Fond semi-transparent sombre
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        # Dessiner l'image de mort du boss avec zoom et fade
        if self.boss_death_active and self.boss_death_image and self.boss_death_alpha > 0:
            # Position relative a la camera
            draw_x = self.boss_death_pos[0] - self.camera_x
            draw_y = self.boss_death_pos[1]

            # Appliquer le zoom
            original_size = self.boss_death_image.get_size()
            new_width = int(original_size[0] * self.boss_death_zoom)
            new_height = int(original_size[1] * self.boss_death_zoom)
            scaled_img = pygame.transform.scale(self.boss_death_image, (new_width, new_height))

            # Appliquer l'alpha (transparence)
            scaled_img.set_alpha(self.boss_death_alpha)

            # Centrer l'image
            img_rect = scaled_img.get_rect(center=(draw_x, draw_y))
            screen.blit(scaled_img, img_rect)

        # Texte "BOSS VAINCU!" avec effet de pulsation
        pulse = 1.0 + math.sin(self.celebration_timer / 200) * 0.15
        font_size = int(72 * pulse)
        try:
            font = pygame.font.Font(str(FONT_METAL_MANIA), font_size)
        except (pygame.error, FileNotFoundError):
            font = pygame.font.Font(None, font_size)

        # Ombre du texte
        shadow_text = font.render("BOSS VAINCU!", True, (50, 50, 50))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 4, HEIGHT // 4 + 4))
        screen.blit(shadow_text, shadow_rect)

        # Texte principal
        text = font.render("BOSS VAINCU!", True, YELLOW)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(text, text_rect)

        # Message "Vous avez gagne!"
        try:
            sub_font = pygame.font.Font(str(FONT_ROAD_RAGE), 36)
        except (pygame.error, FileNotFoundError):
            sub_font = pygame.font.Font(None, 36)

        win_text = sub_font.render("Vous avez gagne!", True, WHITE)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 70))
        screen.blit(win_text, win_rect)

        # Menu de victoire (apres le fade du boss)
        if self.victory_menu_active:
            self._draw_victory_menu(screen)

    def _draw_victory_menu(self, screen):
        """Dessine le menu continuer/quitter apres la mort du boss"""
        try:
            menu_font = pygame.font.Font(str(FONT_ROAD_RAGE), 36)
            small_font = pygame.font.Font(str(FONT_ROAD_RAGE), 24)
        except (pygame.error, FileNotFoundError):
            menu_font = pygame.font.Font(None, 36)
            small_font = pygame.font.Font(None, 24)

        # Box du menu
        box_width = 300
        box_height = 150
        box_x = (WIDTH - box_width) // 2
        box_y = HEIGHT // 2 + 50

        # Fond de la boite
        box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surf.fill((30, 20, 40, 220))
        screen.blit(box_surf, (box_x, box_y))

        # Bordure animee
        border_color = (
            int(200 + math.sin(self.animation_time * 4) * 55),
            int(100 + math.sin(self.animation_time * 3) * 50),
            0
        )
        pygame.draw.rect(screen, border_color, (box_x, box_y, box_width, box_height), 3, border_radius=10)

        # Options
        for i, option in enumerate(self.victory_menu_options):
            y = box_y + 40 + i * 55
            is_selected = i == self.victory_menu_selected

            if is_selected:
                sel_surf = pygame.Surface((box_width - 40, 45), pygame.SRCALPHA)
                sel_surf.fill((255, 200, 0, 80))
                screen.blit(sel_surf, (box_x + 20, y - 8))

                # Fleche animee
                arrow_offset = math.sin(self.animation_time * 8) * 5
                arrow_size = 12
                points = [
                    (box_x + 30 + arrow_offset, y + 14 - arrow_size // 2),
                    (box_x + 30 + arrow_offset, y + 14 + arrow_size // 2),
                    (box_x + 30 + arrow_offset + arrow_size, y + 14)
                ]
                pygame.draw.polygon(screen, YELLOW, points)

                color = YELLOW
            else:
                color = WHITE

            text = menu_font.render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, y + 14))
            screen.blit(text, rect)

        # Instructions
        instructions = small_font.render("Fleches + Entree pour choisir", True, GRAY)
        inst_rect = instructions.get_rect(center=(WIDTH // 2, box_y + box_height + 20))
        screen.blit(instructions, inst_rect)

    def _draw_placeholder_bg(self, screen):
        """Dessine un fond placeholder"""
        # Gradient selon le niveau
        colors = {
            1: ((40, 30, 50), (60, 40, 70)),   # Coulisses - violet sombre
            2: ((50, 40, 30), (80, 60, 40)),   # Scene - marron/orange
            3: ((60, 20, 30), (90, 30, 40)),   # Boss - rouge sombre
        }
        c1, c2 = colors.get(self.current_level_id, ((30, 30, 40), (50, 50, 60)))

        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(c1[0] + (c2[0] - c1[0]) * ratio)
            g = int(c1[1] + (c2[1] - c1[1]) * ratio)
            b = int(c1[2] + (c2[2] - c1[2]) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    def _draw_debug_hitboxes(self, screen):
        """Dessine les hitboxes en mode debug"""
        # Joueur
        player_rect = self.player.rect.move(-self.camera_x, 0)
        pygame.draw.rect(screen, GREEN, player_rect, 2)

        # Ennemis
        for enemy in self.enemies:
            enemy_rect = enemy.rect.move(-self.camera_x, 0)
            pygame.draw.rect(screen, RED, enemy_rect, 2)

        # Projectiles
        for proj in self.player_projectiles:
            proj_rect = proj.rect.move(-self.camera_x, 0)
            pygame.draw.rect(screen, YELLOW, proj_rect, 2)

        for proj in self.boss_projectiles:
            proj_rect = proj.rect.move(-self.camera_x, 0)
            pygame.draw.rect(screen, ORANGE, proj_rect, 2)

    def _draw_damage_numbers(self, screen):
        """Dessine les nombres de degats flottants"""
        for dmg in self.damage_numbers:
            # Position avec camera
            draw_x = dmg["x"] - self.camera_x
            draw_y = dmg["y"] + dmg["offset_y"]

            # Alpha basé sur le timer restant (fade out)
            alpha = min(255, int(dmg["timer"] / 1500 * 255))

            # Taille selon les degats
            if dmg["damage"] >= 5:
                font_size = 36
            elif dmg["damage"] >= 3:
                font_size = 30
            else:
                font_size = 24

            try:
                dmg_font = pygame.font.Font(str(FONT_METAL_MANIA), font_size)
            except (pygame.error, FileNotFoundError):
                dmg_font = pygame.font.Font(None, font_size)

            # Texte des degats
            text = f"-{dmg['damage']}"
            color = dmg["color"]

            # Ombre
            shadow_surf = dmg_font.render(text, True, (0, 0, 0))
            shadow_surf.set_alpha(alpha)
            shadow_rect = shadow_surf.get_rect(center=(draw_x + 2, draw_y + 2))
            screen.blit(shadow_surf, shadow_rect)

            # Texte principal
            text_surf = dmg_font.render(text, True, color)
            text_surf.set_alpha(alpha)
            text_rect = text_surf.get_rect(center=(draw_x, draw_y))
            screen.blit(text_surf, text_rect)

    def _draw_hud(self, screen):
        """Dessine le HUD"""
        # Vie (coeurs/guitares)
        for i in range(PLAYER_MAX_HEALTH):
            x = HUD_MARGIN + i * (HUD_HEALTH_SIZE + 10)
            y = HUD_MARGIN

            if i < self.player.health:
                color = RED
            else:
                color = GRAY

            # Dessiner un coeur simple
            pygame.draw.circle(screen, color, (x + 10, y + 15), 10)
            pygame.draw.circle(screen, color, (x + 25, y + 15), 10)
            pygame.draw.polygon(screen, color, [
                (x, y + 20),
                (x + 35, y + 20),
                (x + 17, y + 40)
            ])

        # Score
        score_text = self.font.render(f"Score: {self.game.game_data['score']}", True, WHITE)
        screen.blit(score_text, (WIDTH - 200, HUD_MARGIN))

        # Combo
        if self.combo > 1:
            combo_text = self.font_big.render(f"x{self.combo}", True, YELLOW)
            screen.blit(combo_text, (WIDTH - 100, HUD_MARGIN + 30))

        # Niveau et stage
        if self.level_data and self.stage_data:
            level_name = self.level_data.get('name', 'Unknown')
            stage_name = self.stage_data.get('name', f'Stage {self.current_stage_id}')
            level_text = self.font.render(f"{level_name} - {stage_name}", True, WHITE)
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HUD_MARGIN))

        # Jauge ultime
        ult_bar_width = 150
        ult_bar_height = 15
        ult_x = HUD_MARGIN
        ult_y = HUD_MARGIN + 60

        # Effet special quand ultime au max
        if self.player.can_use_ultimate():
            # Effet de pulsation (scale)
            pulse = 1.0 + math.sin(self.animation_time * 8) * 0.08
            pulse_width = int(ult_bar_width * pulse)
            pulse_height = int(ult_bar_height * pulse)
            pulse_x = ult_x - (pulse_width - ult_bar_width) // 2
            pulse_y = ult_y - (pulse_height - ult_bar_height) // 2

            # Glow effect (halo lumineux)
            glow_alpha = int(100 + math.sin(self.animation_time * 6) * 55)
            glow_surface = pygame.Surface((pulse_width + 20, pulse_height + 20), pygame.SRCALPHA)
            glow_color = (255, 200, 0, glow_alpha)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, pulse_width + 20, pulse_height + 20), border_radius=8)
            screen.blit(glow_surface, (pulse_x - 10, pulse_y - 10))

            # Couleur qui oscille entre violet et or
            color_shift = (math.sin(self.animation_time * 10) + 1) / 2
            ult_r = int(150 + color_shift * 105)
            ult_g = int(0 + color_shift * 215)
            ult_b = int(255 - color_shift * 255)
            ult_color = (ult_r, ult_g, ult_b)

            # Fond
            pygame.draw.rect(screen, DARK_GRAY, (pulse_x, pulse_y, pulse_width, pulse_height), border_radius=4)
            # Barre remplie
            pygame.draw.rect(screen, ult_color, (pulse_x, pulse_y, pulse_width, pulse_height), border_radius=4)
            # Effet de brillance qui se deplace
            shine_x = int((math.sin(self.animation_time * 4) + 1) / 2 * (pulse_width - 30))
            shine_surface = pygame.Surface((30, pulse_height), pygame.SRCALPHA)
            for i in range(30):
                alpha = int(150 * (1 - abs(i - 15) / 15))
                pygame.draw.line(shine_surface, (255, 255, 255, alpha), (i, 0), (i, pulse_height))
            screen.blit(shine_surface, (pulse_x + shine_x, pulse_y))
            # Bordure
            pygame.draw.rect(screen, YELLOW, (pulse_x, pulse_y, pulse_width, pulse_height), 2, border_radius=4)

            # Label avec effet
            label_color = (255, int(200 + math.sin(self.animation_time * 8) * 55), 0)
            ult_label = self.font.render("ULTIME PRET!", True, label_color)
        else:
            # Jauge normale
            pygame.draw.rect(screen, GRAY, (ult_x, ult_y, ult_bar_width, ult_bar_height))
            ult_fill = int((self.player.ultimate_charge / ULTIMATE_CHARGE_MAX) * ult_bar_width)
            pygame.draw.rect(screen, BLUE, (ult_x, ult_y, ult_fill, ult_bar_height))
            pygame.draw.rect(screen, WHITE, (ult_x, ult_y, ult_bar_width, ult_bar_height), 2)
            ult_label = self.font.render("ULTIME 'K'", True, WHITE)

        screen.blit(ult_label, (ult_x, ult_y + 18))

        # Debug info
        if self.debug_hitboxes:
            debug_text = self.font.render(
                f"DEBUG | Invincible: {self.player.debug_invincible} | F1:Hitbox F2:Skip F3:Godmode",
                True, YELLOW
            )
            screen.blit(debug_text, (10, HEIGHT - 30))

    def _draw_ultimate_overlay(self, screen):
        """Dessine l'overlay Guitar Hero pendant la sequence ultime"""
        # Fond semi-transparent
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Titre ULTIMATE
        title = self.font_big.render("ULTIMATE!", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title, title_rect)

        # Degats accumules
        dmg_text = self.font_big.render(f"Damage: {self.ultimate_total_damage}", True, ORANGE)
        dmg_rect = dmg_text.get_rect(center=(WIDTH // 2, 90))
        screen.blit(dmg_text, dmg_rect)

        # Compteur de notes
        notes_left = ULTIMATE_NOTE_COUNT - len(self.ultimate_results)
        count_text = self.font.render(f"Notes: {notes_left}/{ULTIMATE_NOTE_COUNT}", True, WHITE)
        count_rect = count_text.get_rect(center=(WIDTH // 2, 120))
        screen.blit(count_text, count_rect)

    def _draw_rhythm_bar(self, screen):
        """Dessine la piste Guitar Hero avec les 3 colonnes (F, G, H)"""
        # Fond de la piste
        track_rect = pygame.Rect(TRACK_X, TRACK_Y, TRACK_WIDTH, TRACK_HEIGHT)
        pygame.draw.rect(screen, (20, 20, 30), track_rect)

        # Dessiner les 3 pistes (colonnes)
        for i in range(LANE_COUNT):
            lane_x = TRACK_X + i * LANE_WIDTH
            lane_color = LANE_COLORS[i]

            # Fond de la piste (plus sombre)
            dark_color = (lane_color[0] // 4, lane_color[1] // 4, lane_color[2] // 4)
            pygame.draw.rect(screen, dark_color,
                           (lane_x + 2, TRACK_Y, LANE_WIDTH - 4, TRACK_HEIGHT))

            # Separateurs entre pistes
            pygame.draw.line(screen, GRAY, (lane_x, TRACK_Y), (lane_x, TRACK_Y + TRACK_HEIGHT), 2)

        # Ligne de frappe (zone cible)
        pygame.draw.line(screen, WHITE,
                        (TRACK_X, HIT_LINE_Y),
                        (TRACK_X + TRACK_WIDTH, HIT_LINE_Y), 4)

        # Zones de timing sur la ligne de frappe
        for i in range(LANE_COUNT):
            lane_x = TRACK_X + i * LANE_WIDTH + LANE_WIDTH // 2
            lane_color = LANE_COLORS[i]

            # Cercle cible (plus brillant si touche pressee)
            if self.ultimate_lane_pressed[i]:
                pygame.draw.circle(screen, lane_color, (lane_x, HIT_LINE_Y), NOTE_SIZE // 2 + 5)
                pygame.draw.circle(screen, WHITE, (lane_x, HIT_LINE_Y), NOTE_SIZE // 2, 3)
            else:
                dark_color = (lane_color[0] // 2, lane_color[1] // 2, lane_color[2] // 2)
                pygame.draw.circle(screen, dark_color, (lane_x, HIT_LINE_Y), NOTE_SIZE // 2)
                pygame.draw.circle(screen, lane_color, (lane_x, HIT_LINE_Y), NOTE_SIZE // 2, 2)

        # Dessiner les notes qui tombent
        for note in self.ultimate_notes:
            lane_x = TRACK_X + note["lane"] * LANE_WIDTH + LANE_WIDTH // 2
            lane_color = LANE_COLORS[note["lane"]]

            # Note (cercle colore)
            pygame.draw.circle(screen, lane_color, (lane_x, int(note["y"])), NOTE_SIZE // 2)
            pygame.draw.circle(screen, WHITE, (lane_x, int(note["y"])), NOTE_SIZE // 2, 2)

            # Trainee lumineuse
            pygame.draw.line(screen, lane_color,
                           (lane_x, int(note["y"]) - NOTE_SIZE // 2),
                           (lane_x, int(note["y"]) - NOTE_SIZE), 4)

        # Bordure de la piste
        pygame.draw.rect(screen, WHITE, track_rect, 3)

        # Labels des touches (F, G, H)
        key_names = ["F", "G", "H"]
        for i in range(LANE_COUNT):
            lane_x = TRACK_X + i * LANE_WIDTH + LANE_WIDTH // 2
            key_text = self.font_big.render(key_names[i], True, LANE_COLORS[i])
            key_rect = key_text.get_rect(center=(lane_x, TRACK_Y + TRACK_HEIGHT + 30))
            screen.blit(key_text, key_rect)

        # Afficher les resultats (cercles colores en bas)
        result_colors = {"PERFECT!": YELLOW, "GOOD!": GREEN, "OK": BLUE, "MISS": RED}
        start_x = TRACK_X
        for i, result in enumerate(self.ultimate_results[-8:]):  # Max 8 derniers resultats
            color = result_colors.get(result, WHITE)
            pygame.draw.circle(screen, color, (start_x + i * 30 + 15, TRACK_Y + TRACK_HEIGHT + 70), 10)

    def _draw_timing_feedback(self, screen):
        """Dessine le feedback de timing"""
        colors = {
            "PERFECT!": YELLOW,
            "GOOD!": GREEN,
            "OK": BLUE,
            "MISS": RED,
        }
        color = colors.get(self.timing_feedback, WHITE)

        # Taille selon importance
        if self.timing_feedback == "PERFECT!":
            font = self.font_big
        else:
            font = self.font

        text = font.render(self.timing_feedback, True, color)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

        # Fond semi-transparent
        bg_rect = text_rect.inflate(20, 10)
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 150))
        screen.blit(bg_surf, bg_rect)

        screen.blit(text, text_rect)
