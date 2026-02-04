"""
Rockstar Bros - Scene de Victoire
Affiche la carte de selection de niveau avec le niveau complete
"""

import pygame
import math
from scenes.base import Scene
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, GREEN, PURPLE, GRAY, BLACK, ORANGE, BLUE,
    STATE_MENU, STATE_LEVEL_SELECT, CONTROLS, BG_COLOR, DARK_GRAY,
    FONT_METAL_MANIA, FONT_ROAD_RAGE
)
from level_loader import get_loader


class LevelNodeVictory:
    """Represente un noeud de niveau sur la carte de victoire"""

    def __init__(self, level_data, x, y, unlocked=False, stars=0, is_completed=False):
        self.level_data = level_data
        self.level_id = level_data['id']
        self.x = x
        self.y = y
        self.unlocked = unlocked
        self.stars = stars
        self.is_completed = is_completed  # Le niveau qu'on vient de completer
        self.radius = 50
        self.pulse_timer = 0

    def update(self, dt):
        """Met a jour l'animation du noeud"""
        if self.unlocked:
            self.pulse_timer += dt * 2
            if self.pulse_timer > math.pi * 2:
                self.pulse_timer -= math.pi * 2

    def draw(self, screen, font_large, font_small):
        """Dessine le noeud de niveau"""
        pulse = 0
        if self.unlocked:
            pulse = int(math.sin(self.pulse_timer) * 5)

        # Couleur selon l'etat
        if not self.unlocked:
            color = DARK_GRAY
            border_color = GRAY
        elif self.is_completed:
            # Niveau complete - effet special
            color = YELLOW
            border_color = ORANGE
        else:
            difficulty = self.level_data.get('difficulty', 'easy')
            if difficulty == 'easy':
                color = GREEN
            elif difficulty == 'medium':
                color = BLUE
            else:
                color = PURPLE
            border_color = WHITE

        # Cercle principal avec ombre
        shadow_offset = 4
        pygame.draw.circle(screen, BLACK, (self.x + shadow_offset, self.y + shadow_offset),
                          self.radius + pulse + 3)
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius + pulse)
        pygame.draw.circle(screen, border_color, (self.x, self.y), self.radius + pulse, 4)

        # Numero du niveau au centre
        level_text = font_large.render(str(self.level_id), True, WHITE if self.unlocked else GRAY)
        text_rect = level_text.get_rect(center=(self.x, self.y - 5))
        screen.blit(level_text, text_rect)

        # Nom du niveau en dessous
        if self.unlocked:
            name_text = font_small.render(self.level_data['name'], True, WHITE)
            name_rect = name_text.get_rect(center=(self.x, self.y + self.radius + 25))
            screen.blit(name_text, name_rect)

        # Etoiles gagnees
        if self.unlocked and self.stars > 0:
            star_size = 15
            star_spacing = 18
            total_width = self.stars * star_spacing
            start_x = self.x - total_width // 2

            for i in range(self.stars):
                star_x = start_x + i * star_spacing + star_spacing // 2
                star_y = self.y + self.radius + 45
                self._draw_star(screen, star_x, star_y, star_size, YELLOW)

        # Icone cadenas si verrouille
        if not self.unlocked:
            self._draw_lock(screen, self.x, self.y)

    def _draw_star(self, screen, x, y, size, color):
        """Dessine une etoile"""
        points = []
        for i in range(5):
            angle = math.pi * 2 * i / 5 - math.pi / 2
            outer_x = x + math.cos(angle) * size
            outer_y = y + math.sin(angle) * size
            points.append((outer_x, outer_y))

            angle = math.pi * 2 * (i + 0.5) / 5 - math.pi / 2
            inner_x = x + math.cos(angle) * (size * 0.4)
            inner_y = y + math.sin(angle) * (size * 0.4)
            points.append((inner_x, inner_y))

        pygame.draw.polygon(screen, color, points)
        pygame.draw.polygon(screen, BLACK, points, 2)

    def _draw_lock(self, screen, x, y):
        """Dessine un cadenas"""
        lock_rect = pygame.Rect(x - 12, y - 5, 24, 20)
        pygame.draw.rect(screen, GRAY, lock_rect, border_radius=3)
        pygame.draw.rect(screen, BLACK, lock_rect, 2, border_radius=3)

        arc_rect = pygame.Rect(x - 10, y - 20, 20, 20)
        pygame.draw.arc(screen, GRAY, arc_rect, 0, math.pi, 3)


class VictoryScene(Scene):
    """Scene de victoire avec carte de selection de niveau"""

    def __init__(self, game):
        super().__init__(game)
        self.font_title = None
        self.font_menu = None
        self.font_score = None
        self.font_small = None
        self.font_large = None
        self.font_medium = None

        self.selected_option = 0
        self.options = ["Continuer", "Menu Principal"]

        self.final_score = 0
        self.animation_timer = 0

        # Loader de niveaux
        self.loader = get_loader()

        # Nodes de niveaux
        self.nodes = []
        self.node_positions = [
            (300, 450),
            (640, 300),
            (980, 450),
        ]

        # Animation de fond
        self.bg_offset = 0

        # Niveau complete
        self.completed_level_id = 1

    def enter(self, **kwargs):
        """Initialisation a l'entree dans la victoire"""
        try:
            self.font_title = pygame.font.Font(str(FONT_METAL_MANIA), 72)
            self.font_menu = pygame.font.Font(str(FONT_ROAD_RAGE), 36)
            self.font_score = pygame.font.Font(str(FONT_METAL_MANIA), 48)
            self.font_small = pygame.font.Font(str(FONT_ROAD_RAGE), 24)
            self.font_large = pygame.font.Font(str(FONT_METAL_MANIA), 48)
            self.font_medium = pygame.font.Font(str(FONT_METAL_MANIA), 28)
        except (pygame.error, FileNotFoundError):
            self.font_title = pygame.font.Font(None, 72)
            self.font_menu = pygame.font.Font(None, 36)
            self.font_score = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 24)
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 28)

        self.selected_option = 0
        self.final_score = self.game.game_data.get("score", 0)
        self.animation_timer = 0

        # Recuperer le niveau complete
        self.completed_level_id = self.game.game_data.get("selected_level", 1)

        # Recuperer la progression
        completed_levels = self.game.game_data.get('completed_levels', [])
        level_stars = self.game.game_data.get('level_stars', {})

        # Charger tous les niveaux
        levels = self.loader.get_all_levels()

        # Creer les nodes
        self.nodes = []
        for i, level_data in enumerate(levels):
            if i < len(self.node_positions):
                x, y = self.node_positions[i]
                level_id = level_data['id']

                unlocked = self.loader.is_level_unlocked(level_id, completed_levels)
                stars = level_stars.get(level_id, 0)
                is_completed = (level_id == self.completed_level_id)

                node = LevelNodeVictory(level_data, x, y, unlocked, stars, is_completed)
                self.nodes.append(node)

    def handle_event(self, event):
        """Gere les evenements"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key in CONTROLS["confirm"]:
                if self.selected_option == 0:  # Continuer
                    self.game.change_scene(STATE_LEVEL_SELECT)
                else:  # Menu Principal
                    self.game.change_scene(STATE_MENU)

    def update(self, dt):
        """Mise a jour des animations"""
        self.animation_timer += dt

        # Mettre a jour les nodes
        for node in self.nodes:
            node.update(dt)

        # Animation de fond
        self.bg_offset += dt * 20
        if self.bg_offset > WIDTH:
            self.bg_offset = 0

    def _draw_arrow(self, screen, x, y, color=YELLOW):
        """Dessine une fleche de selection (triangle)"""
        arrow_size = 12
        points = [
            (x, y - arrow_size // 2),
            (x, y + arrow_size // 2),
            (x + arrow_size, y)
        ]
        pygame.draw.polygon(screen, color, points)

    def _draw_background(self, screen):
        """Dessine le fond anime"""
        screen.fill(BG_COLOR)

        grid_spacing = 40
        grid_color = (40, 40, 50)
        offset = int(self.bg_offset) % grid_spacing

        for x in range(-grid_spacing + offset, WIDTH + grid_spacing, grid_spacing):
            pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT), 1)

        for y in range(0, HEIGHT + grid_spacing, grid_spacing):
            pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y), 1)

    def _draw_paths(self, screen):
        """Dessine les chemins entre les nodes de niveaux"""
        if len(self.nodes) < 2:
            return

        for i in range(len(self.nodes) - 1):
            node1 = self.nodes[i]
            node2 = self.nodes[i + 1]

            if node2.unlocked:
                color = WHITE
                width = 4
            else:
                color = DARK_GRAY
                width = 2

            pygame.draw.line(screen, color, (node1.x, node1.y), (node2.x, node2.y), width)

            if not node2.unlocked:
                dist = math.sqrt((node2.x - node1.x) ** 2 + (node2.y - node1.y) ** 2)
                dash_length = 20
                num_dashes = int(dist / dash_length)

                for j in range(num_dashes):
                    if j % 2 == 0:
                        t1 = j / num_dashes
                        t2 = (j + 1) / num_dashes
                        x1 = node1.x + (node2.x - node1.x) * t1
                        y1 = node1.y + (node2.y - node1.y) * t1
                        x2 = node1.x + (node2.x - node1.x) * t2
                        y2 = node1.y + (node2.y - node1.y) * t2
                        pygame.draw.line(screen, GRAY, (x1, y1), (x2, y2), 2)

    def draw(self, screen):
        """Dessine l'ecran de victoire avec la carte"""
        # Background avec grille animee
        self._draw_background(screen)

        # Dessiner les chemins entre les nodes
        self._draw_paths(screen)

        # Dessiner les nodes
        for node in self.nodes:
            node.draw(screen, self.font_large, self.font_small)

        # Titre VICTOIRE avec effet de pulsation
        pulse = 1.0 + math.sin(self.animation_timer * 5) * 0.1
        title_font_size = int(72 * pulse)
        try:
            title_font = pygame.font.Font(str(FONT_METAL_MANIA), title_font_size)
        except (pygame.error, FileNotFoundError):
            title_font = pygame.font.Font(None, title_font_size)

        # Ombre du titre
        shadow_text = title_font.render("VICTOIRE!", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 4, 80 + 4))
        screen.blit(shadow_text, shadow_rect)

        title_text = title_font.render("VICTOIRE!", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 80))
        screen.blit(title_text, title_rect)

        # Score
        score_text = self.font_score.render(f"Score: {self.final_score}", True, WHITE)
        score_rect = score_text.get_rect(center=(WIDTH // 2, 140))
        screen.blit(score_text, score_rect)

        # Box du menu
        box_width = 300
        box_height = 150
        box_x = (WIDTH - box_width) // 2
        box_y = HEIGHT - 200

        # Fond de la boite
        box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surf.fill((30, 20, 40, 220))
        screen.blit(box_surf, (box_x, box_y))

        # Bordure
        border_color = (
            int(200 + math.sin(self.animation_timer * 4) * 55),
            int(100 + math.sin(self.animation_timer * 3) * 50),
            0
        )
        pygame.draw.rect(screen, border_color, (box_x, box_y, box_width, box_height), 3, border_radius=10)

        # Options
        for i, option in enumerate(self.options):
            y = box_y + 40 + i * 55
            is_selected = i == self.selected_option

            if is_selected:
                sel_surf = pygame.Surface((box_width - 40, 45), pygame.SRCALPHA)
                sel_surf.fill((255, 200, 0, 80))
                screen.blit(sel_surf, (box_x + 20, y - 8))

                # Fleche animee
                arrow_offset = math.sin(self.animation_timer * 8) * 5
                self._draw_arrow(screen, box_x + 30 + arrow_offset, y + 14)

                color = YELLOW
            else:
                color = WHITE

            text = self.font_menu.render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, y + 14))
            screen.blit(text, rect)

        # Instructions
        instructions = self.font_small.render(
            "Utilise les fleches et Entree pour naviguer",
            True, GRAY
        )
        inst_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(instructions, inst_rect)
