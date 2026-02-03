"""
Rockstar Bros - Scene du menu principal
Gere le menu, la selection de personnage et le lancement du jeu
"""

import pygame
from scenes.base import Scene
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, GRAY, PURPLE, ORANGE,
    STATE_GAMEPLAY, CONTROLS,
    IMG_DIR, IMG_HOME, IMG_PLAYER_DIR,
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
        self.player1_img = None
        self.player2_img = None

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
            self.game.change_scene(STATE_GAMEPLAY)
        elif event.key == pygame.K_ESCAPE:
            self.menu_state = "main"

    def update(self, dt):
        """Mise a jour du menu (animations eventuelles)"""
        pass

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

    def _draw_main_menu(self, screen):
        """Dessine le menu principal"""
        # Titre
        title_text = self.font_title.render("ROCKSTAR BROS", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Sous-titre
        subtitle_text = self.font_small.render("Guitar Hero", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(WIDTH // 2, 210))
        screen.blit(subtitle_text, subtitle_rect)

        # Options du menu
        for i, option in enumerate(self.main_options):
            if i == self.selected_option:
                color = YELLOW
                prefix = "> "
            else:
                color = WHITE
                prefix = "  "

            text = self.font_menu.render(prefix + option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, 350 + i * 60))
            screen.blit(text, rect)

        # Instructions
        instructions = self.font_small.render(
            "Fleches pour naviguer - Entree pour valider", True, GRAY
        )
        inst_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(instructions, inst_rect)

    def _draw_character_select(self, screen):
        """Dessine l'ecran de selection de personnage"""
        # Titre
        title_text = self.font_title.render("CHOISIS TON GUITARISTE", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
        screen.blit(title_text, title_rect)

        # Personnage 1
        p1_x = WIDTH // 4
        p1_y = HEIGHT // 2
        self._draw_character_option(screen, 1, p1_x, p1_y, self.player1_img, "Axel")

        # Personnage 2
        p2_x = (WIDTH // 4) * 3
        p2_y = HEIGHT // 2
        self._draw_character_option(screen, 2, p2_x, p2_y, self.player2_img, "Luna")

        # Instructions
        instructions = self.font_small.render(
            "Gauche/Droite pour choisir - Entree pour valider - Echap pour retour",
            True, GRAY
        )
        inst_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(instructions, inst_rect)

    def _draw_character_option(self, screen, char_num, x, y, image, name):
        """Dessine une option de personnage"""
        is_selected = self.selected_character == char_num

        # Cadre
        frame_color = YELLOW if is_selected else GRAY
        frame_width = 5 if is_selected else 2
        frame_rect = pygame.Rect(
            x - PLAYER_WIDTH - 20,
            y - PLAYER_HEIGHT - 20,
            (PLAYER_WIDTH + 20) * 2,
            (PLAYER_HEIGHT + 40) * 2
        )
        pygame.draw.rect(screen, frame_color, frame_rect, frame_width, border_radius=10)

        # Image du personnage ou placeholder
        if image:
            img_rect = image.get_rect(center=(x, y))
            screen.blit(image, img_rect)
        else:
            # Placeholder colore
            placeholder_color = PURPLE if char_num == 1 else ORANGE
            placeholder_rect = pygame.Rect(
                x - PLAYER_WIDTH,
                y - PLAYER_HEIGHT,
                PLAYER_WIDTH * 2,
                PLAYER_HEIGHT * 2
            )
            pygame.draw.rect(screen, placeholder_color, placeholder_rect, border_radius=5)

            # Texte placeholder
            ph_text = self.font_small.render(f"P{char_num}", True, WHITE)
            ph_rect = ph_text.get_rect(center=(x, y))
            screen.blit(ph_text, ph_rect)

        # Nom du personnage
        name_color = YELLOW if is_selected else WHITE
        name_text = self.font_menu.render(name, True, name_color)
        name_rect = name_text.get_rect(center=(x, y + PLAYER_HEIGHT + 50))
        screen.blit(name_text, name_rect)
