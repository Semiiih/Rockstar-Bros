"""
Rockstar Bros - Scene de Game Over
Affiche le score et propose de rejouer ou retourner au menu
"""

import pygame
from scenes.base import Scene
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, RED, GRAY,
    STATE_GAMEPLAY, STATE_MENU, CONTROLS
)


class GameOverScene(Scene):
    """Scene de game over"""

    def __init__(self, game):
        super().__init__(game)
        self.font_title = None
        self.font_menu = None
        self.font_score = None
        self.font_small = None

        self.selected_option = 0
        self.options = ["Rejouer", "Menu Principal"]

        self.final_score = 0

    def enter(self, **kwargs):
        """Initialisation a l'entree dans le game over"""
        self.font_title = pygame.font.Font(None, 96)
        self.font_menu = pygame.font.Font(None, 48)
        self.font_score = pygame.font.Font(None, 64)
        self.font_small = pygame.font.Font(None, 32)

        self.selected_option = 0
        self.final_score = self.game.game_data.get("score", 0)

    def handle_event(self, event):
        """Gere les evenements"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key in CONTROLS["confirm"]:
                self._select_option()

    def _select_option(self):
        """Execute l'option selectionnee"""
        if self.selected_option == 0:  # Rejouer
            self.game.reset_game()
            self.game.change_scene(STATE_GAMEPLAY)
        elif self.selected_option == 1:  # Menu Principal
            self.game.change_scene(STATE_MENU)

    def update(self, dt):
        """Mise a jour"""
        pass

    def draw(self, screen):
        """Dessine l'ecran de game over"""
        # Fond rouge sombre
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(40 + ratio * 20)
            g = int(10 + ratio * 10)
            b = int(10 + ratio * 10)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

        # Titre GAME OVER
        title_text = self.font_title.render("GAME OVER", True, RED)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Score
        score_label = self.font_menu.render("Score Final", True, WHITE)
        score_label_rect = score_label.get_rect(center=(WIDTH // 2, 260))
        screen.blit(score_label, score_label_rect)

        score_text = self.font_score.render(str(self.final_score), True, YELLOW)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 320))
        screen.blit(score_text, score_rect)

        # Options
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = YELLOW
                prefix = "> "
            else:
                color = WHITE
                prefix = "  "

            text = self.font_menu.render(prefix + option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, 450 + i * 60))
            screen.blit(text, rect)

        # Instructions
        instructions = self.font_small.render(
            "Fleches pour naviguer - Entree pour valider",
            True, GRAY
        )
        inst_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(instructions, inst_rect)
