"""
Rockstar Bros - Classe Pickup
Gere les collectibles (note, mediator, ampli)
"""

import pygame
import math
from settings import (
    YELLOW, PURPLE, GREEN,
    PICKUP_WIDTH, PICKUP_HEIGHT,
    IMG_UI_DIR, IMG_NOTE, IMG_MEDIATOR, IMG_AMPLI,
)


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
