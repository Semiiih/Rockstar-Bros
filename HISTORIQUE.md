# Historique du Projet Rockstar Bros

## Jour 1

### Structure du projet creee
- **main.py** : Boucle de jeu principale et gestion des scenes
- **settings.py** : Toutes les constantes du jeu centralisees (ecran, physique, joueur, ennemis, etc.)
- **scenes/base.py** : Classe abstraite Scene pour l'interface commune
- **scenes/menu.py** : Menu principal avec selection de personnage (Axel/Luna)
- **scenes/gameplay.py** : Coeur du jeu (joueur, ennemis, projectiles, collisions)
- **scenes/pause.py** : Menu de pause
- **scenes/game_over.py** : Ecran de game over
- **scenes/victory.py** : Ecran de victoire
- **assets/** : Structure des dossiers pour images et sons

### Systeme de combat
- **Attaque normale [J]** : Projectile simple sans timing
- **Attaque ultime [K]** : Sequence Guitar Hero avec notes qui tombent
  - 3 pistes (touches F, G, H)
  - Systeme de timing : PERFECT / GOOD / OK / MISS
  - Plus de PERFECT = plus de degats
  - Le jeu se fige pendant la sequence ultime

### Ennemis implementes
- **Hater** : Ennemi de base (2 PV, poursuit le joueur)
- **Rival** : Ennemi plus fort (3 PV, plus rapide)
- **Boss** : Boss final (20 PV, plusieurs phases, lance des projectiles)

### Systeme audio
- Musique du menu (menu_music.wav)
- Musique du niveau 1 (level1_music.wav)
- Musique du niveau 2 (level2_music.wav)
- Musique du boss (boss_music.wav)

### Corrections de bugs
- Fix du lancement du jeu (main.py n'appelait pas main())
- Fix import DARK_GRAY manquant
- Fix methode _update_beat_pulse qui n'existait plus

### Ameliorations gameplay
- Les ennemis ne peuvent plus se chevaucher entre eux
- Les plateformes chargent leurs images (platform.png, ground.png)
- Ajout de trous/pieges dans les niveaux
- Le joueur et les ennemis peuvent tomber dans le vide et mourir
- Suppression du "sol invisible" pour permettre les chutes

### Images des ecrans
- **home.png** : Ecran d'accueil/menu
- **gameover.png** : Ecran de game over
- **pause.png** : Ecran de pause
- **win.png** : Ecran de victoire

### Assets ajoutes
- Images ennemis : hater_idle.png, rival_idle.png, boss_idle.png, boss_attack.png
- Images plateformes : platform.png, platform_small.png, ground.png
- Images UI : heart_full.png, heart_empty.png

### Niveaux
- **Niveau 1 (Coulisses)** : Tutoriel avec quelques trous et Haters
- **Niveau 2 (Scene)** : Plus difficile avec trous et Rivals
- **Niveau 3 (Boss Arena)** : Combat contre le Boss final

### Controles
- **Fleches / WASD** : Deplacement
- **Espace** : Saut
- **J** : Attaque normale
- **K** : Attaque ultime (quand la jauge est pleine)
- **F, G, H** : Touches pour la sequence Guitar Hero de l'ultime
- **Echap** : Pause
- **F1** : Debug hitboxes
- **F2** : Skip niveau
- **F3** : Mode invincible
