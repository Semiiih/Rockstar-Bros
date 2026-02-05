"""
Rockstar Bros - Mystery Block Easter Egg
A Mario-style block that spawns a star when hit from below.
"""

import pygame
import math
from settings import (
    YELLOW, ORANGE, GRAY, DARK_GRAY,
    MYSTERY_BLOCK_SIZE,
    IMG_UI_DIR, IMG_MYSTERY_BLOCK,
)


class MysteryBlock(pygame.sprite.Sprite):
    """
    Mystery Block - Mario-style Easter Egg entity.
    Visible from the start, spawns a star when hit from below.
    """

    def __init__(self, x, y):
        super().__init__()
        self.width = MYSTERY_BLOCK_SIZE
        self.height = MYSTERY_BLOCK_SIZE

        # Load images
        self.active_image = self._load_image()
        self.used_image = self._create_used_image()
        self.image = self.active_image
        self.rect = self.image.get_rect(topleft=(x, y))

        # State
        self.activated = False
        self.is_ground = False  # Required for platform compatibility

        # Bump animation
        self.bump_offset = 0
        self.is_bumping = False

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

    def _create_used_image(self):
        """Create the 'used' block image (after star is spawned)"""
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        # Darker, empty block
        pygame.draw.rect(surf, DARK_GRAY, (0, 0, self.width, self.height))
        pygame.draw.rect(surf, GRAY, (0, 0, self.width, self.height), 3)
        pygame.draw.rect(surf, (80, 80, 80), (4, 4, self.width - 8, self.height - 8), 2)
        return surf

    def update(self, dt):
        """Update bump animation"""
        if self.is_bumping:
            self.bump_offset -= 0.5
            if self.bump_offset <= -8:
                self.is_bumping = False
            elif self.bump_offset <= -4 and not self.is_bumping:
                self.bump_offset = 0

        # Return to normal position
        if not self.is_bumping and self.bump_offset < 0:
            self.bump_offset += 1
            if self.bump_offset > 0:
                self.bump_offset = 0

    def check_head_collision(self, player):
        """
        Check if player hit the block from below with their head.
        Returns True if this is a valid activation hit.
        """
        if self.activated:
            return False

        # Player must be moving upward (jumping)
        if player.velocity_y >= 0:
            return False

        # Simple collision check - if player collides with block while moving up
        if self.rect.colliderect(player.rect):
            # Player's head is hitting the block
            return True

        return False

    def handle_collision(self, player):
        """
        Handle solid collision with player.
        Called from gameplay collision system.
        Returns True if collision was handled (player should stop).
        """
        if not self.rect.colliderect(player.rect):
            return False

        # Determine collision direction
        # Player coming from below (head bump)
        if player.velocity_y < 0 and player.rect.top < self.rect.bottom:
            player.rect.top = self.rect.bottom
            player.velocity_y = 0
            return True

        # Player coming from above (landing on top)
        if player.velocity_y > 0 and player.rect.bottom > self.rect.top:
            player.rect.bottom = self.rect.top
            player.velocity_y = 0
            return True

        # Side collision from left
        if player.velocity_x > 0 and player.rect.right > self.rect.left:
            player.rect.right = self.rect.left
            return True

        # Side collision from right
        if player.velocity_x < 0 and player.rect.left < self.rect.right:
            player.rect.left = self.rect.right
            return True

        return False

    def activate(self):
        """Activate the block - change to used state and start bump animation"""
        if self.activated:
            return False
        self.activated = True
        self.image = self.used_image
        self.is_bumping = True
        self.bump_offset = 0
        return True

    def draw(self, screen, camera_x):
        """Draw the block (always visible)"""
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y + self.bump_offset

        screen.blit(self.image, (draw_x, draw_y))
