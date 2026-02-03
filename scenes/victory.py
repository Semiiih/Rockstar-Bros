"""
Rockstar Bros - Scene de Victoire
Affiche le score final et felicite le joueur
"""

import pygame
import math
from scenes.base import Scene
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, GREEN, PURPLE, GRAY,
    STATE_MENU, CONTROLS,
    IMG_DIR, IMG_WIN,
    FONT_METAL_MANIA, FONT_ROAD_RAGE
)


class VictoryScene(Scene):
    """Scene de victoire"""

    def __init__(self, game):
        super().__init__(game)
        self.font_title = None
        self.font_menu = None
        self.font_score = None
        self.font_small = None

        self.selected_option = 0
        self.options = ["Menu Principal"]

        self.final_score = 0
        self.animation_timer = 0
        self.background = None

    def enter(self, **kwargs):
        """Initialisation a l'entree dans la victoire"""
        # Charger les polices - Metal Mania pour titres, Road Rage pour texte
        try:
            self.font_title = pygame.font.Font(str(FONT_METAL_MANIA), 96)
            self.font_menu = pygame.font.Font(str(FONT_ROAD_RAGE), 36)
            self.font_score = pygame.font.Font(str(FONT_METAL_MANIA), 72)
            self.font_small = pygame.font.Font(str(FONT_ROAD_RAGE), 24)
        except (pygame.error, FileNotFoundError):
            self.font_title = pygame.font.Font(None, 96)
            self.font_menu = pygame.font.Font(None, 36)
            self.font_score = pygame.font.Font(None, 72)
            self.font_small = pygame.font.Font(None, 24)

        self.selected_option = 0
        self.final_score = self.game.game_data.get("score", 0)
        self.animation_timer = 0

        # Charger l'image de victoire
        try:
            bg_path = IMG_DIR / IMG_WIN
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError):
            self.background = None

    def handle_event(self, event):
        """Gere les evenements"""
        if event.type == pygame.KEYDOWN:
            if event.key in CONTROLS["confirm"]:
                self.game.change_scene(STATE_MENU)

    def update(self, dt):
        """Mise a jour des animations"""
        self.animation_timer += dt

    def _draw_arrow(self, screen, x, y, color=YELLOW):
        """Dessine une fleche de selection (triangle)"""
        arrow_size = 12
        points = [
            (x, y - arrow_size // 2),
            (x, y + arrow_size // 2),
            (x + arrow_size, y)
        ]
        pygame.draw.polygon(screen, color, points)

    def draw(self, screen):
        """Dessine l'ecran de victoire"""
        # Background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            # Fallback: fond avec effet de celebration
            self._draw_celebration_bg(screen)

        # Titre VICTOIRE avec effet de pulsation
        pulse = 1.0 + math.sin(self.animation_timer * 5) * 0.1
        title_font_size = int(96 * pulse)
        try:
            title_font = pygame.font.Font(str(FONT_METAL_MANIA), title_font_size)
        except (pygame.error, FileNotFoundError):
            title_font = pygame.font.Font(None, title_font_size)

        title_text = title_font.render("VICTOIRE!", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Sous-titre
        subtitle = self.font_menu.render("Tu as vaincu le Boss!", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, 230))
        screen.blit(subtitle, subtitle_rect)

        # Score
        score_label = self.font_menu.render("Score Final", True, WHITE)
        score_label_rect = score_label.get_rect(center=(WIDTH // 2, 320))
        screen.blit(score_label, score_label_rect)

        score_text = self.font_score.render(str(self.final_score), True, YELLOW)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 390))
        screen.blit(score_text, score_rect)

        # Message de felicitations
        congrats_messages = [
            "Tu es une vraie Rockstar!",
            "La scene t'appartient!",
            "Le public t'acclame!",
        ]
        msg_index = int(self.animation_timer) % len(congrats_messages)
        congrats = self.font_menu.render(congrats_messages[msg_index], True, PURPLE)
        congrats_rect = congrats.get_rect(center=(WIDTH // 2, 480))
        screen.blit(congrats, congrats_rect)

        # Option retour menu
        text = self.font_menu.render("Menu Principal", True, YELLOW)
        rect = text.get_rect(center=(WIDTH // 2, 560))
        screen.blit(text, rect)
        # Fleche a gauche
        self._draw_arrow(screen, rect.left - 25, rect.centery)

        # Instructions
        instructions = self.font_small.render(
            "Appuie sur Entree pour continuer",
            True, GRAY
        )
        inst_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(instructions, inst_rect)

    def _draw_celebration_bg(self, screen):
        """Dessine un fond festif"""
        # Gradient vert/violet
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(20 + ratio * 40)
            g = int(50 + ratio * 30)
            b = int(30 + ratio * 50)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        # Particules / etoiles
        for i in range(20):
            x = (int(self.animation_timer * 50 + i * 100) % (WIDTH + 100)) - 50
            y = (i * 47) % HEIGHT
            size = 3 + (i % 3)

            # Couleur alternee
            if i % 3 == 0:
                color = YELLOW
            elif i % 3 == 1:
                color = PURPLE
            else:
                color = GREEN

            pygame.draw.circle(screen, color, (x, y), size)

        # Rayons de lumiere depuis le haut
        for i in range(5):
            angle = math.sin(self.animation_timer + i) * 0.3
            start_x = WIDTH // 2 + i * 100 - 200
            end_x = start_x + int(math.tan(angle) * HEIGHT)

            pygame.draw.line(
                screen,
                (255, 255, 200, 50),
                (start_x, 0),
                (end_x, HEIGHT),
                3
            )
