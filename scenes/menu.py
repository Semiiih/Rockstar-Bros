"""
Rockstar Bros - Scene du menu principal
Menu stylise avec selection de personnage et configuration des touches
"""

import pygame
import math
from scenes.base import Scene
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, GRAY, PURPLE, ORANGE, RED, BLACK,
    STATE_GAMEPLAY, CONTROLS,
    IMG_DIR, IMG_HOME, IMG_LOGO, IMG_PLAYER_DIR,
    IMG_PLAYER1_IDLE, IMG_PLAYER2_IDLE,
    PLAYER_WIDTH, PLAYER_HEIGHT,
    SND_DIR, SND_MUSIC_MENU,
    FONT_METAL_MANIA, FONT_ROAD_RAGE
)


# Noms des touches pour l'affichage
KEY_NAMES = {
    pygame.K_LEFT: "←", pygame.K_RIGHT: "→", pygame.K_UP: "↑", pygame.K_DOWN: "↓",
    pygame.K_SPACE: "ESPACE", pygame.K_RETURN: "ENTREE", pygame.K_ESCAPE: "ECHAP",
    pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D",
    pygame.K_e: "E", pygame.K_f: "F", pygame.K_g: "G", pygame.K_h: "H",
    pygame.K_i: "I", pygame.K_j: "J", pygame.K_k: "K", pygame.K_l: "L",
    pygame.K_m: "M", pygame.K_n: "N", pygame.K_o: "O", pygame.K_p: "P",
    pygame.K_q: "Q", pygame.K_r: "R", pygame.K_s: "S", pygame.K_t: "T",
    pygame.K_u: "U", pygame.K_v: "V", pygame.K_w: "W", pygame.K_x: "X",
    pygame.K_y: "Y", pygame.K_z: "Z",
    pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3",
    pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7",
    pygame.K_8: "8", pygame.K_9: "9",
    pygame.K_LSHIFT: "L-SHIFT", pygame.K_RSHIFT: "R-SHIFT",
    pygame.K_LCTRL: "L-CTRL", pygame.K_RCTRL: "R-CTRL",
    pygame.K_TAB: "TAB", pygame.K_BACKSPACE: "RETOUR",
}

# Actions configurables et leurs noms
CONFIGURABLE_ACTIONS = [
    ("left", "Gauche"),
    ("right", "Droite"),
    ("jump", "Sauter"),
    ("crouch", "S'accroupir"),
    ("attack", "Attaquer"),
    ("ultimate", "Ultime"),
]


def get_key_name(key):
    """Retourne le nom lisible d'une touche"""
    return KEY_NAMES.get(key, pygame.key.name(key).upper())


class MenuScene(Scene):
    """Scene du menu principal avec selection de personnage et options"""

    def __init__(self, game):
        super().__init__(game)
        self.font_title = None
        self.font_menu = None
        self.font_small = None

        # Etat du menu: "main", "character_select", "options", "controls"
        self.menu_state = "main"
        self.selected_option = 0
        self.main_options = ["Jouer", "Options", "Quitter"]
        self.options_menu = ["Touches", "Retour"]
        self.selected_character = 1

        # Configuration des touches
        self.controls_selected = 0
        self.waiting_for_key = False
        self.key_to_change = None

        # Images
        self.background = None
        self.logo = None
        self.player1_img = None
        self.player2_img = None

        # Animation
        self.anim_time = 0

        # Particules de fond
        self.particles = []
        for _ in range(30):
            self._spawn_particle()

    def _spawn_particle(self):
        """Cree une particule de fond"""
        import random
        particle = {
            "x": random.randint(0, WIDTH),
            "y": random.randint(0, HEIGHT),
            "size": random.randint(2, 6),
            "speed": random.uniform(0.5, 2),
            "alpha": random.randint(50, 150),
            "color": random.choice([(255, 200, 0), (255, 100, 0), (200, 0, 200)])
        }
        self.particles.append(particle)

    def enter(self, **kwargs):
        """Initialisation a l'entree dans la scene"""
        try:
            self.font_title = pygame.font.Font(str(FONT_METAL_MANIA), 72)
            self.font_menu = pygame.font.Font(str(FONT_ROAD_RAGE), 36)
            self.font_small = pygame.font.Font(str(FONT_ROAD_RAGE), 24)
        except (pygame.error, FileNotFoundError):
            self.font_title = pygame.font.Font(None, 72)
            self.font_menu = pygame.font.Font(None, 36)
            self.font_small = pygame.font.Font(None, 24)

        self.menu_state = "main"
        self.selected_option = 0
        self._load_images()
        self._play_menu_music()

    def _load_images(self):
        """Charge les images du menu"""
        try:
            bg_path = IMG_DIR / IMG_HOME
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError):
            self.background = None

        try:
            logo_path = IMG_DIR / IMG_LOGO
            self.logo = pygame.image.load(str(logo_path)).convert_alpha()
            logo_width = 500
            ratio = logo_width / self.logo.get_width()
            logo_height = int(self.logo.get_height() * ratio)
            self.logo = pygame.transform.scale(self.logo, (logo_width, logo_height))
        except (pygame.error, FileNotFoundError):
            self.logo = None

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
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError):
            pass

    def handle_event(self, event):
        """Gere les evenements du menu"""
        if event.type == pygame.KEYDOWN:
            # Attente d'une touche pour la configuration
            if self.waiting_for_key:
                self._set_new_key(event.key)
                return

            if self.menu_state == "main":
                self._handle_main_menu(event)
            elif self.menu_state == "character_select":
                self._handle_character_select(event)
            elif self.menu_state == "options":
                self._handle_options(event)
            elif self.menu_state == "controls":
                self._handle_controls(event)

    def _handle_main_menu(self, event):
        """Gere les inputs du menu principal"""
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.main_options)
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.main_options)
        elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
            if self.selected_option == 0:  # Jouer
                self.menu_state = "character_select"
                self.selected_character = 1
            elif self.selected_option == 1:  # Options
                self.menu_state = "options"
                self.selected_option = 0
            elif self.selected_option == 2:  # Quitter
                self.game.running = False

    def _handle_character_select(self, event):
        """Gere les inputs de la selection de personnage"""
        if event.key == pygame.K_LEFT:
            self.selected_character = 1
        elif event.key == pygame.K_RIGHT:
            self.selected_character = 2
        elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
            self.game.game_data["selected_character"] = self.selected_character
            self.game.reset_game()
            self.game.change_scene(STATE_GAMEPLAY)
        elif event.key == pygame.K_ESCAPE:
            self.menu_state = "main"
            self.selected_option = 0

    def _handle_options(self, event):
        """Gere les inputs du menu options"""
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.options_menu)
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options_menu)
        elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
            if self.selected_option == 0:  # Touches
                self.menu_state = "controls"
                self.controls_selected = 0
            elif self.selected_option == 1:  # Retour
                self.menu_state = "main"
                self.selected_option = 0
        elif event.key == pygame.K_ESCAPE:
            self.menu_state = "main"
            self.selected_option = 0

    def _handle_controls(self, event):
        """Gere les inputs du menu de configuration des touches"""
        num_actions = len(CONFIGURABLE_ACTIONS)

        if event.key == pygame.K_UP:
            self.controls_selected = (self.controls_selected - 1) % (num_actions + 1)
        elif event.key == pygame.K_DOWN:
            self.controls_selected = (self.controls_selected + 1) % (num_actions + 1)
        elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
            if self.controls_selected < num_actions:
                # Commencer a attendre une nouvelle touche
                self.waiting_for_key = True
                self.key_to_change = CONFIGURABLE_ACTIONS[self.controls_selected][0]
            else:
                # Retour
                self.menu_state = "options"
                self.selected_option = 0
        elif event.key == pygame.K_ESCAPE:
            self.menu_state = "options"
            self.selected_option = 0

    def _set_new_key(self, key):
        """Definit une nouvelle touche pour l'action selectionnee"""
        if key == pygame.K_ESCAPE:
            # Annuler
            self.waiting_for_key = False
            self.key_to_change = None
            return

        # Mettre a jour la touche (remplace la premiere touche)
        if self.key_to_change and self.key_to_change in CONTROLS:
            CONTROLS[self.key_to_change][0] = key

        self.waiting_for_key = False
        self.key_to_change = None

    def update(self, dt):
        """Mise a jour du menu"""
        self.anim_time += dt

        # Mettre a jour les particules
        for particle in self.particles:
            particle["y"] -= particle["speed"]
            if particle["y"] < -10:
                particle["y"] = HEIGHT + 10
                particle["x"] = __import__("random").randint(0, WIDTH)

    def draw(self, screen):
        """Dessine le menu"""
        # Background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            self._draw_gradient_bg(screen)

        # Particules de fond
        self._draw_particles(screen)

        # Overlay semi-transparent pour meilleure lisibilite
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        screen.blit(overlay, (0, 0))

        if self.menu_state == "main":
            self._draw_main_menu(screen)
        elif self.menu_state == "character_select":
            self._draw_character_select(screen)
        elif self.menu_state == "options":
            self._draw_options(screen)
        elif self.menu_state == "controls":
            self._draw_controls(screen)

    def _draw_particles(self, screen):
        """Dessine les particules de fond"""
        for particle in self.particles:
            surf = pygame.Surface((particle["size"] * 2, particle["size"] * 2), pygame.SRCALPHA)
            color = (*particle["color"], particle["alpha"])
            pygame.draw.circle(surf, color, (particle["size"], particle["size"]), particle["size"])
            screen.blit(surf, (int(particle["x"]), int(particle["y"])))

    def _draw_gradient_bg(self, screen):
        """Dessine un fond degrade rock"""
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(20 + ratio * 30)
            g = int(10 + ratio * 20)
            b = int(30 + ratio * 40)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    def _draw_menu_box(self, screen, title, options, selected, y_start=250):
        """Dessine une boite de menu stylisee"""
        box_width = 500
        box_height = 100 + len(options) * 70
        box_x = (WIDTH - box_width) // 2
        box_y = y_start

        # Fond de la boite avec effet rock
        box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)

        # Gradient dans la boite
        for y in range(box_height):
            alpha = 200 - int(y / box_height * 50)
            pygame.draw.line(box_surf, (30, 20, 40, alpha), (0, y), (box_width, y))

        screen.blit(box_surf, (box_x, box_y))

        # Bordure animee
        border_color = (
            int(200 + math.sin(self.anim_time * 4) * 55),
            int(100 + math.sin(self.anim_time * 3) * 50),
            0
        )
        pygame.draw.rect(screen, border_color, (box_x, box_y, box_width, box_height), 3, border_radius=10)

        # Titre de la boite
        title_text = self.font_menu.render(title, True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH // 2, box_y + 40))
        screen.blit(title_text, title_rect)

        # Ligne sous le titre
        pygame.draw.line(screen, YELLOW, (box_x + 30, box_y + 70), (box_x + box_width - 30, box_y + 70), 2)

        # Options
        for i, option in enumerate(options):
            y = box_y + 100 + i * 65
            is_selected = i == selected

            if is_selected:
                # Fond de selection
                sel_surf = pygame.Surface((box_width - 60, 50), pygame.SRCALPHA)
                sel_surf.fill((255, 200, 0, 80))
                screen.blit(sel_surf, (box_x + 30, y - 8))

                # Fleches animees
                arrow_offset = math.sin(self.anim_time * 8) * 5
                self._draw_arrow(screen, box_x + 45 + arrow_offset, y + 17)
                self._draw_arrow_right(screen, box_x + box_width - 45 - arrow_offset, y + 17)

                color = YELLOW
            else:
                color = WHITE

            text = self.font_menu.render(option, True, color)
            rect = text.get_rect(center=(WIDTH // 2, y + 17))
            screen.blit(text, rect)

        return box_y + box_height

    def _draw_arrow(self, screen, x, y, color=YELLOW):
        """Dessine une fleche vers la droite"""
        points = [(x, y - 8), (x, y + 8), (x + 12, y)]
        pygame.draw.polygon(screen, color, points)

    def _draw_arrow_right(self, screen, x, y, color=YELLOW):
        """Dessine une fleche vers la gauche"""
        points = [(x, y - 8), (x, y + 8), (x - 12, y)]
        pygame.draw.polygon(screen, color, points)

    def _draw_main_menu(self, screen):
        """Dessine le menu principal"""
        # Logo avec effet de pulsation
        if self.logo:
            pulse = 1.0 + math.sin(self.anim_time * 2) * 0.03
            logo_w = int(self.logo.get_width() * pulse)
            logo_h = int(self.logo.get_height() * pulse)
            scaled_logo = pygame.transform.scale(self.logo, (logo_w, logo_h))
            logo_rect = scaled_logo.get_rect(center=(WIDTH // 2, 130))
            screen.blit(scaled_logo, logo_rect)
        else:
            # Titre texte avec effet
            title_text = self.font_title.render("ROCKSTAR BROS", True, YELLOW)
            shadow_text = self.font_title.render("ROCKSTAR BROS", True, (50, 30, 0))
            title_rect = title_text.get_rect(center=(WIDTH // 2, 130))
            screen.blit(shadow_text, title_rect.move(4, 4))
            screen.blit(title_text, title_rect)

        # Boite de menu
        self._draw_menu_box(screen, "MENU PRINCIPAL", self.main_options, self.selected_option)

        # Instructions en bas
        self._draw_instructions(screen, "Naviguer  |  ENTREE Valider")

    def _draw_options(self, screen):
        """Dessine le menu options"""
        # Titre
        title_text = self.font_title.render("OPTIONS", True, YELLOW)
        shadow_text = self.font_title.render("OPTIONS", True, (50, 30, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 120))
        screen.blit(shadow_text, title_rect.move(4, 4))
        screen.blit(title_text, title_rect)

        # Menu options - centre verticalement
        self._draw_menu_box(screen, "PARAMETRES", self.options_menu, self.selected_option, 220)

        self._draw_instructions(screen, "Naviguer  |  ENTREE Valider  |  ECHAP Retour")

    def _draw_controls(self, screen):
        """Dessine le menu de configuration des touches"""
        # Titre
        title_text = self.font_title.render("TOUCHES", True, YELLOW)
        shadow_text = self.font_title.render("TOUCHES", True, (50, 30, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 60))
        screen.blit(shadow_text, title_rect.move(4, 4))
        screen.blit(title_text, title_rect)

        # Calculer la hauteur necessaire
        num_actions = len(CONFIGURABLE_ACTIONS)
        row_height = 48
        header_height = 70
        retour_height = 55
        padding = 30

        # Hauteur totale: header + actions + retour + padding
        box_height = header_height + (num_actions * row_height) + retour_height + padding
        box_width = 650
        box_x = (WIDTH - box_width) // 2
        box_y = 110

        # Fond
        box_surf = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        box_surf.fill((30, 20, 40, 220))
        screen.blit(box_surf, (box_x, box_y))

        # Bordure
        border_color = (200, 100, 0)
        pygame.draw.rect(screen, border_color, (box_x, box_y, box_width, box_height), 3, border_radius=10)

        # Colonnes bien espacees - tout a l'interieur de la boite
        col1_x = box_x + 40  # Action
        col2_x = box_x + 280  # Touche 1
        col3_x = box_x + 450  # Touche 2

        # En-tete
        header_text = self.font_menu.render("Action", True, YELLOW)
        screen.blit(header_text, (col1_x, box_y + 20))
        header_text2 = self.font_menu.render("Touche 1", True, YELLOW)
        screen.blit(header_text2, (col2_x, box_y + 20))
        header_text3 = self.font_menu.render("Touche 2", True, YELLOW)
        screen.blit(header_text3, (col3_x, box_y + 20))

        pygame.draw.line(screen, YELLOW, (box_x + 20, box_y + 60), (box_x + box_width - 20, box_y + 60), 2)

        # Liste des actions
        for i, (action_key, action_name) in enumerate(CONFIGURABLE_ACTIONS):
            y = box_y + header_height + i * row_height
            is_selected = i == self.controls_selected

            if is_selected:
                # Fond de selection - bien centre dans la boite
                sel_surf = pygame.Surface((box_width - 40, 42), pygame.SRCALPHA)
                sel_surf.fill((255, 200, 0, 80))
                screen.blit(sel_surf, (box_x + 20, y - 2))

            # Nom de l'action
            color = YELLOW if is_selected else WHITE
            name_text = self.font_small.render(action_name, True, color)
            screen.blit(name_text, (col1_x, y + 10))

            # Touches actuelles
            keys = CONTROLS.get(action_key, [])
            if len(keys) > 0:
                key1_name = get_key_name(keys[0])
                if self.waiting_for_key and self.key_to_change == action_key:
                    key1_text = self.font_small.render("...", True, RED)
                else:
                    key1_text = self.font_small.render(key1_name, True, color)
                screen.blit(key1_text, (col2_x, y + 10))

            if len(keys) > 1:
                key2_name = get_key_name(keys[1])
                key2_text = self.font_small.render(key2_name, True, GRAY)
                screen.blit(key2_text, (col3_x, y + 10))

        # Option Retour - positionne apres les actions
        retour_y = box_y + header_height + num_actions * row_height + 10
        is_retour_selected = self.controls_selected == num_actions

        if is_retour_selected:
            sel_surf = pygame.Surface((box_width - 40, 42), pygame.SRCALPHA)
            sel_surf.fill((255, 200, 0, 80))
            screen.blit(sel_surf, (box_x + 20, retour_y))

        retour_color = YELLOW if is_retour_selected else WHITE
        retour_text = self.font_menu.render("Retour", True, retour_color)
        # Centrer verticalement le texte dans la bande de selection
        text_y = retour_y + (42 - retour_text.get_height()) // 2
        screen.blit(retour_text, (col1_x, text_y))

        # Message si en attente de touche
        if self.waiting_for_key:
            msg = self.font_small.render("Appuyez sur une touche... (ECHAP pour annuler)", True, RED)
            msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT - 80))
            screen.blit(msg, msg_rect)
        else:
            self._draw_instructions(screen, "Naviguer  |  ENTREE Modifier  |  ECHAP Retour")

    def _draw_instructions(self, screen, text):
        """Dessine les instructions en bas de l'ecran"""
        # Fond semi-transparent
        inst_surf = pygame.Surface((WIDTH, 50), pygame.SRCALPHA)
        inst_surf.fill((0, 0, 0, 150))
        screen.blit(inst_surf, (0, HEIGHT - 50))

        inst_text = self.font_small.render(text, True, WHITE)
        inst_rect = inst_text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
        screen.blit(inst_text, inst_rect)

    def _draw_character_select(self, screen):
        """Dessine l'ecran de selection de personnage"""
        # Titre avec effet
        title_text = self.font_title.render("CHOISIS TON GUITARISTE", True, YELLOW)
        shadow_text = self.font_title.render("CHOISIS TON GUITARISTE", True, (50, 30, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 80))
        screen.blit(shadow_text, title_rect.move(4, 4))
        screen.blit(title_text, title_rect)

        # Personnages
        p1_x = WIDTH // 3
        p2_x = (WIDTH // 5) * 3
        char_y = HEIGHT // 2 - 20

        self._draw_character_option(screen, 1, p1_x, char_y, self.player1_img, "Axel")
        self._draw_character_option(screen, 2, p2_x, char_y, self.player2_img, "Luna")

        # VS au milieu
        # vs_pulse = 1.0 + math.sin(self.anim_time * 4) * 0.1
        # try:
        #     vs_font = pygame.font.Font(str(FONT_METAL_MANIA), int(60 * vs_pulse))
        # except (pygame.error, FileNotFoundError):
        #     vs_font = pygame.font.Font(None, int(60 * vs_pulse))
        # vs_text = vs_font.render("VS", True, RED)
        # vs_rect = vs_text.get_rect(center=(WIDTH // 2, char_y))
        # screen.blit(vs_text, vs_rect)

        self._draw_instructions(screen, "Choisir  |  ENTREE Valider  |  ECHAP Retour")

    def _draw_character_option(self, screen, char_num, x, y, image, name):
        """Dessine une option de personnage avec animations rock"""
        is_selected = self.selected_character == char_num

        img_width = PLAYER_WIDTH * 2
        img_height = PLAYER_HEIGHT * 2

        # Animation
        offset_y = 0
        rotation = 0
        scale_bonus = 0
        if is_selected:
            headbang = math.sin(self.anim_time * 8) * 3
            offset_y = abs(headbang)
            rotation = math.sin(self.anim_time * 6) * 5
            scale_bonus = abs(math.sin(self.anim_time * 4)) * 0.08

        char_y = y + offset_y

        # Cadre
        padding = 20
        frame_rect = pygame.Rect(
            x - img_width // 2 - padding,
            y - img_height // 2 - padding,
            img_width + padding * 2,
            img_height + padding * 2
        )

        if is_selected:
            # Effet de glow
            for i in range(3):
                glow_offset = i * 3
                glow_alpha = 100 - i * 30
                glow_surf = pygame.Surface((frame_rect.width + glow_offset * 2, frame_rect.height + glow_offset * 2), pygame.SRCALPHA)
                glow_color = (255, 150, 0, glow_alpha)
                pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=15)
                screen.blit(glow_surf, (frame_rect.x - glow_offset, frame_rect.y - glow_offset))

            # Cadre principal
            frame_color = (255, int(150 + math.sin(self.anim_time * 8) * 105), 0)
            pygame.draw.rect(screen, frame_color, frame_rect, 5, border_radius=12)
        else:
            pygame.draw.rect(screen, GRAY, frame_rect, 2, border_radius=12)

        # Image
        if image:
            if is_selected:
                new_width = int(img_width * (1 + scale_bonus))
                new_height = int(img_height * (1 + scale_bonus))
                scaled_img = pygame.transform.scale(image, (new_width, new_height))
                rotated_img = pygame.transform.rotate(scaled_img, rotation)
                img_rect = rotated_img.get_rect(center=(x, char_y))
                screen.blit(rotated_img, img_rect)
            else:
                img_rect = image.get_rect(center=(x, y))
                screen.blit(image, img_rect)
        else:
            placeholder_color = PURPLE if char_num == 1 else ORANGE
            placeholder_rect = pygame.Rect(x - img_width // 2, char_y - img_height // 2, img_width, img_height)
            pygame.draw.rect(screen, placeholder_color, placeholder_rect, border_radius=5)

        # Nom
        name_y = frame_rect.bottom + 30
        if is_selected:
            name_scale = 1.0 + abs(math.sin(self.anim_time * 6)) * 0.15
            try:
                rock_font = pygame.font.Font(str(FONT_METAL_MANIA), int(40 * name_scale))
            except (pygame.error, FileNotFoundError):
                rock_font = self.font_menu
            name_text = rock_font.render(name, True, YELLOW)
        else:
            name_text = self.font_menu.render(name, True, WHITE)
        name_rect = name_text.get_rect(center=(x, name_y))
        screen.blit(name_text, name_rect)
