"""
Rockstar Bros - Scene de pause
Menu de pause identique au menu principal avec Reprendre, Touches, Quitter
"""

import pygame
import math
from scenes.base import Scene
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, GRAY, BLACK, ORANGE, RED,
    STATE_GAMEPLAY, STATE_MENU, CONTROLS,
    IMG_DIR, IMG_PAUSE,
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


class PauseScene(Scene):
    """Scene de pause du jeu - identique au menu principal"""

    def __init__(self, game):
        super().__init__(game)
        self.font_title = None
        self.font_menu = None
        self.font_small = None

        # Etat du menu: "main" ou "controls"
        self.menu_state = "main"
        self.selected_option = 0
        self.main_options = ["Reprendre", "Touches", "Quitter"]

        # Configuration des touches
        self.controls_selected = 0
        self.waiting_for_key = False
        self.key_to_change = None

        # Background pause
        self.background = None
        self.game_screenshot = None

        # Animation
        self.anim_time = 0

    def enter(self, **kwargs):
        """Initialisation a l'entree dans la pause"""
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
        self.controls_selected = 0
        self.waiting_for_key = False
        self.anim_time = 0

        # Charger l'image de pause ou capturer l'ecran
        try:
            bg_path = IMG_DIR / IMG_PAUSE
            self.background = pygame.image.load(str(bg_path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError):
            self.background = None
            self.game_screenshot = self.game.screen.copy()

    def handle_event(self, event):
        """Gere les evenements du menu pause"""
        if event.type == pygame.KEYDOWN:
            # Attente d'une touche pour la configuration
            if self.waiting_for_key:
                self._set_new_key(event.key)
                return

            if self.menu_state == "main":
                self._handle_main_menu(event)
            elif self.menu_state == "controls":
                self._handle_controls(event)

    def _handle_main_menu(self, event):
        """Gere les inputs du menu principal pause"""
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.main_options)
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.main_options)
        elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
            if self.selected_option == 0:  # Reprendre
                self.game.change_scene(STATE_GAMEPLAY)
            elif self.selected_option == 1:  # Touches
                self.menu_state = "controls"
                self.controls_selected = 0
            elif self.selected_option == 2:  # Quitter
                self.game.change_scene(STATE_MENU)
        elif event.key == pygame.K_ESCAPE:
            # Echap pour reprendre directement
            self.game.change_scene(STATE_GAMEPLAY)

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
                self.menu_state = "main"
                self.selected_option = 0
        elif event.key == pygame.K_ESCAPE:
            self.menu_state = "main"
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
        """Mise a jour de l'animation"""
        self.anim_time += dt

    def _draw_arrow(self, screen, x, y, color=YELLOW):
        """Dessine une fleche de selection (triangle)"""
        arrow_size = 12
        points = [
            (x, y - arrow_size // 2),
            (x, y + arrow_size // 2),
            (x + arrow_size, y)
        ]
        pygame.draw.polygon(screen, color, points)

    def _draw_arrow_right(self, screen, x, y, color=YELLOW):
        """Dessine une fleche vers la gauche"""
        points = [(x, y - 8), (x, y + 8), (x - 12, y)]
        pygame.draw.polygon(screen, color, points)

    def draw(self, screen):
        """Dessine le menu pause"""
        # Background
        if self.background:
            screen.blit(self.background, (0, 0))
        elif self.game_screenshot:
            screen.blit(self.game_screenshot, (0, 0))
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

        if self.menu_state == "main":
            self._draw_main_menu(screen)
        elif self.menu_state == "controls":
            self._draw_controls(screen)

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

    def _draw_main_menu(self, screen):
        """Dessine le menu principal pause"""
        # Titre PAUSE avec effet
        title_text = self.font_title.render("PAUSE", True, YELLOW)
        shadow_text = self.font_title.render("PAUSE", True, (50, 30, 0))
        title_rect = title_text.get_rect(center=(WIDTH // 2, 130))
        screen.blit(shadow_text, title_rect.move(4, 4))
        screen.blit(title_text, title_rect)

        # Boite de menu
        self._draw_menu_box(screen, "MENU PAUSE", self.main_options, self.selected_option)

        # Instructions en bas
        self._draw_instructions(screen, "↑↓ Naviguer  |  ENTREE Valider  |  ECHAP Reprendre")

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

        # Colonnes
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

        # Option Retour
        retour_y = box_y + header_height + num_actions * row_height + 10
        is_retour_selected = self.controls_selected == num_actions

        if is_retour_selected:
            sel_surf = pygame.Surface((box_width - 40, 42), pygame.SRCALPHA)
            sel_surf.fill((255, 200, 0, 80))
            screen.blit(sel_surf, (box_x + 20, retour_y))

        retour_color = YELLOW if is_retour_selected else WHITE
        retour_text = self.font_menu.render("Retour", True, retour_color)
        text_y = retour_y + (42 - retour_text.get_height()) // 2
        screen.blit(retour_text, (col1_x, text_y))

        # Message si en attente de touche
        if self.waiting_for_key:
            msg = self.font_small.render("Appuyez sur une touche... (ECHAP pour annuler)", True, RED)
            msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT - 80))
            screen.blit(msg, msg_rect)
        else:
            self._draw_instructions(screen, "↑↓ Naviguer  |  ENTREE Modifier  |  ECHAP Retour")

    def _draw_instructions(self, screen, text):
        """Dessine les instructions en bas de l'ecran"""
        inst_surf = pygame.Surface((WIDTH, 50), pygame.SRCALPHA)
        inst_surf.fill((0, 0, 0, 150))
        screen.blit(inst_surf, (0, HEIGHT - 50))

        inst_text = self.font_small.render(text, True, WHITE)
        inst_rect = inst_text.get_rect(center=(WIDTH // 2, HEIGHT - 25))
        screen.blit(inst_text, inst_rect)
