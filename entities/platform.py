"""
Rockstar Bros - Classe Platform
Gere les plateformes et le sol
"""

import pygame
from settings import (
    IMG_PLATFORMS_DIR, IMG_PLATFORM, IMG_PLATFORM_SMALL, IMG_GROUND,
)


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
