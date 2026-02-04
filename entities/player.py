"""
Rockstar Bros - Classe Player
Gestion du joueur, animation, collision et combat
"""

import pygame
from settings import (
    PLAYER_WIDTH, PLAYER_HEIGHT, PURPLE, ORANGE,
    PLAYER_SPEED, PLAYER_JUMP_FORCE, PLAYER_MAX_HEALTH,
    PLAYER_INVINCIBILITY_TIME, CONTROLS,
    GRAVITY, MAX_FALL_SPEED,
    PROJECTILE_COOLDOWN, ULTIMATE_CHARGE_MAX,
    IMG_PLAYER_DIR,
    IMG_PLAYER1_IDLE, IMG_PLAYER1_RUN1, IMG_PLAYER1_RUN2, IMG_PLAYER1_JUMP, IMG_PLAYER1_ATTACK,
    IMG_PLAYER2_IDLE, IMG_PLAYER2_RUN1, IMG_PLAYER2_RUN2, IMG_PLAYER2_JUMP, IMG_PLAYER2_ATTACK,
    IMG_PLAYER1_ULTIMATE, IMG_PLAYER2_ULTIMATE,
)


class Player(pygame.sprite.Sprite):
    """Classe du joueur"""

    def __init__(self, character_id, x, y):
        super().__init__()
        self.character_id = character_id

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
