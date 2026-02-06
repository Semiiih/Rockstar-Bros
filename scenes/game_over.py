"""
Rockstar Bros - Scene de Game Over
Affiche le score et propose de rejouer ou retourner au menu
"""

import pygame
from scenes.base import Scene
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, RED, GRAY,
    STATE_GAMEPLAY, STATE_MENU, CONTROLS,
    IMG_DIR, IMG_GAMEOVER,
    FONT_METAL_MANIA, FONT_ROAD_RAGE,
    SND_DIR, SND_BOSS_LAUGH_1, SND_BOSS_LAUGH_2, SND_BOSS_LAUGH_3, SND_MENU_CLICK,
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
        self.background = None

        # Son de navigation
        self.click_sfx = None
        try:
            self.click_sfx = pygame.mixer.Sound(str(SND_DIR / SND_MENU_CLICK))
            self.click_sfx.set_volume(0.5)
        except (pygame.error, FileNotFoundError):
            pass

    def enter(self, **kwargs):
        """Initialisation a l'entree dans le game over"""
        # Charger les polices - Metal Mania pour titres, Road Rage pour texte
        try:
            self.font_title = pygame.font.Font(str(FONT_METAL_MANIA), 96)
            self.font_menu = pygame.font.Font(str(FONT_ROAD_RAGE), 36)
            self.font_score = pygame.font.Font(str(FONT_METAL_MANIA), 64)
            self.font_small = pygame.font.Font(str(FONT_ROAD_RAGE), 24)
        except (pygame.error, FileNotFoundError):
            self.font_title = pygame.font.Font(None, 96)
            self.font_menu = pygame.font.Font(None, 36)
            self.font_score = pygame.font.Font(None, 64)
            self.font_small = pygame.font.Font(None, 24)

        self.selected_option = 0
        self.final_score = self.game.game_data.get("score", 0)

        # Jouer le son de defaite (rire du boss) seulement si pas mort par chute
        # Chaque niveau a son propre rire de boss
        death_by_fall = self.game.game_data.get("death_by_fall", False)
        if not death_by_fall:
            try:
                # Choisir le son de rire selon le niveau
                current_level = self.game.game_data.get("selected_level", 1)
                if current_level == 1:
                    laugh_sound = SND_BOSS_LAUGH_1
                elif current_level == 2:
                    laugh_sound = SND_BOSS_LAUGH_2
                else:
                    laugh_sound = SND_BOSS_LAUGH_3

                music_path = str(SND_DIR / laugh_sound)
                try:
                    pygame.mixer.music.load(music_path)
                except pygame.error:
                    pygame.mixer.music.load(music_path, namehint=".mp3")
                pygame.mixer.music.set_volume(0.6)
                pygame.mixer.music.play()  # Jouer une seule fois (pas en boucle)
            except (pygame.error, FileNotFoundError):
                pass

        # Charger l'image de game over
        try:
            bg_path = IMG_DIR / IMG_GAMEOVER
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError):
            self.background = None

    def handle_event(self, event):
        """Gere les evenements"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
                if self.click_sfx:
                    self.click_sfx.play()
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                if self.click_sfx:
                    self.click_sfx.play()
            elif event.key in CONTROLS["confirm"]:
                self._select_option()

    def _select_option(self):
        """Execute l'option selectionnee"""
        if self.selected_option == 0:  # Rejouer
            # Garder le niveau ET le stage actuel (checkpoint)
            current_level = self.game.game_data.get("selected_level", 1)
            current_stage = self.game.game_data.get("current_stage", 1)
            # Garder le score, juste reset les vies et l'ultime
            self.game.game_data["lives"] = 3
            self.game.game_data["ultimate_charge"] = 0
            self.game.game_data["selected_level"] = current_level
            self.game.game_data["current_stage"] = current_stage
            self.game.change_scene(STATE_GAMEPLAY)
        elif self.selected_option == 1:  # Menu Principal
            self.game.change_scene(STATE_MENU)

    def update(self, dt):
        """Mise a jour"""
        pass

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
        """Dessine l'ecran de game over"""
        # Background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            # Fond rouge sombre si pas d'image
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
            color = YELLOW if i == self.selected_option else WHITE
            text = self.font_menu.render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, 450 + i * 60))
            screen.blit(text, rect)

            # Fleche a gauche de l'option selectionnee
            if i == self.selected_option:
                self._draw_arrow(screen, rect.left - 25, rect.centery)

        # Instructions
        instructions = self.font_small.render(
            "Fleches pour naviguer - Entree pour valider",
            True, GRAY
        )
        inst_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(instructions, inst_rect)
