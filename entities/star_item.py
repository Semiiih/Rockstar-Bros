"""
Rockstar Bros - Star Item (Easter Egg)
A collectible star that grants temporary invincibility and contact-kill powers.
"""

import pygame
import math
from settings import (
    YELLOW, ORANGE, WHITE,
    STAR_SIZE, STAR_SPAWN_VELOCITY,
    GRAVITY, MAX_FALL_SPEED,
    IMG_UI_DIR, IMG_STAR,
)


class StarItem(pygame.sprite.Sprite):
    """
    Star Item - Easter Egg collectible.
    Spawns from mystery block, moves right and bounces.
    Grants STAR_MODE when collected.
    """

    def __init__(self, x, y):
        super().__init__()
        self.width = STAR_SIZE
        self.height = STAR_SIZE

        # Load or create image
        self.image = self._load_image()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))

        # Physics - star pops up then moves right
        self.velocity_x = 3  # Move right
        self.velocity_y = STAR_SPAWN_VELOCITY  # Start moving upward (pop out of block)
        self.on_ground = False

        # Animation
        self.rotation = 0
        self.sparkle_timer = 0

    def _load_image(self):
        """Load star sprite or create placeholder"""
        try:
            path = IMG_UI_DIR / IMG_STAR
            img = pygame.image.load(str(path)).convert_alpha()
            return pygame.transform.scale(img, (self.width, self.height))
        except (pygame.error, FileNotFoundError):
            # Create placeholder star
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self._draw_star_shape(surf, self.width // 2, self.height // 2, self.width // 2 - 4, YELLOW, ORANGE)
            return surf

    def _draw_star_shape(self, surface, cx, cy, size, fill_color, outline_color):
        """Draw a 5-pointed star shape"""
        import math as m
        points = []
        for i in range(5):
            # Outer point
            angle = m.radians(-90 + i * 72)
            points.append((cx + size * m.cos(angle), cy + size * m.sin(angle)))
            # Inner point
            angle = m.radians(-90 + i * 72 + 36)
            inner_size = size * 0.4
            points.append((cx + inner_size * m.cos(angle), cy + inner_size * m.sin(angle)))

        pygame.draw.polygon(surface, fill_color, points)
        pygame.draw.polygon(surface, outline_color, points, 2)

    def update(self, dt, platforms=None):
        """Update star physics and animation"""
        # Apply gravity
        self.velocity_y += GRAVITY * 0.6
        if self.velocity_y > MAX_FALL_SPEED * 0.6:
            self.velocity_y = MAX_FALL_SPEED * 0.6

        # Move horizontally (always moving right)
        self.rect.x += self.velocity_x

        # Move vertically
        self.rect.y += self.velocity_y

        # Check platform collision - bounce!
        if platforms:
            for platform in platforms:
                if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = -10  # Bounce up!

        # Rotation animation (spin effect)
        self.rotation += 180 * dt  # Fast spin
        if self.rotation >= 360:
            self.rotation -= 360

        # Sparkle effect
        self.sparkle_timer += dt

        # Rotate image for visual effect
        self._update_rotated_image()

    def _update_rotated_image(self):
        """Update the rotated image for spinning effect"""
        # Scale X based on rotation to create a 3D spinning effect
        scale_x = abs(math.cos(math.radians(self.rotation)))
        if scale_x < 0.2:
            scale_x = 0.2

        new_width = int(self.width * scale_x)
        if new_width < 4:
            new_width = 4

        self.image = pygame.transform.scale(self.original_image, (new_width, self.height))
        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)

    def draw(self, screen, camera_x):
        """Draw the star with sparkle effects"""
        draw_x = self.rect.x - camera_x
        draw_y = self.rect.y

        # Draw sparkles around the star
        self._draw_sparkles(screen, self.rect.centerx - camera_x, self.rect.centery)

        # Draw the star
        screen.blit(self.image, (draw_x, draw_y))

    def _draw_sparkles(self, screen, cx, cy):
        """Draw animated sparkles around the star"""
        sparkle_count = 4
        for i in range(sparkle_count):
            angle = self.sparkle_timer * 2 + i * (360 / sparkle_count)
            distance = 20 + math.sin(self.sparkle_timer * 4 + i) * 5
            x = cx + math.cos(math.radians(angle)) * distance
            y = cy + math.sin(math.radians(angle)) * distance

            # Pulsing size
            size = 2 + math.sin(self.sparkle_timer * 6 + i * 2) * 1

            # Sparkle color alternates
            color = YELLOW if i % 2 == 0 else WHITE
            pygame.draw.circle(screen, color, (int(x), int(y)), int(size))
