"""
Rockstar Bros - Scene de pause
Menu de pause avec options Resume / Quit
"""

import pygame
from scenes.base import Scene
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, GRAY, BLACK,
    STATE_GAMEPLAY, STATE_MENU, CONTROLS,
    IMG_DIR, IMG_PAUSE
)


class PauseScene(Scene):
    """Scene de pause du jeu"""

    def __init__(self, game):
        super().__init__(game)
        self.font_title = None
        self.font_menu = None
        self.font_small = None

        self.selected_option = 0
        self.options = ["Reprendre", "Menu Principal"]

        # Background pause
        self.background = None
        self.game_screenshot = None

    def enter(self, **kwargs):
        """Initialisation a l'entree dans la pause"""
        self.font_title = pygame.font.Font(None, 72)
        self.font_menu = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)

        self.selected_option = 0

        # Charger l'image de pause
        try:
            bg_path = IMG_DIR / IMG_PAUSE
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError):
            self.background = None
            # Fallback: capturer l'ecran actuel
            self.game_screenshot = self.game.screen.copy()

    def handle_event(self, event):
        """Gere les evenements du menu pause"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key in CONTROLS["confirm"]:
                self._select_option()
            elif event.key in CONTROLS["pause"]:
                # Echap pour reprendre directement
                self.game.change_scene(STATE_GAMEPLAY)

    def _select_option(self):
        """Execute l'option selectionnee"""
        if self.selected_option == 0:  # Reprendre
            self.game.change_scene(STATE_GAMEPLAY)
        elif self.selected_option == 1:  # Menu Principal
            self.game.change_scene(STATE_MENU)

    def update(self, dt):
        """Mise a jour (rien a faire en pause)"""
        pass

    def draw(self, screen):
        """Dessine le menu pause"""
        # Background
        if self.background:
            screen.blit(self.background, (0, 0))
        elif self.game_screenshot:
            # Fallback: screenshot du jeu assombri
            screen.blit(self.game_screenshot, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

        # Cadre central
        frame_width = 400
        frame_height = 300
        frame_x = (WIDTH - frame_width) // 2
        frame_y = (HEIGHT - frame_height) // 2

        pygame.draw.rect(screen, (40, 40, 50),
                        (frame_x, frame_y, frame_width, frame_height),
                        border_radius=15)
        pygame.draw.rect(screen, WHITE,
                        (frame_x, frame_y, frame_width, frame_height),
                        3, border_radius=15)

        # Titre
        title_text = self.font_title.render("PAUSE", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, frame_y + 60))
        screen.blit(title_text, title_rect)

        # Options
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                color = YELLOW
                prefix = "> "
            else:
                color = WHITE
                prefix = "  "

            text = self.font_menu.render(prefix + option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, frame_y + 140 + i * 60))
            screen.blit(text, rect)

        # Instructions
        instructions = self.font_small.render(
            "Fleches + Entree | Echap pour reprendre",
            True, GRAY
        )
        inst_rect = instructions.get_rect(center=(WIDTH // 2, frame_y + frame_height - 30))
        screen.blit(instructions, inst_rect)
