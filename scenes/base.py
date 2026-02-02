"""
Rockstar Bros - Classe de base pour les scenes
Interface commune pour toutes les scenes du jeu
"""

from abc import ABC, abstractmethod


class Scene(ABC):
    """
    Cssant l'interface commune lasse abstraite definia toutes les scenes.
    Chaque scene doit implementer: handle_event, update, draw
    """

    def __init__(self, game):
        """
        Initialise la scene avec une reference au jeu principal.

        Args:
            game: Instance de la classe Game (pour acceder aux donnees partagees)
        """
        self.game = game

    def enter(self, **kwargs):
        """
        Appelee quand on entre dans cette scene.
        Peut etre surchargee pour initialiser des elements specifiques.

        Args:
            **kwargs: Arguments optionnels passes lors du changement de scene
        """
        pass

    def exit(self):
        """
        Appelee quand on quitte cette scene.
        Peut etre surchargee pour nettoyer des ressources.
        """
        pass

    @abstractmethod
    def handle_event(self, event):
        """
        Gere un evenement pygame.

        Args:
            event: Evenement pygame a traiter
        """
        pass

    @abstractmethod
    def update(self, dt):
        """
        Met a jour la logique de la scene.

        Args:
            dt: Delta time en secondes depuis la derniere frame
        """
        pass

    @abstractmethod
    def draw(self, screen):
        """
        Dessine la scene a l'ecran.

        Args:
            screen: Surface pygame sur laquelle dessiner
        """
        pass
