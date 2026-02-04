"""
Level Loader - Charge les configurations de niveaux depuis JSON
"""

import json
import os
from typing import Dict, List, Optional


class LevelLoader:
    """Charge et gere les configurations de niveaux depuis les fichiers JSON"""

    def __init__(self, levels_dir: str = "levels"):
        """
        Initialize le loader

        Args:
            levels_dir: Dossier contenant les fichiers JSON des niveaux
        """
        self.levels_dir = levels_dir
        self.levels_cache: Dict[int, dict] = {}

    def load_level(self, level_id: int) -> Optional[dict]:
        """
        Charge un niveau depuis son fichier JSON

        Args:
            level_id: ID du niveau a charger

        Returns:
            Dictionnaire contenant toute la config du niveau, ou None si erreur
        """
        # Verifier le cache
        if level_id in self.levels_cache:
            return self.levels_cache[level_id]

        # Charger depuis le fichier
        filename = f"level_{level_id}.json"
        filepath = os.path.join(self.levels_dir, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                level_data = json.load(f)

            # Valider que l'ID correspond
            if level_data.get('id') != level_id:
                print(f"Warning: level_id mismatch in {filename}")

            # Mettre en cache
            self.levels_cache[level_id] = level_data
            return level_data

        except FileNotFoundError:
            print(f"Error: Level file not found: {filepath}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in {filepath}: {e}")
            return None

    def get_stage(self, level_id: int, stage_id: int) -> Optional[dict]:
        """
        Recupere un stage specifique d'un niveau

        Args:
            level_id: ID du niveau
            stage_id: ID du stage (1, 2 ou 3)

        Returns:
            Dictionnaire du stage, ou None si non trouve
        """
        level_data = self.load_level(level_id)
        if not level_data:
            return None

        stages = level_data.get('stages', [])
        for stage in stages:
            if stage.get('stage_id') == stage_id:
                return stage

        print(f"Error: Stage {stage_id} not found in level {level_id}")
        return None

    def get_all_levels(self) -> List[dict]:
        """
        Charge tous les niveaux disponibles

        Returns:
            Liste des configurations de tous les niveaux
        """
        levels = []

        # Scanner le dossier levels pour trouver tous les fichiers level_X.json
        if not os.path.exists(self.levels_dir):
            print(f"Error: Levels directory not found: {self.levels_dir}")
            return levels

        for filename in os.listdir(self.levels_dir):
            if filename.startswith('level_') and filename.endswith('.json'):
                # Extraire l'ID du nom de fichier
                try:
                    level_id = int(filename.replace('level_', '').replace('.json', ''))
                    level_data = self.load_level(level_id)
                    if level_data:
                        levels.append(level_data)
                except ValueError:
                    continue

        # Trier par ID
        levels.sort(key=lambda x: x.get('id', 0))
        return levels

    def is_level_unlocked(self, level_id: int, completed_levels: List[int]) -> bool:
        """
        Verifie si un niveau est debloque

        Args:
            level_id: ID du niveau a verifier
            completed_levels: Liste des IDs de niveaux completes

        Returns:
            True si le niveau est debloque
        """
        level_data = self.load_level(level_id)
        if not level_data:
            return False

        unlock_condition = level_data.get('unlock_condition')

        # Pas de condition = toujours debloque
        if unlock_condition is None:
            return True

        # Si c'est un ID de niveau, verifier qu'il est complete
        if isinstance(unlock_condition, int):
            return unlock_condition in completed_levels

        return False

    def get_level_rewards(self, level_id: int) -> Optional[dict]:
        """
        Recupere les recompenses d'un niveau

        Args:
            level_id: ID du niveau

        Returns:
            Dictionnaire des recompenses (completion_score, stars_thresholds)
        """
        level_data = self.load_level(level_id)
        if not level_data:
            return None

        return level_data.get('rewards', {})

    def get_stars_count(self, level_id: int, score: int) -> int:
        """
        Calcule le nombre d'etoiles gagnees selon le score

        Args:
            level_id: ID du niveau
            score: Score obtenu

        Returns:
            Nombre d'etoiles (0-3)
        """
        rewards = self.get_level_rewards(level_id)
        if not rewards:
            return 0

        thresholds = rewards.get('stars_thresholds', [])
        stars = 0

        for threshold in thresholds:
            if score >= threshold:
                stars += 1

        return min(stars, 3)  # Maximum 3 etoiles


# Instance globale pour faciliter l'acces
_loader = None

def get_loader() -> LevelLoader:
    """Retourne l'instance globale du loader"""
    global _loader
    if _loader is None:
        _loader = LevelLoader()
    return _loader
