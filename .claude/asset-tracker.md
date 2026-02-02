# Asset Tracker - Rockstar Bros

## Vue d'ensemble

**Total estimé** : 35-40 images
**Statut actuel** : 0/40 créés

---

## 1. PERSONNAGES JOUEURS (10 images) - PRIORITÉ HAUTE

### Hero 1 (Personnage A)
- [ ] `hero1_idle.png` - Pose repos (64×64px)
- [ ] `hero1_run_1.png` - Course frame 1
- [ ] `hero1_run_2.png` - Course frame 2
- [ ] `hero1_jump.png` - En l'air
- [ ] `hero1_attack.png` - Attaque (optionnel si temps)

### Hero 2 (Personnage B)
- [ ] `hero2_idle.png` - Pose repos (64×64px)
- [ ] `hero2_run_1.png` - Course frame 1
- [ ] `hero2_run_2.png` - Course frame 2
- [ ] `hero2_jump.png` - En l'air
- [ ] `hero2_attack.png` - Attaque (optionnel si temps)

**Placeholder temporaire** :
```python
# Rectangle bleu pour Hero 1
surface.fill((50, 150, 255))

# Rectangle rouge pour Hero 2
surface.fill((255, 50, 50))
```

---

## 2. ATTAQUES MUSICALES (3 images) - PRIORITÉ HAUTE

- [ ] `sound_wave.png` - Projectile onde sonore (32×32px)
- [ ] `impact.png` - Effet collision (optionnel, 48×48px)
- [ ] `ultimate.png` - Attaque spéciale (64×64px, priorité basse)

**Placeholder** :
```python
# Cercle jaune pour projectile
pygame.draw.circle(surface, (255, 255, 0), center, 8)
```

---

## 3. ENNEMIS (4 images) - PRIORITÉ HAUTE

### Hater (ennemi faible)
- [ ] `hater_idle.png` - Pose normale (48×48px)
- [ ] `hater_hit.png` - Prend coup (optionnel)

### Rockstar Rival (ennemi moyen)
- [ ] `rockstar_idle.png` - Pose normale (64×64px)
- [ ] `rockstar_hit.png` - Prend coup (optionnel)

**Placeholder** :
```python
# Rectangle violet pour Hater
surface.fill((150, 50, 150))

# Rectangle orange pour Rockstar
surface.fill((255, 150, 50))
```

---

## 4. BOSS FINAL (4 images) - PRIORITÉ MOYENNE

- [ ] `boss_idle.png` - Pose normale (96×96px)
- [ ] `boss_attack.png` - Animation attaque
- [ ] `boss_projectile.png` - "Mots toxiques" (32×32px)
- [ ] `boss_shockwave.png` - Onde de choc sol (128×32px)

**Placeholder** :
```python
# Rectangle rouge foncé pour boss
surface.fill((180, 0, 0))
```

---

## 5. PLATEFORMES (3 images) - PRIORITÉ HAUTE

- [ ] `platform_crate.png` - Caisse (64×32px)
- [ ] `platform_amp.png` - Ampli (64×64px)
- [ ] `platform_case.png` - Flight case (96×48px)

**Placeholder** :
```python
# Rectangle marron
pygame.draw.rect(screen, (100, 70, 40), rect)
```

---

## 6. BACKGROUNDS (3 images) - PRIORITÉ MOYENNE

- [ ] `bg_backstage.png` - Coulisses niveau 1 (800×600px)
- [ ] `bg_stage.png` - Scène niveau 2 (800×600px)
- [ ] `bg_boss_arena.png` - Arène boss (800×600px)

**Placeholder** :
```python
# Dégradés de couleur
# Niveau 1 : gris foncé
screen.fill((40, 40, 50))

# Niveau 2 : bleu nuit
screen.fill((20, 30, 60))

# Boss : rouge sombre
screen.fill((60, 20, 20))
```

---

## 7. COLLECTIBLES (3 images) - PRIORITÉ BASSE

- [ ] `collectible_pick.png` - Médiator (24×24px)
- [ ] `collectible_note.png` - Note musique (24×24px)
- [ ] `collectible_amp.png` - Ampli bonus (32×32px)

**Placeholder** :
```python
# Petits cercles colorés
pygame.draw.circle(screen, (255, 215, 0), pos, 8)  # Or
```

---

## 8. UI / HUD (5 images) - PRIORITÉ HAUTE

### Système de vie
- [ ] `ui_heart_full.png` - Guitare pleine (32×32px)
- [ ] `ui_heart_empty.png` - Guitare vide (32×32px)

### Barre Guitar Hero
- [ ] `ui_rhythm_bar.png` - Fond barre (400×40px)
- [ ] `ui_rhythm_cursor.png` - Curseur métronome (16×40px)
- [ ] `ui_rhythm_zone.png` - Zone parfaite (80×40px, vert)

**Placeholder** :
```python
# Vie : rectangles rouges/gris
for i in range(player.hp):
    pygame.draw.rect(screen, (255, 0, 0), (10 + i*40, 10, 32, 32))

# Barre rythme : rectangles
pygame.draw.rect(screen, (50, 50, 50), (200, 20, 400, 30))  # Fond
pygame.draw.rect(screen, (0, 255, 0), (350, 20, 100, 30))   # Zone parfaite
pygame.draw.circle(screen, (255, 255, 0), (cursor_x, 35), 5) # Curseur
```

---

## 9. ÉCRANS (4 images) - PRIORITÉ BASSE

- [ ] `screen_menu.png` - Menu principal (800×600px)
- [ ] `screen_pause.png` - Menu pause (optionnel)
- [ ] `screen_gameover.png` - Game Over (800×600px)
- [ ] `screen_victory.png` - Victoire (800×600px)

**Placeholder** :
```python
# Texte simple avec fond
font_title = pygame.font.Font(None, 72)
text = font_title.render("ROCKSTAR BROS", True, (255, 255, 255))
screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//3))
```

---

## SONS (Non bloquants pour MVP)

### Musiques
- [ ] `music_menu.mp3`
- [ ] `music_level1.mp3`
- [ ] `music_level2.mp3`
- [ ] `music_boss.mp3`

### Effets sonores
- [ ] `sfx_jump.wav`
- [ ] `sfx_attack.wav`
- [ ] `sfx_hit.wav`
- [ ] `sfx_perfect_timing.wav`
- [ ] `sfx_collect.wav`
- [ ] `sfx_ui_click.wav`

### Rythme
- [ ] `sfx_metronome_tick.wav`

**Note** : Sons peuvent être ajoutés en fin de projet. Pas bloquants pour gameplay.

---

## Priorités de développement

### Phase 1 : MVP JOUABLE (Jour 1-2)
**Objectif** : Jeu fonctionnel avec placeholders

✅ Utiliser rectangles colorés pour TOUT
✅ Concentrer sur la mécanique (mouvement, saut, collision)
✅ 0 asset graphique requis

### Phase 2 : ASSETS CRITIQUES (Jour 3)
**Objectif** : Remplacer les éléments les plus visibles

Priorité :
1. Héros (idle + run) = 4 images
2. 1 ennemi (idle) = 1 image
3. Projectile = 1 image
4. Plateformes = 1 image
5. UI vie = 2 images
**Total : ~9 images** pour avoir un jeu présentable

### Phase 3 : POLISH (Jour 4)
**Objectif** : Ajouter backgrounds, boss, écrans

- 3 backgrounds
- Boss (2-3 images)
- Écrans menu/victory/gameover
**Total : +10 images**

### Phase 4 : FINITIONS (Jour 4 fin + 5)
**Objectif** : Sons, animations supplémentaires

- Sons critiques (jump, attack, hit)
- Musiques
- Animations attaque si temps

---

## Dimensions recommandées

| Type | Taille | Notes |
|------|--------|-------|
| Joueur | 64×64px | Carré, transparent |
| Ennemi faible | 48×48px | Plus petit que joueur |
| Ennemi fort | 64×64px | Même taille joueur |
| Boss | 96×96px | 1.5× taille joueur |
| Projectile | 32×32px | Petit, rapide |
| Plateforme | 64×32px | Rectangle horizontal |
| Background | 800×600px | Taille écran |
| UI vie | 32×32px | Icône HUD |
| UI barre | 400×40px | Barre horizontale |
| Collectible | 24×24px | Petit objet |

---

## Outils de création recommandés

### Pixel art (style rétro)
- **Piskel** (en ligne, gratuit) : https://www.piskelapp.com
- **Aseprite** (payant mais excellent)
- **LibreSprite** (fork gratuit Aseprite)

### Graphiques simples
- **Canva** (templates gratuits)
- **GIMP** (gratuit, complet)
- **Inkscape** (vectoriel gratuit)

### IA génération (si autorisé)
- **Bing Image Creator** (DALL-E gratuit)
- **Stable Diffusion** (local)
- Prompt exemple : "pixel art guitar hero character sprite sheet, 64x64, transparent background"

### Placeholder code
```python
# Fonction helper pour créer surfaces temporaires
def create_placeholder(width, height, color):
    surf = pygame.Surface((width, height))
    surf.fill(color)
    return surf

# Usage
player_img = create_placeholder(64, 64, (50, 150, 255))  # Bleu
enemy_img = create_placeholder(48, 48, (150, 50, 150))   # Violet
```

---

## Checklist avant rendu final

### Graphismes
- [ ] 2 héros distincts visuellement
- [ ] Au moins 2 types ennemis différenciables
- [ ] Boss visuellement impressionnant
- [ ] 3 backgrounds différents (1 par niveau)
- [ ] UI vie (cœurs/guitares) claire
- [ ] Barre Guitar Hero visible et compréhensible

### Sons (optionnel mais ++++)
- [ ] Musique de fond (au moins niveau + boss)
- [ ] Son saut
- [ ] Son attaque
- [ ] Son timing parfait (différent attaque normale)

### Animations minimum
- [ ] Joueur : idle ≠ run ≠ jump (3 états différents)
- [ ] Ennemis : au moins 2 frames (idle + hit)

---

## Notes finales

**Règle d'or** : Un jeu avec des rectangles colorés qui fonctionne bien > un jeu avec de beaux sprites qui bug.

**Timeline réaliste** :
- Jour 1-2 : 100% placeholders
- Jour 3 : 9 assets prioritaires
- Jour 4 : 15-20 assets total
- Jour 5 : Polish + sons

**Si manque de temps** :
Garder placeholders pour éléments secondaires (collectibles, effets, écrans). Focus sur joueur + ennemis + backgrounds.

---

**Ce fichier sera mis à jour au fur et à mesure. Cocher [x] les assets complétés.**