"""
Rockstar Bros - Classe Player
Gere le joueur: mouvements, animations, combat
"""

import pygame
from settings import (
    PURPLE, ORANGE,
    GRAVITY, MAX_FALL_SPEED,
    PLAYER_SPEED, PLAYER_JUMP_FORCE, PLAYER_MAX_HEALTH,
    PLAYER_INVINCIBILITY_TIME, PLAYER_WIDTH, PLAYER_HEIGHT,
    PROJECTILE_COOLDOWN, ULTIMATE_CHARGE_MAX,
    IMG_PLAYER_DIR,
    IMG_PLAYER1_IDLE, IMG_PLAYER1_RUN1, IMG_PLAYER1_RUN2, IMG_PLAYER1_JUMP, IMG_PLAYER1_ATTACK,
    IMG_PLAYER2_IDLE, IMG_PLAYER2_RUN1, IMG_PLAYER2_RUN2, IMG_PLAYER2_JUMP, IMG_PLAYER2_ATTACK,
    IMG_PLAYER1_ULTIMATE, IMG_PLAYER2_ULTIMATE,
    IMG_PLAYER1_CROUCH1, IMG_PLAYER1_CROUCH2, IMG_PLAYER2_CROUCH1, IMG_PLAYER2_CROUCH2,
    CONTROLS,
)


class Player(pygame.sprite.Sprite):
    """Classe du joueur"""

    def __init__(self, character_id, x, y):
        super().__init__()
        self.character_id = character_id

        # Images
        self.images = {}
        self._load_images()

        # Sprite de base - utiliser l'image idle si disponible
        idle_img = self.images.get("idle")
        if idle_img:
            self.image = idle_img
        else:
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
        self.state = "idle"  # idle, run, jump, attack, ultimate, crouch
        self.attack_anim_timer = 0  # Timer pour garder l'animation d'attaque

        # Accroupissement
        self.is_crouching = False
        self.wants_to_stand = False
        self.normal_height = PLAYER_HEIGHT
        self.crouch_height = PLAYER_HEIGHT // 2  # Moitie de la hauteur normale

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
                "crouch1": IMG_PLAYER1_CROUCH1,
                "crouch2": IMG_PLAYER1_CROUCH2,
            }
        else:
            img_files = {
                "idle": IMG_PLAYER2_IDLE,
                "run1": IMG_PLAYER2_RUN1,
                "run2": IMG_PLAYER2_RUN2,
                "jump": IMG_PLAYER2_JUMP,
                "attack": IMG_PLAYER2_ATTACK,
                "ultimate": IMG_PLAYER2_ULTIMATE,
                "crouch1": IMG_PLAYER2_CROUCH1,
                "crouch2": IMG_PLAYER2_CROUCH2,
            }

        for key, filename in img_files.items():
            try:
                path = IMG_PLAYER_DIR / filename
                img = pygame.image.load(str(path)).convert_alpha()
                # Pour l'attaque, garder les proportions (hauteur fixe, largeur proportionnelle)
                if key == "attack":
                    original_width, original_height = img.get_size()
                    ratio = PLAYER_HEIGHT / original_height
                    new_width = int(original_width * ratio)
                    img = pygame.transform.scale(img, (new_width, PLAYER_HEIGHT))
                else:
                    img = pygame.transform.scale(img, (PLAYER_WIDTH, PLAYER_HEIGHT))
                # Flipper les images crouch car elles sont orientees dans l'autre sens
                if key in ("crouch1", "crouch2"):
                    img = pygame.transform.flip(img, True, False)
                self.images[key] = img
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
        elif self.state == "crouch":
            # Animation crouch avec 2 frames
            frame_key = "crouch1" if self.anim_frame == 0 else "crouch2"
            img = self.images.get(frame_key)
            if img:
                # Redimensionner l'image pour la hauteur accroupie
                img = pygame.transform.scale(img, (PLAYER_WIDTH, self.crouch_height))
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
            height = self.crouch_height if self.is_crouching else PLAYER_HEIGHT
            img = self._get_placeholder((PLAYER_WIDTH, height), color)

        # Flip si regarde a gauche
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        return img

    def handle_input(self, keys):
        """Gere les inputs du joueur"""
        self.velocity_x = 0

        # Accroupissement (seulement au sol)
        crouch = any(keys[k] for k in CONTROLS["crouch"])
        was_crouching = self.is_crouching

        if crouch and self.on_ground:
            self.is_crouching = True
            # Reduire la hitbox si on vient de s'accroupir
            if not was_crouching:
                bottom = self.rect.bottom
                self.rect.height = self.crouch_height
                self.rect.bottom = bottom
        else:
            # Marquer qu'on veut se relever (sera verifie dans update avec les obstacles)
            self.wants_to_stand = not crouch and was_crouching

        # Deplacement horizontal (plus lent si accroupi)
        move_left = any(keys[k] for k in CONTROLS["left"])
        move_right = any(keys[k] for k in CONTROLS["right"])

        speed = PLAYER_SPEED // 2 if self.is_crouching else PLAYER_SPEED

        if move_left:
            self.velocity_x = -speed
            self.facing_right = False
        if move_right:
            self.velocity_x = speed
            self.facing_right = True

        # Saut (pas possible si accroupi)
        jump = any(keys[k] for k in CONTROLS["jump"])
        if jump and self.on_ground and not self.is_crouching:
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

        # Si le joueur tombe pendant qu'il est accroupi, restaurer la taille
        if not self.on_ground and self.is_crouching:
            self.is_crouching = False
            bottom = self.rect.bottom
            self.rect.height = self.normal_height
            self.rect.bottom = bottom

        # Verifier si le joueur peut se relever (pas d'obstacle au-dessus)
        if self.is_crouching and self.wants_to_stand:
            # Creer un rect temporaire pour tester la hauteur normale
            test_rect = pygame.Rect(
                self.rect.x,
                self.rect.bottom - self.normal_height,
                self.rect.width,
                self.normal_height
            )
            # Verifier collision avec les plateformes
            can_stand = True
            for platform in platforms:
                if test_rect.colliderect(platform.rect):
                    can_stand = False
                    break

            if can_stand:
                # Se relever
                bottom = self.rect.bottom
                self.rect.height = self.normal_height
                self.rect.bottom = bottom
                self.is_crouching = False

        self.wants_to_stand = False

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
        elif self.is_crouching:
            self.state = "crouch"
        elif self.velocity_x != 0:
            self.state = "run"
        else:
            self.state = "idle"

        # Animation de course ou accroupi
        if self.state in ("run", "crouch"):
            self.anim_timer += dt_ms
            # Crouch anime plus lentement que la course
            anim_speed = 250 if self.state == "crouch" else 150
            if self.anim_timer >= anim_speed:
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
