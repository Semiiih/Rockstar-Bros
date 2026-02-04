"""
Rockstar Bros - Classe Pickup
Gere les collectibles (note, mediator, ampli, health)
"""

import pygame
import math
from settings import (
    YELLOW, PURPLE, GREEN, RED,
    PICKUP_WIDTH, PICKUP_HEIGHT,
    IMG_UI_DIR, IMG_NOTE, IMG_MEDIATOR, IMG_AMPLI, IMG_HEALTH,
)


class Pickup(pygame.sprite.Sprite):
    """Collectible (note, mediator, ampli, health)"""

    def __init__(self, x, y, pickup_type="note"):
        super().__init__()
        self.pickup_type = pickup_type

        # Couleur selon type
        if pickup_type == "note":
            color = YELLOW
        elif pickup_type == "mediator":
            color = PURPLE
        elif pickup_type == "health":
            color = RED
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
            "health": IMG_HEALTH,
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
        elif self.pickup_type == "health":
            # Meme style de coeur que le HUD (deux cercles + triangle)
            # Taille reduite pour le pickup (70% de la taille)
            w, h = size
            scale = 0.7
            offset_x = int(w * (1 - scale) / 2)
            offset_y = int(h * (1 - scale) / 2)
            sw, sh = int(w * scale), int(h * scale)
            # Deux cercles en haut
            radius = sw // 4
            pygame.draw.circle(surf, color, (offset_x + sw // 4 + 2, offset_y + sh // 3), radius)
            pygame.draw.circle(surf, color, (offset_x + sw * 3 // 4 - 2, offset_y + sh // 3), radius)
            # Triangle en bas
            pygame.draw.polygon(surf, color, [
                (offset_x, offset_y + sh // 3 + 2),
                (offset_x + sw, offset_y + sh // 3 + 2),
                (offset_x + sw // 2, offset_y + sh - 2)
            ])
        else:
            pygame.draw.rect(surf, color, (0, 0, size[0], size[1]), border_radius=5)
        return surf

    def update(self, dt):
        """Met a jour le pickup (animation)"""
        self.float_offset += self.float_speed * dt
        self.rect.centery = self.base_y + math.sin(self.float_offset * 3) * 5
