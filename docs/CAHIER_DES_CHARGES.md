# Cahier des charges - Rockstar Bros

## 1. Concept

**Genre** : Plateforme 2D (side-scroller)  
**Inspiration** : Mario (sauts, plateformes, ennemis simples)  
**Twist Guitar Hero** : Le héros attaque avec des ondes musicales / riffs, et certaines actions sont rythmées (bonus si timing correct)

### Pitch
Tu incarnes un guitariste qui traverse une scène géante (coulisses → scène → finale). Tu élimines des perturbateurs (stress, huées, pannes) en lançant des riffs. À la fin : boss (le "Hater King" / "Manager tyrannique" / "Monstre de feedback").

---

## 2. Loop de gameplay

Ce que le joueur fait en continu :
1. **Avancer** → **sauter** → **éviter chutes/pièges**
2. **Combattre** des ennemis avec attaque musicale
3. **Ramasser** des bonus (notes, médiators, amplis)
4. **Atteindre** un checkpoint
5. **Boss final** + victoire

---

## 3. Contrôles

### Commandes principales
- **Gauche/Droite** (←/→) : Déplacement
- **Saut** : `ESPACE`
- **Attaque musicale** : `J` (ou `K`)
- **Attaque ultime** : `K` (après jauge remplie grâce à des bonus)
- **Pause** : `ESC`

### Commandes développement (debug)
- `F1` : Afficher hitboxes
- `F2` : Skip niveau
- `F3` : Mode invincible

---

## 4. Mouvements & physique (simple mais propre)

### Joueur
- **Gravité** + vitesse verticale
- **Détection collision** sol/plateformes
- **Animation simple** (même 2 frames suffisent)
- **2 personnages** sélectionnables

### Environnements
- **Plateformes fixes** (rectangles)
- **1-2 plateformes mobiles** (optionnel)

**Règle d'or** : Collisions rectangulaires simples (AABB), pas de moteur compliqué.

---

## 5. Système d'attaque "musicale"

### Attaque de base
- **Projectile "onde sonore"** (petit cercle/rectangle) qui part vers l'avant
- **Cooldown** (ex : 0,35 s)
- **Dégâts fixes**

### Bonus "rythme" (facultatif mais stylé)
- Un **métronome interne** (ex : 120 BPM)
- Si tu attaques proche du beat :
  - **+ dégâts** OU projectile plus rapide OU + score

**Important** : Ce système doit être **visible à l'écran** grâce à une barre inspirée de Guitar Hero.

(Même sans audio : tu peux simuler le beat avec un timer.)

---

## 6. Ennemis

### Ennemis de base (2 types suffisants)

1. **Hater** : Marche vers toi lentement
2. **Autre rockstar** : Plus résistant

### Comportements simples
- **Patrouille** gauche/droite
- **Suit le joueur** si proche
- **Prend des dégâts** quand touché par une onde
  - Hater : **2 coups** pour mourir
  - Rockstar : **3 coups** pour mourir
- **Contact = dégâts** au joueur

---

## 7. Système de vie / UI

### Vie
- **Joueur** : 3 cœurs (représentés par des **guitares**)
- **Ennemis** :
  - Hater : 2 PV
  - Rockstar : 3 PV

### UI en haut de l'écran
- **Vie** (guitares)
- **Score**
- **Combo** (si rythme activé)
- **Métronome Guitar Hero** (barre avec curseur)

---

## 8. Collectibles & progression

### Collectibles
- **Médiators** : Attaque spéciale (option)
- **Notes musicales** : Points bonus
- **Amplis** : Boost temporaire

### Checkpoints
- **1 checkpoint par niveau** (reprise si mort)

---

## 9. Niveaux (scope réaliste)

### Niveau 1 : Tutoriel (Coulisses)
- Plateformes faciles
- 1 type d'ennemi (Hater)
- 1 checkpoint

### Niveau 2 : Challenge (Scène)
- Plus vertical
- 2 types d'ennemis (Hater + Rockstar)
- Pièges (chutes, obstacles mobiles)

### Niveau 3 : Boss (Arène)
- Petite arène fermée
- Boss final : **Rockstar concurrente**

---

## 10. Boss final (simple mais impressionnant)

**Boss** : "Rockstar concurrente"

### Stats
- **PV : 20** (par exemple)

### Phases d'attaque
1. **Tire des projectiles** (ex : "mots toxiques" / "boules de bruit")
2. **Saute et provoque une onde de choc au sol**

### Stratégie joueur
Le joueur gagne en :
- **Évitant** les attaques
- **Attaquant** au bon timing (système rythme)

**Win condition** : PV boss = 0 → écran victoire  
**Lose condition** : Vie joueur = 0 → game over

---

## 11. Écrans (états du jeu)

1. **Menu** (Play / Quit)
2. **Choix personnage** (optionnel, peut être dans menu)
3. **Jeu** (gameplay)
4. **Pause** (Resume / Quit)
5. **Game Over** (Retry / Menu)
6. **Victoire** (Score final / Menu)

---

## 12. Structure de code (propre, piscine-friendly)

Voir fichier `piscine_presentation.pdf` pour la structure recommandée.

### Principe POO
```
main.py          # Chef d'orchestre (boucle + scènes)
settings.py      # Constantes globales
scenes/          # États du jeu (menu, gameplay, pause, etc.)
  base.py        # Classe Scene (interface)
  menu.py        # Menu principal
  gameplay.py    # Cœur du jeu
  game_over.py   # Écran défaite
  victory.py     # Écran victoire
entities/        # Entités (optionnel si gameplay.py pas trop gros)
  player.py
  enemies.py
  boss.py
assets/          # Ressources
  images/
  sounds/
```

---

## 13. Critères de réussite

### Obligatoires ✅
- Jouable du début à la fin
- Thème Guitar Hero visible (perso, scène, attaques, ennemis)
- Contrôles responsifs
- Aucun bug bloquant (chutes infinies, collision cassée)
- Code clair + constantes centralisées + commenté

### Bonus ⭐
- 2 personnages jouables
- Système rythme/combo fonctionnel avec feedback visuel
- Boss avec plusieurs phases distinctes
- Animations fluides
- Sons immersifs (musique + SFX)

---

## 14. Direction artistique (simple mais efficace)

### Décor
- **Scène** : amplis, lumières, public (silhouettes)
- **Plateformes** : caisses, enceintes, flight cases
- **Ennemis** : "huées" (bulles), rockstars rivaux

### Style
- Pixel art rétro (conseillé pour rapidité)
- Couleurs vives et contrastées
- Thème musical omniprésent

---

## 15. Timeline de développement (5 jours)

### Jour 1 : Fondations
- Structure projet (main.py, settings.py, scenes/)
- Joueur qui bouge + saute
- Gravité fonctionnelle
- 1 plateforme
- Assets placeholder (rectangles)

### Jour 2 : Mécanique combat
- Attaque de base (projectile)
- 1 ennemi Hater (patrouille)
- Collisions joueur-ennemi-projectile
- Système vie basique
- Barre Guitar Hero (visuel minimal)

### Jour 3 : Contenu
- Système rythme complet (bonus dégâts)
- 3 niveaux (3 backgrounds + layouts)
- Boss avec phases simples
- Remplacement assets placeholder par sprites

### Jour 4 : UI/UX + Sons
- UI/HUD complet (vie, score, combo)
- Sons (attaque, hit, musique)
- Écrans menu/pause/game_over/victory
- Polish et corrections bugs

### Jour 5 : Finalisation
- Tests complets (tous niveaux jouables)
- Préparation démo
- Préparation soutenance orale
- **Rendu code : Lundi 9 février 9h**

---

## 16. Assets à produire (résumé)

### Minimum vital (MVP)
**~15 images** :
- Joueur (idle + run) × 2 persos = 4
- 1 ennemi (idle) = 1
- Projectile = 1
- Plateforme = 1
- Background simple = 1
- UI vie (guitare pleine/vide) = 2
- Barre Guitar Hero = 2
- Écrans texte (menu/gameover) = 2

### Complet (objectif)
**35-40 images** :
- Héros 1 (5 images : idle, run×2, jump, attack)
- Héros 2 (5 images)
- Hater (idle + hit)
- Rockstar (idle + hit)
- Boss (idle + attack + projectile + shockwave)
- 3 plateformes types
- 3 backgrounds (coulisses, scène, arène)
- Collectibles (3)
- UI complète (5)
- Écrans (4)

**Sons (non bloquants)** :
- Musiques (menu, niveaux, boss) = 4
- SFX (jump, attack, hit, collect) = 6

---

## 17. Contraintes techniques

### Performances
- **60 FPS** constant
- Pas de lag lors des collisions multiples
- Chargement assets au démarrage (pas en runtime)

### Compatibilité
- Python 3.8+
- Pygame 2.x
- Pas de dépendances externes complexes

### Code
- **POO** : Classes pour entités
- **Constantes** : Centralisées dans settings.py
- **Commentaires** : Sur parties complexes
- **Nommage** : Clair et en anglais (variables, fonctions, classes)

---

## 18. Livrables attendus

### Code
- Repo complet fonctionnel
- README.md avec instructions installation/lancement
- Tous les fichiers nécessaires (code + assets)

### Soutenance (Jour 5)
- **Démo en direct** du jeu (5-7 min)
- **Présentation technique** (architecture, choix design)
- **Réponses aux questions** du jury

### Documents
- Ce cahier des charges (référence)
- Documentation code (si temps)

---

## 19. Critères de notation

### Fonctionnalités (40%)
- Jouabilité complète (début → fin)
- Mécanique Guitar Hero présente et visible
- 3 niveaux distincts
- Boss fonctionnel

### Technique (30%)
- Structure code propre (POO, scènes)
- Pas de bugs bloquants
- Performance (60 FPS stable)
- Code commenté et lisible

### Créativité (20%)
- Originalité gameplay rythme
- Direction artistique cohérente
- Polish (animations, sons, UI)

### Présentation (10%)
- Clarté démo
- Qualité présentation orale
- Réponses questions jury

---

## 20. Conseils finaux

### Priorités
1. **Gameplay fonctionnel** > Graphismes
2. **Mécanique unique** (rythme) bien visible
3. **Stabilité** > Features supplémentaires

### Pièges à éviter
- Vouloir trop de contenu (3 niveaux suffisent)
- Négliger le système rythme (c'est le twist principal)
- Passer trop de temps sur les assets (placeholders OK)
- Coder sans plan (respecter architecture proposée)

### Atouts pour la démo
- Jeu jouable en entier
- Système Guitar Hero bien visible et compréhensible
- Au moins 1 son (musique ou SFX) pour immersion
- Code propre avec constantes dans settings.py

---

**Bonne chance ! 🎸🎮**