"""
Rockstar Bros - Mystery Block Easter Egg
A Mario-style hidden block that spawns a star when hit from below.
"""

import pygame
import math
from settings import (
    YELLOW, ORANGE, WHITE,
    MYSTERY_BLOCK_SIZE,
    IMG_UI_DIR, IMG_MYSTERY_BLOCK,
)


class MysteryBlock(pygame.sprite.Sprite):
    """
    Mystery Block - Mario-style Easter Egg entity.
    INVISIBLE until hit from below, then appears and spawns a star.
    A floating arrow hints at its location.
    """

    def __init__(self, x, y):
        super().__init__()
        self.width = MYSTERY_BLOCK_SIZE
        self.height = MYSTERY_BLOCK_SIZE

        # Load the visible image (shown after activation)
        self.visible_image = self._load_image()

        # Create invisible placeholder for collision (transparent)
        self.invisible_image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.invisible_image.fill((0, 0, 0, 0))  # Fully transparent

        # Start invisible
        self.image = self.invisible_image
        self.rect = self.image.get_rect(topleft=(x, y))

        # State
        self.activated = False
        self.visible = False
        self.is_ground = False  # Required for platform compatibility

        # Arrow animation (20px above the block)
        self.arrow_offset = 0
        self.arrow_bob_speed = 4
        self.arrow_distance = 20  # Distance above the block

    def _load_image(self):
        """Load the mystery block sprite or create placeholder"""
        try:
            path = IMG_UI_DIR / IMG_MYSTERY_BLOCK
            img = pygame.image.load(str(path)).convert_alpha()
            return pygame.transform.scale(img, (self.width, self.height))
        except (pygame.error, FileNotFoundError):
            # Create placeholder - golden block with question mark (Mario style)
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            # Block base
            pygame.draw.rect(surf, ORANGE, (0, 0, self.width, self.height))
            # Dark border
            pygame.draw.rect(surf, (139, 69, 19), (0, 0, self.width, self.height), 3)
            # Inner highlight
            pygame.draw.rect(surf, YELLOW, (4, 4, self.width - 8, self.height - 8), 2)
            # Question mark
            font = pygame.font.Font(None, 40)
            text = font.render("?", True, (139, 69, 19))
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            surf.blit(text, text_rect)
            return surf

    def update(self, dt):
        """Update arrow bobbing animation"""
        self.arrow_offset += self.arrow_bob_speed * dt

    def activate(self):
        """Activate the block - make it visible"""
        if self.activated:
            return False
        self.activated = True
        self.visible = True
        self.image = self.visible_image
        return True

    def draw(self, screen, camera_x):
        """Draw the block and arrow indicator"""
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y

        # Draw the block only if visible (after activation)
        if self.visible:
            screen.blit(self.image, (draw_x, draw_y))

        # Draw the arrow indicator if NOT activated
        if not self.activated:
            self._draw_arrow(screen, camera_x)

    def _draw_arrow(self, screen, camera_x):
        """Draw a bobbing arrow pointing down at the hidden block"""
        # Arrow position: centered above the block, 20px gap + bobbing
        arrow_x = self.rect.centerx - camera_x
        bob = math.sin(self.arrow_offset * 3) * 6  # Bob up and down 6px
        arrow_y = self.rect.top - self.arrow_distance - 15 + bob  # 15 is arrow height

        # Arrow size
        arrow_width = 24
        arrow_height = 20

        # Draw arrow pointing DOWN (triangle)
        points = [
            (arrow_x, arrow_y + arrow_height),                    # Bottom point (pointing down)
            (arrow_x - arrow_width // 2, arrow_y),                # Top left
            (arrow_x + arrow_width // 2, arrow_y),                # Top right
        ]

        # Glow effect
        glow_alpha = int(150 + math.sin(self.arrow_offset * 5) * 50)
        glow_surf = pygame.Surface((arrow_width + 16, arrow_height + 16), pygame.SRCALPHA)
        glow_points = [
            ((arrow_width + 16) // 2, arrow_height + 8),
            ((arrow_width + 16) // 2 - arrow_width // 2 - 4, 4),
            ((arrow_width + 16) // 2 + arrow_width // 2 + 4, 4),
        ]
        pygame.draw.polygon(glow_surf, (255, 255, 0, glow_alpha // 2), glow_points)
        screen.blit(glow_surf, (arrow_x - (arrow_width + 16) // 2, arrow_y - 4))

        # Main arrow (yellow with orange outline)
        pygame.draw.polygon(screen, YELLOW, points)
        pygame.draw.polygon(screen, ORANGE, points, 3)

        # White highlight
        highlight_points = [
            (arrow_x, arrow_y + arrow_height - 6),
            (arrow_x - arrow_width // 4, arrow_y + 4),
            (arrow_x + arrow_width // 4, arrow_y + 4),
        ]
        pygame.draw.polygon(screen, WHITE, highlight_points)
