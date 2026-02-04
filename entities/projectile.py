"""
Rockstar Bros - Classes Projectiles
Gere les projectiles du joueur et du boss
"""

import pygame
import math
from settings import (
    WIDTH, HEIGHT, YELLOW, RED, ORANGE, PURPLE,
    PROJECTILE_SPEED, PROJECTILE_WIDTH, PROJECTILE_HEIGHT, PROJECTILE_DAMAGE,
    BOSS_PROJECTILE_SPEED, BOSS_DAMAGE, BOSS_SHOCKWAVE_DAMAGE,
    BOSS2_PROJECTILE_SPEED, BOSS2_DAMAGE, BOSS2_SHOCKWAVE_DAMAGE,
    BOSS3_PROJECTILE_SPEED, BOSS3_DAMAGE, BOSS3_SHOCKWAVE_DAMAGE,
    RIVAL_PROJECTILE_SPEED, RIVAL_PROJECTILE_DAMAGE,
    IMG_FX_DIR, IMG_PROJECTILE, IMG_SHOCKWAVE, IMG_RIVAL_PROJECTILE,
    IMG_ENEMIES_DIR, IMG_BOSS_PROJECTILE, IMG_BOSS2_PROJECTILE, IMG_BOSS3_PROJECTILE,
)


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
        """Charge l'image du projectile avec proportions respectees"""
        try:
            path = IMG_FX_DIR / IMG_PROJECTILE
            img = pygame.image.load(str(path)).convert_alpha()
            # Garder les proportions (hauteur fixe, largeur proportionnelle)
            original_width, original_height = img.get_size()
            ratio = PROJECTILE_HEIGHT / original_height
            new_width = int(original_width * ratio)
            self.image = pygame.transform.scale(img, (new_width, PROJECTILE_HEIGHT))
        except (pygame.error, FileNotFoundError):
            pass

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.ellipse(surf, color, (0, 0, size[0], size[1]))
        return surf

    def update(self, dt, camera_x=0):
        """Met a jour le projectile"""
        self.rect.x += self.speed * self.direction

        # Supprime si hors ecran visible (relatif a la camera)
        screen_x = self.rect.x - camera_x
        if screen_x < -200 or screen_x > WIDTH + 200:
            self.kill()


class BossProjectile(pygame.sprite.Sprite):
    """Projectile du boss - supporte les 3 types de boss"""

    def __init__(self, x, y, target_x, target_y, boss_type="boss"):
        super().__init__()
        self.boss_type = boss_type
        self.projectile_height = 40  # Hauteur cible du projectile

        # Config selon le type de boss
        if boss_type == "boss2":
            self.speed = BOSS2_PROJECTILE_SPEED
            self.damage = BOSS2_SHOCKWAVE_DAMAGE
            self.color = PURPLE
            self.img_file = IMG_BOSS2_PROJECTILE
        elif boss_type == "boss3":
            self.speed = BOSS3_PROJECTILE_SPEED
            self.damage = BOSS3_SHOCKWAVE_DAMAGE
            self.color = ORANGE
            self.img_file = IMG_BOSS3_PROJECTILE
            self.projectile_height = 50  # Plus gros pour boss3
        else:  # boss1
            self.speed = BOSS_PROJECTILE_SPEED
            self.damage = BOSS_SHOCKWAVE_DAMAGE
            self.color = RED
            self.img_file = IMG_BOSS_PROJECTILE

        self.image = self._get_placeholder((self.projectile_height, self.projectile_height), self.color)
        self._load_image()
        self.rect = self.image.get_rect(center=(x, y))

        # Calcul direction vers la cible
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            self.vel_x = (dx / dist) * self.speed
            self.vel_y = (dy / dist) * self.speed
        else:
            self.vel_x = -self.speed
            self.vel_y = 0

    def _load_image(self):
        """Charge l'image du projectile du boss"""
        try:
            path = IMG_ENEMIES_DIR / self.img_file
            img = pygame.image.load(str(path)).convert_alpha()
            # Garder les proportions (hauteur fixe, largeur proportionnelle)
            original_width, original_height = img.get_size()
            ratio = self.projectile_height / original_height
            new_width = int(original_width * ratio)
            self.image = pygame.transform.scale(img, (new_width, self.projectile_height))
        except (pygame.error, FileNotFoundError):
            pass

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


class RivalProjectile(pygame.sprite.Sprite):
    """Projectile des rivals tireurs"""

    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.projectile_height = 30  # Hauteur cible du projectile
        self.image = self._get_placeholder((30, 30), ORANGE)
        self._load_image()
        self.rect = self.image.get_rect(center=(x, y))

        # Calcul direction vers la cible
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            self.vel_x = (dx / dist) * RIVAL_PROJECTILE_SPEED
            self.vel_y = (dy / dist) * RIVAL_PROJECTILE_SPEED
        else:
            self.vel_x = -RIVAL_PROJECTILE_SPEED
            self.vel_y = 0

        self.damage = RIVAL_PROJECTILE_DAMAGE

    def _load_image(self):
        """Charge l'image projectile rival avec proportions respectees"""
        try:
            path = IMG_FX_DIR / IMG_RIVAL_PROJECTILE
            img = pygame.image.load(str(path)).convert_alpha()
            # Garder les proportions (hauteur fixe, largeur proportionnelle)
            original_width, original_height = img.get_size()
            ratio = self.projectile_height / original_height
            new_width = int(original_width * ratio)
            self.image = pygame.transform.scale(img, (new_width, self.projectile_height))
        except (pygame.error, FileNotFoundError):
            pass

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
