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
        }

        # Scenes disponibles
        self.scenes = {}
        self.current_scene = None
        self._init_scenes()

        # Commencer par le menu
        self.change_scene(STATE_MENU)

    def _init_scenes(self):
        """Initialise toutes les scenes du jeu"""
        self.scenes[STATE_MENU] = MenuScene(self)
        self.scenes[STATE_GAMEPLAY] = GameplayScene(self)
        self.scenes[STATE_PAUSE] = PauseScene(self)
        self.scenes[STATE_GAME_OVER] = GameOverScene(self)
        self.scenes[STATE_VICTORY] = VictoryScene(self)

    def change_scene(self, scene_name, **kwargs):
        """Change la scene active"""
        if scene_name in self.scenes:
            self.current_scene = self.scenes[scene_name]
            self.current_scene.enter(**kwargs)

    def reset_game(self):
        """Reinitialise les donnees du jeu pour une nouvelle partie"""
        self.game_data["current_level"] = 1
        self.game_data["score"] = 0
        self.game_data["lives"] = 3
        # Recreer la scene gameplay pour reset complet
        self.scenes[STATE_GAMEPLAY] = GameplayScene(self)

    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            # Delta time en secondes
            dt = self.clock.tick(FPS) / 1000.0

            # Gestion des evenements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    if self.current_scene:
                        self.current_scene.handle_event(event)

            # Mise a jour
            if self.current_scene:
                self.current_scene.update(dt)

            # Rendu
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
