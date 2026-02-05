"""
Level Select Scene - Scene de selection des niveaux avec interface carte
"""

import pygame
from scenes.base import Scene
from settings import (
    WIDTH, HEIGHT, WHITE, BLACK, BG_COLOR, DARK_GRAY, GRAY,
    PURPLE, ORANGE, YELLOW, GREEN, BLUE, RED,
    FONT_METAL_MANIA, FONT_ROAD_RAGE,
    STATE_GAMEPLAY, STATE_MENU,
    CONTROLS,
    IMG_BG_DIR, IMG_BG_LEVEL_CHOICE,
    SND_DIR, SND_MUSIC_MENU,
)
from level_loader import get_loader
import math


class LevelNode:
    """Represente un noeud de niveau sur la carte"""

    def __init__(self, level_data, x, y, unlocked=False, stars=0):
        self.level_data = level_data
        self.level_id = level_data['id']
        self.x = x
        self.y = y
        self.unlocked = unlocked
        self.stars = stars  # 0-3 etoiles
        self.radius = 50
        self.hover = False
        self.pulse_timer = 0

    def get_rect(self):
        """Retourne le rect pour la detection de collision"""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def update(self, dt, mouse_pos):
        """Met a jour l'animation du noeud"""
        # Verifier le hover
        dist = math.sqrt((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2)
        self.hover = dist <= self.radius and self.unlocked

        # Animation de pulsation
        if self.unlocked:
            self.pulse_timer += dt * 2
            if self.pulse_timer > math.pi * 2:
                self.pulse_timer -= math.pi * 2

    def draw(self, screen, font_large, font_small):
        """Dessine le noeud de niveau"""
        # Effet de pulsation pour les niveaux deverrouilles
        pulse = 0
        if self.unlocked:
            pulse = int(math.sin(self.pulse_timer) * 5)

        # Couleur selon l'etat
        if not self.unlocked:
            color = DARK_GRAY
            border_color = GRAY
        elif self.hover:
            color = ORANGE
            border_color = YELLOW
        else:
            # Couleur selon la difficulte
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
        # Corps du cadenas
        lock_rect = pygame.Rect(x - 12, y - 5, 24, 20)
        pygame.draw.rect(screen, GRAY, lock_rect, border_radius=3)
        pygame.draw.rect(screen, BLACK, lock_rect, 2, border_radius=3)

        # Anse du cadenas
        arc_rect = pygame.Rect(x - 10, y - 20, 20, 20)
        pygame.draw.arc(screen, GRAY, arc_rect, 0, math.pi, 3)


class LevelSelectScene(Scene):
    """Scene de selection des niveaux avec interface carte"""

    def __init__(self, game):
        super().__init__(game)

        # Charger les fonts
        try:
            self.font_title = pygame.font.Font(str(FONT_ROAD_RAGE), 72)
            self.font_large = pygame.font.Font(str(FONT_METAL_MANIA), 48)
            self.font_medium = pygame.font.Font(str(FONT_METAL_MANIA), 28)
            self.font_small = pygame.font.Font(str(FONT_METAL_MANIA), 20)
        except:
            self.font_title = pygame.font.Font(None, 72)
            self.font_large = pygame.font.Font(None, 48)
            self.font_medium = pygame.font.Font(None, 28)
            self.font_small = pygame.font.Font(None, 20)

        # Loader de niveaux
        self.loader = get_loader()

        # Nodes de niveaux
        self.nodes = []
        self.selected_node = None

        # Positions des nodes sur la carte (a adapter selon le nombre de niveaux)
        self.node_positions = [
            (300, 450),   # Level 1
            (640, 300),   # Level 2
            (980, 450),   # Level 3
        ]

        # Donnees de progression (a charger depuis save plus tard)
        self.completed_levels = []
        self.level_stars = {}  # {level_id: stars_count}

        # Background
        self.background = None

        # Animation de fond
        self.bg_offset = 0

    def enter(self, **kwargs):
        """Entre dans la scene"""
        # Charger le background
        try:
            bg_path = IMG_BG_DIR / IMG_BG_LEVEL_CHOICE
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Could not load level choice background: {e}")
            self.background = None

        # Recuperer la progression depuis game_data
        self.completed_levels = self.game.game_data.get('completed_levels', [])
        self.level_stars = self.game.game_data.get('level_stars', {})

        # Charger tous les niveaux
        levels = self.loader.get_all_levels()

        # Creer les nodes
        self.nodes = []
        for i, level_data in enumerate(levels):
            if i < len(self.node_positions):
                x, y = self.node_positions[i]
                level_id = level_data['id']

                # Verifier si debloque
                unlocked = self.loader.is_level_unlocked(level_id, self.completed_levels)

                # Obtenir les etoiles
                stars = self.level_stars.get(level_id, 0)

                node = LevelNode(level_data, x, y, unlocked, stars)
                self.nodes.append(node)

        self.selected_node = None

        # Jouer la musique du menu (meme musique que le menu principal)
        try:
            music_path = str(SND_DIR / SND_MUSIC_MENU)
            try:
                pygame.mixer.music.load(music_path)
            except pygame.error:
                pygame.mixer.music.load(music_path, namehint=".mp3")
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError):
            pass

    def handle_event(self, event):
        """Gere les evenements"""
        if event.type == pygame.KEYDOWN:
            # Retour au menu
            if event.key in CONTROLS["pause"]:
                self.game.change_scene(STATE_MENU)

            # Selection avec Enter
            if event.key in CONTROLS["confirm"] and self.selected_node:
                self._start_level(self.selected_node.level_id)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic gauche
                mouse_pos = pygame.mouse.get_pos()
                for node in self.nodes:
                    if node.unlocked and node.hover:
                        self.selected_node = node
                        self._start_level(node.level_id)
                        break

    def update(self, dt):
        """Met a jour la scene"""
        mouse_pos = pygame.mouse.get_pos()

        # Mettre a jour les nodes
        for node in self.nodes:
            node.update(dt, mouse_pos)

            # Selection automatique au hover
            if node.hover:
                self.selected_node = node

        # Animation de fond
        self.bg_offset += dt * 20
        if self.bg_offset > WIDTH:
            self.bg_offset = 0

    def draw(self, screen):
        """Dessine la scene"""
        # Background image ou fond anime
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(BG_COLOR)
            # Fond anime (etoiles ou grille)
            self._draw_background(screen)

        # Titre
        title = self.font_title.render("SÉLECTIONNEZ VOTRE NIVEAU", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, 80))
        # Ombre du titre
        title_shadow = self.font_title.render("SÉLECTIONNEZ VOTRE NIVEAU", True, BLACK)
        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title, title_rect)

        # Dessiner les chemins entre les nodes
        self._draw_paths(screen)

        # Dessiner les nodes
        for node in self.nodes:
            node.draw(screen, self.font_large, self.font_small)

        # Info du niveau selectionne
        if self.selected_node and self.selected_node.unlocked:
            self._draw_level_info(screen, self.selected_node)

        # Instructions
        instructions = self.font_small.render("Cliquez sur un niveau pour commencer - ESC pour revenir en arrière", True, WHITE)
        inst_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(instructions, inst_rect)

    def _draw_background(self, screen):
        """Dessine le fond anime"""
        # Grille simple
        grid_spacing = 40
        grid_color = (40, 40, 50)

        offset = int(self.bg_offset) % grid_spacing

        # Lignes verticales
        for x in range(-grid_spacing + offset, WIDTH + grid_spacing, grid_spacing):
            pygame.draw.line(screen, grid_color, (x, 0), (x, HEIGHT), 1)

        # Lignes horizontales
        for y in range(0, HEIGHT + grid_spacing, grid_spacing):
            pygame.draw.line(screen, grid_color, (0, y), (WIDTH, y), 1)

    def _draw_paths(self, screen):
        """Dessine les chemins entre les nodes de niveaux"""
        if len(self.nodes) < 2:
            return

        for i in range(len(self.nodes) - 1):
            node1 = self.nodes[i]
            node2 = self.nodes[i + 1]

            # Couleur du chemin (debloque si le niveau suivant est debloque)
            if node2.unlocked:
                color = WHITE
                width = 4
            else:
                color = DARK_GRAY
                width = 2

            # Dessiner une ligne entre les centres
            pygame.draw.line(screen, color, (node1.x, node1.y), (node2.x, node2.y), width)

            # Pointilles si verrouille
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

    def _draw_level_info(self, screen, node):
        """Dessine les informations du niveau selectionne"""
        # Panel d'info en bas a droite
        panel_width = 400
        panel_height = 180
        panel_x = WIDTH - panel_width - 40
        panel_y = HEIGHT - panel_height - 80

        # Fond du panel avec transparence
        panel_surf = pygame.Surface((panel_width, panel_height))
        panel_surf.set_alpha(230)
        panel_surf.fill((30, 30, 40))
        screen.blit(panel_surf, (panel_x, panel_y))

        # Bordure
        pygame.draw.rect(screen, ORANGE, (panel_x, panel_y, panel_width, panel_height), 3, border_radius=10)

        # Nom du niveau
        name_text = self.font_medium.render(node.level_data['name'], True, YELLOW)
        screen.blit(name_text, (panel_x + 20, panel_y + 15))

        # Description
        desc = node.level_data.get('description', 'No description')
        desc_text = self.font_small.render(desc, True, WHITE)
        screen.blit(desc_text, (panel_x + 20, panel_y + 55))

        # Difficulte
        difficulty = node.level_data.get('difficulty', 'easy').upper()
        diff_color = GREEN if difficulty == 'EASY' else (BLUE if difficulty == 'MEDIUM' else RED)
        diff_text = self.font_small.render(f"Difficulty: {difficulty}", True, diff_color)
        screen.blit(diff_text, (panel_x + 20, panel_y + 90))

        # Nombre de stages
        num_stages = len(node.level_data.get('stages', []))
        stages_text = self.font_small.render(f"Stages: {num_stages}", True, WHITE)
        screen.blit(stages_text, (panel_x + 20, panel_y + 120))

        # Instruction
        play_text = self.font_small.render("Click to PLAY!", True, YELLOW)
        screen.blit(play_text, (panel_x + 20, panel_y + 145))

    def _start_level(self, level_id):
        """Demarre un niveau"""
        # Sauvegarder le niveau selectionne
        self.game.game_data['selected_level'] = level_id
        self.game.game_data['current_stage'] = 1

        # Aller a la scene de gameplay
        self.game.change_scene(STATE_GAMEPLAY, level_id=level_id, stage_id=1)
