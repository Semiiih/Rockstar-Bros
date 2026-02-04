"""
Rockstar Bros - Scene du menu principal
Gere le menu, la selection de personnage et le lancement du jeu
"""

import pygame
import math
from scenes.base import Scene
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, GRAY, PURPLE, ORANGE,
    STATE_LEVEL_SELECT, CONTROLS,
    IMG_DIR, IMG_HOME, IMG_LOGO, IMG_PLAYER_DIR,
    IMG_PLAYER1_IDLE, IMG_PLAYER2_IDLE,
    PLAYER_WIDTH, PLAYER_HEIGHT,
    SND_DIR, SND_MUSIC_MENU,
    FONT_METAL_MANIA, FONT_ROAD_RAGE
)


class MenuScene(Scene):
    """Scene du menu principal avec selection de personnage"""

    def __init__(self, game):
        super().__init__(game)
        self.font_title = None
        self.font_menu = None
        self.font_small = None

        # Etat du menu
        self.menu_state = "main"  # "main" ou "character_select"
        self.selected_option = 0
        self.main_options = ["Jouer", "Quitter"]
        self.selected_character = 1

        # Images (chargees dans enter())
        self.background = None
        self.logo = None
        self.player1_img = None
        self.player2_img = None

        # Animation
        self.anim_time = 0

    def enter(self, **kwargs):
        """Initialisation a l'entree dans la scene"""
        # Charger les polices - Metal Mania pour titres, Road Rage pour texte
        try:
            self.font_title = pygame.font.Font(str(FONT_METAL_MANIA), 72)
            self.font_menu = pygame.font.Font(str(FONT_ROAD_RAGE), 36)
            self.font_small = pygame.font.Font(str(FONT_ROAD_RAGE), 24)
        except (pygame.error, FileNotFoundError):
            # Fallback si la font n'est pas trouvee
            self.font_title = pygame.font.Font(None, 72)
            self.font_menu = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)

        # Reset etat
        self.menu_state = "main"
        self.selected_option = 0

        # Charger le background
        self._load_images()

        # Charger et jouer la musique du menu
        self._play_menu_music()

    def _load_images(self):
        """Charge les images du menu"""
        # Background (home.png)
        try:
            bg_path = IMG_DIR / IMG_HOME
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError):
            self.background = None

        # Logo
        try:
            logo_path = IMG_DIR / IMG_LOGO
            self.logo = pygame.image.load(str(logo_path)).convert_alpha()
            # Redimensionner le logo (largeur 400px, hauteur proportionnelle)
            logo_width = 400
            ratio = logo_width / self.logo.get_width()
            logo_height = int(self.logo.get_height() * ratio)
            self.logo = pygame.transform.scale(self.logo, (logo_width, logo_height))
        except (pygame.error, FileNotFoundError):
            self.logo = None

        # Images des personnages pour selection
        try:
            p1_path = IMG_PLAYER_DIR / IMG_PLAYER1_IDLE
            self.player1_img = pygame.image.load(str(p1_path)).convert_alpha()
            self.player1_img = pygame.transform.scale(
                self.player1_img, (PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2)
            )
        except (pygame.error, FileNotFoundError):
            self.player1_img = None

        try:
            p2_path = IMG_PLAYER_DIR / IMG_PLAYER2_IDLE
            self.player2_img = pygame.image.load(str(p2_path)).convert_alpha()
            self.player2_img = pygame.transform.scale(
                self.player2_img, (PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2)
            )
        except (pygame.error, FileNotFoundError):
            self.player2_img = None

    def _play_menu_music(self):
        """Charge et joue la musique du menu"""
        try:
            music_path = SND_DIR / SND_MUSIC_MENU
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # -1 = boucle infinie
        except (pygame.error, FileNotFoundError) as e:
            print(f"Impossible de charger la musique du menu: {e}")

    def handle_event(self, event):
        """Gere les evenements du menu"""
        if event.type == pygame.KEYDOWN:
            if self.menu_state == "main":
                self._handle_main_menu(event)
            elif self.menu_state == "character_select":
                self._handle_character_select(event)

    def _handle_main_menu(self, event):
        """Gere les inputs du menu principal"""
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.main_options)
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.main_options)
        elif event.key in CONTROLS["confirm"]:
            if self.selected_option == 0:  # Jouer
                self.menu_state = "character_select"
                self.selected_character = 1
            elif self.selected_option == 1:  # Quitter
                self.game.running = False

    def _handle_character_select(self, event):
        """Gere les inputs de la selection de personnage"""
        if event.key == pygame.K_LEFT:
            self.selected_character = 1
        elif event.key == pygame.K_RIGHT:
            self.selected_character = 2
        elif event.key in CONTROLS["confirm"]:
            # Lancer le jeu avec le personnage selectionne
            self.game.game_data["selected_character"] = self.selected_character
            self.game.reset_game()
            # Aller vers la selection de niveau
            self.game.change_scene(STATE_LEVEL_SELECT)
        elif event.key == pygame.K_ESCAPE:
            self.menu_state = "main"

    def update(self, dt):
        """Mise a jour du menu (animations eventuelles)"""
        self.anim_time += dt

    def draw(self, screen):
        """Dessine le menu"""
        # Background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            # Fond degrade simple si pas d'image
            self._draw_gradient_bg(screen)

        if self.menu_state == "main":
            self._draw_main_menu(screen)
        elif self.menu_state == "character_select":
            self._draw_character_select(screen)

    def _draw_gradient_bg(self, screen):
        """Dessine un fond degrade simple"""
        for y in range(HEIGHT):
            color_value = int(25 + (y / HEIGHT) * 30)
            pygame.draw.line(
                screen,
                (color_value, color_value, color_value + 20),
                (0, y), (WIDTH, y)
            )

    def _draw_arrow(self, screen, x, y, color=YELLOW):
        """Dessine une fleche de selection (triangle)"""
        arrow_size = 12
        points = [
            (x, y - arrow_size // 2),
            (x, y + arrow_size // 2),
            (x + arrow_size, y)
        ]
        pygame.draw.polygon(screen, color, points)

    def _draw_main_menu(self, screen):
        """Dessine le menu principal"""
        # Logo ou titre texte
        if self.logo:
            logo_rect = self.logo.get_rect(center=(WIDTH // 2, 140))
            screen.blit(self.logo, logo_rect)
        else:
            # Fallback: titre texte si pas de logo
            title_text = self.font_title.render("ROCKSTAR BROS", True, YELLOW)
            title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
            screen.blit(title_text, title_rect)

            # Sous-titre
            subtitle_text = self.font_small.render("Guitar Hero", True, WHITE)
            subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 210))
            screen.blit(subtitle_text, subtitle_rect)

        # Options du menu
        for i, option in enumerate(self.main_options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.font_menu.render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, 350 + i * 60))
            screen.blit(text, rect)

            # Fleche a gauche de l'option selectionnee
            if i == self.selected_option:
                self._draw_arrow(screen, rect.left - 25, rect.centery)

        # Instructions
        instructions = self.font_small.render(
            "Fleches pour naviguer - Entree pour valider", True, WHITE
        )
        inst_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 150))
        screen.blit(instructions, inst_rect)

    def _draw_character_select(self, screen):
        """Dessine l'ecran de selection de personnage"""
        # Titre
        title_text = self.font_title.render("CHOISIS TON GUITARISTE", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Personnage 1
        p1_x = WIDTH // 3
        p1_y = HEIGHT // 2
        self._draw_character_option(screen, 1, p1_x, p1_y, self.player1_img, "Axel")

        # Personnage 2
        p2_x = (WIDTH // 5) * 3
        p2_y = HEIGHT // 2
        self._draw_character_option(screen, 2, p2_x, p2_y, self.player2_img, "Luna")

        # Instructions
        instructions = self.font_small.render(
            "Gauche/Droite pour choisir - Entree pour valider - Echap pour retour",
            True, WHITE
        )
        inst_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        screen.blit(instructions, inst_rect)

    def _draw_character_option(self, screen, char_num, x, y, image, name):
        """Dessine une option de personnage avec animations rock"""
        is_selected = self.selected_character == char_num

        # Dimensions de l'image (2x la taille normale)
        img_width = PLAYER_WIDTH * 2
        img_height = PLAYER_HEIGHT * 2

        # Animation rock pour le personnage selectionne
        offset_y = 0
        rotation = 0
        scale_bonus = 0
        if is_selected:
            # Effet de "headbang" rock - oscillation rapide
            headbang = math.sin(self.anim_time * 8) * 3
            offset_y = abs(headbang)
            # Legere rotation style rock
            rotation = math.sin(self.anim_time * 6) * 5
            # Pulsation au rythme
            scale_bonus = abs(math.sin(self.anim_time * 4)) * 0.08

        # Position du personnage avec animation
        char_y = y + offset_y

        # Cadre autour du personnage uniquement (pas le nom)
        padding = 15
        frame_rect = pygame.Rect(
            x - img_width // 2 - padding,
            y - img_height // 2 - padding,
            img_width + padding * 2,
            img_height + padding * 2
        )

        if is_selected:
            # Effet d'eclairs/energie rock autour du cadre
            for i in range(3):
                spark_offset = math.sin(self.anim_time * 10 + i * 2) * 5
                spark_alpha = int(100 + math.sin(self.anim_time * 12 + i) * 80)
                spark_color = (255, 100 + i * 50, 0, spark_alpha)
                spark_surface = pygame.Surface((frame_rect.width + 30, frame_rect.height + 30), pygame.SRCALPHA)
                pygame.draw.rect(
                    spark_surface, spark_color,
                    (spark_offset, spark_offset, frame_rect.width + 30 - spark_offset * 2, frame_rect.height + 30 - spark_offset * 2),
                    3, border_radius=12
                )
                screen.blit(spark_surface, (frame_rect.x - 15, frame_rect.y - 15))

            # Cadre principal avec couleur qui pulse
            frame_color = (
                255,
                int(150 + math.sin(self.anim_time * 8) * 105),
                0
            )
            pygame.draw.rect(screen, frame_color, frame_rect, 5, border_radius=10)
        else:
            # Cadre simple pour non-selectionne
            pygame.draw.rect(screen, GRAY, frame_rect, 2, border_radius=10)

        # Image du personnage ou placeholder
        if image:
            # Appliquer les effets si selectionne
            if is_selected:
                new_width = int(img_width * (1 + scale_bonus))
                new_height = int(img_height * (1 + scale_bonus))
                scaled_img = pygame.transform.scale(image, (new_width, new_height))
                # Appliquer la rotation
                rotated_img = pygame.transform.rotate(scaled_img, rotation)
                img_rect = rotated_img.get_rect(center=(x, char_y))
                screen.blit(rotated_img, img_rect)
            else:
                img_rect = image.get_rect(center=(x, y))
                screen.blit(image, img_rect)
        else:
            # Placeholder colore
            placeholder_color = PURPLE if char_num == 1 else ORANGE
            placeholder_rect = pygame.Rect(
                x - img_width // 2,
                char_y - img_height // 2,
                img_width,
                img_height
            )
            pygame.draw.rect(screen, placeholder_color, placeholder_rect, border_radius=5)

            # Texte placeholder
            ph_text = self.font_small.render(f"P{char_num}", True, WHITE)
            ph_rect = ph_text.get_rect(center=(x, char_y))
            screen.blit(ph_text, ph_rect)

        # Nom du personnage (plus eloigne du cadre)
        name_y = frame_rect.bottom + 40
        if is_selected:
            # Effet de texte rock pour le nom selectionne
            name_scale = 1.0 + abs(math.sin(self.anim_time * 6)) * 0.1
            try:
                rock_font = pygame.font.Font(str(FONT_METAL_MANIA), int(36 * name_scale))
            except (pygame.error, FileNotFoundError):
                rock_font = self.font_menu
            name_text = rock_font.render(name, True, YELLOW)
        else:
            name_text = self.font_menu.render(name, True, WHITE)
        name_rect = name_text.get_rect(center=(x, name_y))
        screen.blit(name_text, name_rect)
