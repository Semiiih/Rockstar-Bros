"""
Rockstar Bros - Point d'entree principal
Gestion de la boucle de jeu et des scenes
"""

import pygame
import sys
from settings import (
    WIDTH, HEIGHT, FPS, TITLE, BG_COLOR,
    STATE_MENU, STATE_GAMEPLAY, STATE_PAUSE,
    STATE_GAME_OVER, STATE_VICTORY
)
from scenes.menu import MenuScene
from scenes.gameplay import GameplayScene
from scenes.pause import PauseScene
from scenes.game_over import GameOverScene
from scenes.victory import VictoryScene


# Duree de la transition en millisecondes
TRANSITION_DURATION = 1200


class Game:
    """Classe principale du jeu - gere la boucle et les scenes"""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Donnees partagees entre scenes
        self.game_data = {
            "selected_character": 1,
            "current_level": 1,
            "score": 0,
            "lives": 3,
            "ultimate_charge": 0,
        }

        # Scenes disponibles
        self.scenes = {}
        self.current_scene = None
        self._init_scenes()

        # Systeme de transition
        self.transitioning = False
        self.transition_timer = 0
        self.transition_from_surface = None
        self.transition_to_surface = None
        self.pending_scene = None
        self.pending_kwargs = {}

        # Commencer par le menu (sans transition)
        self._change_scene_immediate(STATE_MENU)

    def _init_scenes(self):
        """Initialise toutes les scenes du jeu"""
        self.scenes[STATE_MENU] = MenuScene(self)
        self.scenes[STATE_GAMEPLAY] = GameplayScene(self)
        self.scenes[STATE_PAUSE] = PauseScene(self)
        self.scenes[STATE_GAME_OVER] = GameOverScene(self)
        self.scenes[STATE_VICTORY] = VictoryScene(self)

    def _change_scene_immediate(self, scene_name, **kwargs):
        """Change la scene immediatement sans transition"""
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            self.current_scene.enter(**kwargs)

    def change_scene(self, scene_name, **kwargs):
        """Change la scene avec transition slide"""
        if scene_name in self.scenes and not self.transitioning:
            # Capturer l'ecran actuel
            self.transition_from_surface = self.screen.copy()

            # Preparer la nouvelle scene
            self.pending_scene = scene_name
            self.pending_kwargs = kwargs

            # Activer la nouvelle scene pour la dessiner
            new_scene = self.scenes[scene_name]
            new_scene.enter(**kwargs)

            # Capturer l'ecran de la nouvelle scene
            self.transition_to_surface = pygame.Surface((WIDTH, HEIGHT))
            self.transition_to_surface.fill(BG_COLOR)
            new_scene.draw(self.transition_to_surface)

            # Demarrer la transition
            self.transitioning = True
            self.transition_timer = 0
            self.current_scene = new_scene

    def _update_transition(self, dt_ms):
        """Met a jour l'animation de transition"""
        self.transition_timer += dt_ms

        if self.transition_timer >= TRANSITION_DURATION:
            # Transition terminee
            self.transitioning = False
            self.transition_from_surface = None
            self.transition_to_surface = None

    def _draw_transition(self):
        """Dessine l'effet de transition diagonale avec bande blanche"""
        progress = min(self.transition_timer / TRANSITION_DURATION, 1.0)

        # Easing ease in-out pour un mouvement fluide
        if progress < 0.5:
            eased = 2 * progress * progress
        else:
            eased = 1 - ((-2 * progress + 2) ** 2) / 2

        # La ligne diagonale se deplace de droite a gauche
        # Position X de la separation (de WIDTH + HEIGHT a -HEIGHT)
        total_travel = WIDTH + HEIGHT * 2
        split_x = int(WIDTH + HEIGHT - eased * total_travel)

        # D'abord dessiner la nouvelle scene en entier
        if self.transition_to_surface:
            self.screen.blit(self.transition_to_surface, (0, 0))

        # Puis dessiner l'ancienne scene avec un clip diagonal (partie gauche)
        if self.transition_from_surface:
            # Points du polygone pour l'ancienne scene (partie gauche)
            clip_points = [
                (0, 0),
                (split_x, 0),
                (split_x - HEIGHT, HEIGHT),
                (0, HEIGHT),
            ]
            pygame.draw.polygon(self.screen, (0, 0, 0), clip_points)  # Fond noir temporaire

            # Dessiner l'ancienne scene pixel par pixel dans la zone
            for y in range(HEIGHT):
                # Calculer la limite X pour cette ligne
                x_limit = split_x - y
                if x_limit > 0:
                    # Copier la ligne de l'ancienne surface
                    line_rect = pygame.Rect(0, y, min(x_limit, WIDTH), 1)
                    self.screen.blit(self.transition_from_surface, (0, y), line_rect)

        # Dessiner la bande blanche diagonale (separateur)
        band_width = 6
        band_points = [
            (split_x - band_width, 0),
            (split_x + band_width, 0),
            (split_x - HEIGHT + band_width, HEIGHT),
            (split_x - HEIGHT - band_width, HEIGHT),
        ]
        pygame.draw.polygon(self.screen, (255, 255, 255), band_points)

        # Deuxieme bande blanche pour epaissir
        band_points2 = [
            (split_x - band_width - 3, 0),
            (split_x - band_width, 0),
            (split_x - HEIGHT - band_width, HEIGHT),
            (split_x - HEIGHT - band_width - 3, HEIGHT),
        ]
        pygame.draw.polygon(self.screen, (220, 220, 220), band_points2)

    def reset_game(self):
        """Reinitialise les donnees du jeu pour une nouvelle partie"""
        self.game_data["current_level"] = 1
        self.game_data["score"] = 0
        self.game_data["lives"] = 3
        self.game_data["ultimate_charge"] = 0
        # Recreer la scene gameplay pour reset complet
        self.scenes[STATE_GAMEPLAY] = GameplayScene(self)

    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            # Delta time en secondes
            dt = self.clock.tick(FPS) / 1000.0
            dt_ms = dt * 1000

            # Gestion des evenements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif not self.transitioning:
                    # Ne pas traiter les events pendant la transition
                    if self.current_scene:
                        self.current_scene.handle_event(event)

            # Mise a jour
            if self.transitioning:
                self._update_transition(dt_ms)
            elif self.current_scene:
                self.current_scene.update(dt)

            # Rendu
            if self.transitioning:
                self._draw_transition()
            else:
                self.screen.fill(BG_COLOR)
                if self.current_scene:
                    self.current_scene.draw(self.screen)

            pygame.display.flip()

        self.quit()

    def quit(self):
        """Ferme proprement le jeu"""
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
