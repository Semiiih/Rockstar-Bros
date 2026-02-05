"""
Rockstar Bros - Classes Ennemis
Gere les ennemis (Hater, Rival) et le Boss avec animations
"""

import pygame
import random
from settings import (
    WHITE, RED, ORANGE, GRAY, GREEN, BLUE, PURPLE,
    GRAVITY, MAX_FALL_SPEED,
    HATER_SPEED, HATER_HEALTH, HATER_DAMAGE, HATER_WIDTH, HATER_HEIGHT,
    HATER_DETECTION_RANGE, HATER_SCORE,
    HATER_FLYING_SPEED, HATER_FLYING_HEALTH, HATER_FLYING_DAMAGE, HATER_FLYING_WIDTH, HATER_FLYING_HEIGHT,
    HATER_FLYING_DETECTION_RANGE, HATER_FLYING_SCORE, HATER_FLYING_HOVER_AMPLITUDE, HATER_FLYING_HOVER_SPEED,
    RIVAL_SPEED, RIVAL_HEALTH, RIVAL_DAMAGE, RIVAL_WIDTH, RIVAL_HEIGHT,
    RIVAL_DETECTION_RANGE, RIVAL_SCORE, RIVAL_SHOOT_COOLDOWN, RIVAL_PROJECTILE_SPEED, RIVAL_PROJECTILE_DAMAGE,
    BOSS_HEALTH, BOSS_DAMAGE, BOSS_WIDTH, BOSS_HEIGHT, BOSS_SPEED,
    BOSS_ATTACK_COOLDOWN, BOSS_SCORE,
    BOSS2_HEALTH, BOSS2_DAMAGE, BOSS2_WIDTH, BOSS2_HEIGHT, BOSS2_SPEED,
    BOSS2_ATTACK_COOLDOWN, BOSS2_SCORE,
    BOSS3_HEALTH, BOSS3_DAMAGE, BOSS3_WIDTH, BOSS3_HEIGHT, BOSS3_SPEED,
    BOSS3_ATTACK_COOLDOWN, BOSS3_SCORE,
    BOSS_PHASE_2_THRESHOLD, BOSS_PHASE_3_THRESHOLD,
    IMG_ENEMIES_DIR,
    # Hater images
    IMG_HATER_IDLE, IMG_HATER_RUN, IMG_HATER_RUN1, IMG_HATER_ATTACK, IMG_HATER_DEAD,
    # Hater Flying images
    IMG_HATER_FLYING_IDLE, IMG_HATER_FLYING_FLY1, IMG_HATER_FLYING_FLY2,
    IMG_HATER_FLYING_ATTACK, IMG_HATER_FLYING_HIT, IMG_HATER_FLYING_DEAD,
    # Rival images
    IMG_RIVAL_IDLE, IMG_RIVAL_RUN1, IMG_RIVAL_RUN2, IMG_RIVAL_ATTACK, IMG_RIVAL_ATTACK2, IMG_RIVAL_DEAD,
    # Boss images
    IMG_BOSS_IDLE, IMG_BOSS_RUN1, IMG_BOSS_RUN2, IMG_BOSS_JUMP, IMG_BOSS_ATTACK,
    IMG_BOSS2_IDLE, IMG_BOSS2_RUN1, IMG_BOSS2_RUN2, IMG_BOSS2_JUMP, IMG_BOSS2_ATTACK,
    IMG_BOSS3_IDLE, IMG_BOSS3_RUN1, IMG_BOSS3_RUN2, IMG_BOSS3_JUMP, IMG_BOSS3_ATTACK,
)
from entities.projectile import BossProjectile, RivalProjectile
import math


class Enemy(pygame.sprite.Sprite):
    """Classe de base pour les ennemis avec animations"""

    _image_cache = {}  # Cache classe: {enemy_type: {key: image}}

    def __init__(self, x, y, enemy_type="hater"):
        super().__init__()
        self.enemy_type = enemy_type

        # Config selon type
        if enemy_type == "hater":
            self.width = HATER_WIDTH
            self.height = HATER_HEIGHT
            self.speed = HATER_SPEED
            self.max_health = HATER_HEALTH
            self.damage = HATER_DAMAGE
            self.detection_range = HATER_DETECTION_RANGE
            self.score_value = HATER_SCORE
            self.color = RED
            self.can_fly = False
            self.can_shoot = False
        elif enemy_type == "hater_flying":
            self.width = HATER_FLYING_WIDTH
            self.height = HATER_FLYING_HEIGHT
            self.speed = HATER_FLYING_SPEED
            self.max_health = HATER_FLYING_HEALTH
            self.damage = HATER_FLYING_DAMAGE
            self.detection_range = HATER_FLYING_DETECTION_RANGE
            self.score_value = HATER_FLYING_SCORE
            self.color = PURPLE
            self.can_fly = True
            self.can_shoot = False
            # Attributs pour le vol
            self.hover_offset = 0
            self.hover_amplitude = HATER_FLYING_HOVER_AMPLITUDE
            self.hover_speed = HATER_FLYING_HOVER_SPEED
            self.base_y = y - 100  # Vole plus haut
        elif enemy_type == "rival" or enemy_type == "rival_shooter":
            self.width = RIVAL_WIDTH
            self.height = RIVAL_HEIGHT
            self.speed = RIVAL_SPEED
            self.max_health = RIVAL_HEALTH
            self.damage = RIVAL_DAMAGE
            self.score_value = RIVAL_SCORE
            self.color = ORANGE
            self.can_fly = False
            self.can_shoot = (enemy_type == "rival_shooter")
            # Attributs pour tirer
            if self.can_shoot:
                self.detection_range = 800  # Grande portée pour les tireurs (800px)
                self.shoot_cooldown = RIVAL_SHOOT_COOLDOWN
                self.shoot_timer = 1500  # Premier tir apres 1.5 seconde (laisse le temps au joueur)
                self.shoot_anim_timer = 0  # Timer pour l'animation de tir
            else:
                self.detection_range = RIVAL_DETECTION_RANGE
        else:
            # Fallback
            self.width = HATER_WIDTH
            self.height = HATER_HEIGHT
            self.speed = HATER_SPEED
            self.max_health = HATER_HEALTH
            self.damage = HATER_DAMAGE
            self.detection_range = HATER_DETECTION_RANGE
            self.score_value = HATER_SCORE
            self.color = RED
            self.can_fly = False
            self.can_shoot = False

        self.health = self.max_health

        # Charger toutes les images d'animation
        self.images = {}
        self._load_images()

        # Image par defaut
        self.image = self.images.get("idle") or self._get_placeholder((self.width, self.height), self.color)

        # Position initiale (pour les volants, spawner plus haut)
        if self.can_fly:
            self.rect = self.image.get_rect(center=(x, self.base_y))
        else:
            self.rect = self.image.get_rect(midbottom=(x, y))

        # Position float pour mouvement sub-pixel precis
        self.float_x = float(self.rect.x)

        # Comportement
        self.facing_right = False
        self.patrol_direction = -1
        self.patrol_distance = 100
        self.start_x = x
        self.hit_flash = 0

        # Animation
        self.state = "idle"  # idle, run, attack, dead
        self.anim_frame = 0
        self.anim_timer = 0
        self.is_dead = False
        self.death_timer = 0

        # Physique (pour tomber dans les trous)
        self.velocity_y = 0
        self.on_ground = False

    def _load_images(self):
        """Charge toutes les images d'animation de l'ennemi"""
        # Cle de cache unique pour ce type d'ennemi
        cache_key = self.enemy_type if self.enemy_type != "rival_shooter" else "rival_shooter"

        # Utiliser le cache si disponible
        if cache_key in Enemy._image_cache:
            self.images = dict(Enemy._image_cache[cache_key])
            return

        if self.enemy_type == "hater":
            img_files = {
                "idle": IMG_HATER_IDLE,
                "run1": IMG_HATER_RUN,
                "run2": IMG_HATER_RUN1,
                "attack": IMG_HATER_ATTACK,
                "dead": IMG_HATER_DEAD,
            }
        elif self.enemy_type == "hater_flying":
            img_files = {
                "idle": IMG_HATER_FLYING_IDLE,
                "run1": IMG_HATER_FLYING_FLY1,  # Animation de vol
                "run2": IMG_HATER_FLYING_FLY2,
                "attack": IMG_HATER_FLYING_ATTACK,
                "dead": IMG_HATER_FLYING_DEAD,
            }
        else:  # rival / rival_shooter
            img_files = {
                "idle": IMG_RIVAL_IDLE,
                "run1": IMG_RIVAL_RUN1,
                "run2": IMG_RIVAL_RUN2,
                "attack": IMG_RIVAL_ATTACK2 if self.can_shoot else IMG_RIVAL_ATTACK,
                "dead": IMG_RIVAL_DEAD,
            }

        for key, filename in img_files.items():
            try:
                path = IMG_ENEMIES_DIR / filename
                img = pygame.image.load(str(path)).convert_alpha()
                # Pour l'attaque et dead, garder les proportions
                if key in ("attack", "dead"):
                    original_width, original_height = img.get_size()
                    ratio = self.height / original_height
                    new_width = int(original_width * ratio)
                    img = pygame.transform.scale(img, (new_width, self.height))
                else:
                    img = pygame.transform.scale(img, (self.width, self.height))
                self.images[key] = img
            except Exception:
                self.images[key] = None

        # Mettre en cache
        Enemy._image_cache[cache_key] = dict(self.images)

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        return surf

    def _get_current_image(self):
        """Retourne l'image correspondant a l'etat actuel"""
        if self.is_dead:
            img = self.images.get("dead")
        elif self.can_shoot and hasattr(self, 'shoot_anim_timer') and self.shoot_anim_timer > 0:
            # Animation de tir pour les rivals tireurs
            img = self.images.get("attack")
        elif self.state == "attack" and not self.can_shoot:
            # Attaque au corps à corps seulement pour les non-tireurs
            img = self.images.get("attack")
        elif self.state == "run":
            frame_key = "run1" if self.anim_frame == 0 else "run2"
            img = self.images.get(frame_key)
        else:
            img = self.images.get("idle")

        if img is None:
            img = self._get_placeholder((self.width, self.height), self.color)

        return img

    def update(self, dt, player_rect, platforms=None, other_enemies=None, projectile_group=None):
        """Met a jour l'ennemi"""
        dt_ms = dt * 1000

        # Si mort, juste faire l'animation de mort
        if self.is_dead:
            self.death_timer += dt_ms
            if self.death_timer >= 2000:  # Disparait apres 2 secondes
                self.kill()
            # Mettre a jour l'image pour afficher l'image dead
            # Les ennemis volants tombent quand ils meurent
            if self.can_fly and platforms:
                self.velocity_y += GRAVITY * 0.5  # Tombent moins vite
                self.rect.y += self.velocity_y
            self.image = self._get_current_image()
            return

        # Flash de degats
        if self.hit_flash > 0:
            self.hit_flash -= dt_ms

        # Gestion du tir pour les rivals tireurs
        if self.can_shoot and projectile_group is not None:
            # Decrémenter le timer d'animation de tir
            if self.shoot_anim_timer > 0:
                self.shoot_anim_timer -= dt_ms

            self.shoot_timer -= dt_ms
            if self.shoot_timer <= 0:
                # Tirer vers le joueur si dans la range
                dist_to_player = abs(self.rect.centerx - player_rect.centerx)
                if dist_to_player < self.detection_range:
                    # Creer un projectile
                    proj = RivalProjectile(
                        self.rect.centerx,
                        self.rect.centery,
                        player_rect.centerx,
                        player_rect.centery
                    )
                    projectile_group.add(proj)
                    # Activer l'animation de tir
                    self.shoot_anim_timer = 400  # Animation pendant 400ms
                    self.state = "attack"
                # Reset le timer meme si hors portee pour eviter accumulation negative
                self.shoot_timer = self.shoot_cooldown

        # Physique differente pour les volants
        if self.can_fly:
            # Pas de gravite, mouvement de hovering
            self.hover_offset += dt * self.hover_speed
            hover_y = math.sin(self.hover_offset) * self.hover_amplitude
            target_y = self.base_y + hover_y
            self.rect.centery = int(target_y)
            self.on_ground = True  # Toujours "au sol" pour le comportement
        else:
            # Appliquer la gravite seulement en l'air (evite oscillation on_ground)
            if not self.on_ground:
                self.velocity_y += GRAVITY
                if self.velocity_y > MAX_FALL_SPEED:
                    self.velocity_y = MAX_FALL_SPEED

            # Mouvement vertical pixel par pixel pour collision precise
            self.on_ground = False
            if platforms:
                dy = self.velocity_y
                if dy != 0:
                    sign = 1 if dy > 0 else -1
                    remaining = abs(dy)

                    while remaining > 0:
                        step = min(1, remaining)
                        self.rect.y += sign * step
                        remaining -= step

                        # Collision avec le sol uniquement
                        for platform in platforms:
                            if platform.is_ground and self.rect.colliderect(platform.rect):
                                if sign > 0:  # Tombe
                                    self.rect.bottom = platform.rect.top
                                    self.velocity_y = 0
                                    self.on_ground = True
                                break
                        if self.on_ground:
                            break
                else:
                    # velocity_y == 0 : verifier si toujours au sol
                    self.rect.y += 1
                    for platform in platforms:
                        if platform.is_ground and self.rect.colliderect(platform.rect):
                            self.rect.bottom = platform.rect.top
                            self.on_ground = True
                            break
                    if not self.on_ground:
                        self.rect.y -= 1

        # Verifier si un autre ennemi est trop proche (pour eviter l'oscillation)
        blocked_left = False
        blocked_right = False
        if other_enemies:
            for other in other_enemies:
                if other is self or other.is_dead:
                    continue
                # Distance entre les deux ennemis
                dist = abs(self.rect.centerx - other.rect.centerx)
                min_dist = (self.rect.width + other.rect.width) // 2 + 15
                if dist < min_dist:
                    # Bloquer le mouvement vers l'autre ennemi
                    if other.rect.centerx < self.rect.centerx:
                        blocked_left = True
                    else:
                        blocked_right = True

        # Determiner l'etat
        old_state = self.state
        is_moving = False

        # Mouvement horizontal seulement si au sol
        if self.on_ground:
            dist_to_player_x = abs(self.rect.centerx - player_rect.centerx)

            # Les rivals tireurs (rival_shooter) restent IMMOBILES et tirent
            if self.can_shoot:
                # Ne bouge JAMAIS, regarde juste le joueur
                self.facing_right = player_rect.centerx > self.rect.centerx
                # L'état est géré par le tir (shoot_anim_timer)
                if self.shoot_anim_timer <= 0:
                    self.state = "idle"
            else:
                # Tous les autres ennemis (hater, hater_flying, rival) BOUGENT et FRAPPENT
                if dist_to_player_x < self.detection_range:
                    # Zone morte: si le joueur est trop proche, ne pas bouger
                    # Hysteresis: doit s'eloigner a 50px pour reprendre la poursuite
                    chase_threshold = 50 if self.state == "idle" or self.state == "attack" else 30
                    if dist_to_player_x > chase_threshold:
                        # Poursuit le joueur (sauf si bloque par un autre ennemi)
                        if player_rect.centerx < self.rect.centerx:
                            if not blocked_left:
                                self.float_x -= self.speed
                                is_moving = True
                            self.facing_right = False
                        else:
                            if not blocked_right:
                                self.float_x += self.speed
                                is_moving = True
                            self.facing_right = True
                        if is_moving:
                            self.state = "run"
                    else:
                        # Trop proche horizontalement, s'arreter et regarder le joueur
                        self.facing_right = player_rect.centerx > self.rect.centerx
                        self.state = "idle"

                    # Attaque au corps a corps si tres proche
                    if dist_to_player_x < 80:
                        self.state = "attack"
                else:
                    # Patrouille (sauf si bloque)
                    move_dir = self.speed * self.patrol_direction
                    can_move = (move_dir < 0 and not blocked_left) or (move_dir > 0 and not blocked_right)
                    if can_move:
                        self.float_x += move_dir
                        is_moving = True
                    if abs(self.rect.x - self.start_x) > self.patrol_distance:
                        self.patrol_direction *= -1
                        self.facing_right = self.patrol_direction > 0
                    if is_moving:
                        self.state = "run"
                    else:
                        self.state = "idle"
        else:
            self.state = "idle"

        # Synchroniser float_x -> rect.x
        self.rect.x = round(self.float_x)

        # Animation de course
        if self.state == "run":
            self.anim_timer += dt_ms
            if self.anim_timer >= 200:  # Change frame toutes les 200ms
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 2

        # Mise a jour de l'image
        self.image = self._get_current_image()

    def take_damage(self, amount):
        """L'ennemi prend des degats"""
        self.health -= amount
        self.hit_flash = 100

        if self.health <= 0:
            self.is_dead = True
            self.state = "dead"
            return True
        return False

    def draw(self, screen, camera_x):
        """Dessine l'ennemi avec effets"""
        img = self.image
        # L'image de base regarde a droite, donc flip si regarde a gauche
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        draw_rect = self.rect.move(-camera_x, 0)

        # Effet de transparence si mort (commence a disparaitre apres 1.5s)
        if self.is_dead:
            if self.death_timer > 1500:
                alpha = max(0, 255 - int((self.death_timer - 1500) / 500 * 255))
                img = img.copy()
                img.set_alpha(alpha)

        screen.blit(img, draw_rect)

        # Effet d'impact rouge quand touche (pas si mort)
        if self.hit_flash > 0 and not self.is_dead:
            # Cercle d'impact rouge qui s'agrandit et disparait
            flash_progress = 1.0 - (self.hit_flash / 100)  # 0 -> 1
            impact_radius = int(15 + flash_progress * 25)
            impact_alpha = int(200 * (1 - flash_progress))

            impact_surf = pygame.Surface((impact_radius * 2, impact_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(impact_surf, (255, 50, 50, impact_alpha),
                             (impact_radius, impact_radius), impact_radius)
            # Cercle interieur plus clair
            inner_radius = int(impact_radius * 0.6)
            pygame.draw.circle(impact_surf, (255, 150, 100, impact_alpha // 2),
                             (impact_radius, impact_radius), inner_radius)

            impact_pos = (draw_rect.centerx - impact_radius, draw_rect.centery - impact_radius)
            screen.blit(impact_surf, impact_pos)


class Boss(pygame.sprite.Sprite):
    """Boss - Support 3 types de boss avec stats et images differentes"""

    def __init__(self, x, y, boss_type="boss"):
        super().__init__()

        self.boss_type = boss_type

        # Config selon le type de boss
        if boss_type == "boss2":
            self.width = BOSS2_WIDTH
            self.height = BOSS2_HEIGHT
            self.max_health = BOSS2_HEALTH
            self.damage = BOSS2_DAMAGE
            self.speed = BOSS2_SPEED
            self.attack_cooldown = BOSS2_ATTACK_COOLDOWN
            self.score_value = BOSS2_SCORE
            self.color = (150, 0, 150)  # Violet pour boss 2
        elif boss_type == "boss3":
            self.width = BOSS3_WIDTH
            self.height = BOSS3_HEIGHT
            self.max_health = BOSS3_HEALTH
            self.damage = BOSS3_DAMAGE
            self.speed = BOSS3_SPEED
            self.attack_cooldown = BOSS3_ATTACK_COOLDOWN
            self.score_value = BOSS3_SCORE
            self.color = (255, 50, 0)  # Rouge flamboyant pour boss 3
        else:  # boss / boss1
            self.width = BOSS_WIDTH
            self.height = BOSS_HEIGHT
            self.max_health = BOSS_HEALTH
            self.damage = BOSS_DAMAGE
            self.speed = BOSS_SPEED
            self.attack_cooldown = BOSS_ATTACK_COOLDOWN
            self.score_value = BOSS_SCORE
            self.color = (200, 0, 100)  # Rouge-violet pour boss 1

        # Charger toutes les images
        self.images = {}
        self._load_images()

        self.image = self.images.get("idle") or self._get_placeholder((self.width, self.height), self.color)
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.health = self.max_health

        # Comportement
        self.phase = 1
        self.facing_right = False
        self.attack_timer = self.attack_cooldown
        self.current_attack = None
        self.hit_flash = 0

        # Animation
        self.state = "idle"  # idle, run, attack, jump
        self.anim_frame = 0
        self.anim_timer = 0
        self.attack_anim_timer = 0

        # Position float pour mouvement sub-pixel precis
        self.float_x = float(self.rect.x)

        # Mouvement
        self.move_timer = 0
        self.move_direction = -1
        self.is_moving = False

        # Flag pour declencher le son de tir
        self.just_attacked = False

    def _load_images(self):
        """Charge toutes les images d'animation du boss"""
        # Selection des images selon le type de boss
        if self.boss_type == "boss2":
            img_files = {
                "idle": IMG_BOSS2_IDLE,
                "run1": IMG_BOSS2_RUN1,
                "run2": IMG_BOSS2_RUN2,
                "jump": IMG_BOSS2_JUMP,
                "attack": IMG_BOSS2_ATTACK,
            }
        elif self.boss_type == "boss3":
            img_files = {
                "idle": IMG_BOSS3_IDLE,
                "run1": IMG_BOSS3_RUN1,
                "run2": IMG_BOSS3_RUN2,
                "jump": IMG_BOSS3_JUMP,
                "attack": IMG_BOSS3_ATTACK,
            }
        else:  # boss1
            img_files = {
                "idle": IMG_BOSS_IDLE,
                "run1": IMG_BOSS_RUN1,
                "run2": IMG_BOSS_RUN2,
                "jump": IMG_BOSS_JUMP,
                "attack": IMG_BOSS_ATTACK,
            }

        for key, filename in img_files.items():
            try:
                path = IMG_ENEMIES_DIR / filename
                img = pygame.image.load(str(path)).convert_alpha()
                # Pour l'attaque, garder les proportions (hauteur fixe, largeur proportionnelle)
                if key == "attack":
                    original_width, original_height = img.get_size()
                    ratio = self.height / original_height
                    new_width = int(original_width * ratio)
                    img = pygame.transform.scale(img, (new_width, self.height))
                else:
                    img = pygame.transform.scale(img, (self.width, self.height))
                self.images[key] = img
            except (pygame.error, FileNotFoundError):
                self.images[key] = None

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        pygame.draw.rect(surf, (255, 255, 255), (20, 30, 30, 20))
        pygame.draw.rect(surf, (255, 255, 255), (size[0] - 50, 30, 30, 20))
        return surf

    def _get_current_image(self):
        """Retourne l'image correspondant a l'etat actuel"""
        if self.attack_anim_timer > 0:
            img = self.images.get("attack")
        elif self.state == "run":
            frame_key = "run1" if self.anim_frame == 0 else "run2"
            img = self.images.get(frame_key)
        elif self.state == "jump":
            img = self.images.get("jump")
        else:
            img = self.images.get("idle")

        if img is None:
            img = self._get_placeholder((self.width, self.height), self.color)

        return img

    def update(self, dt, player_rect, projectiles_group):
        """Met a jour le boss"""
        dt_ms = dt * 1000

        # Flash de degats
        if self.hit_flash > 0:
            self.hit_flash -= dt_ms

        # Timer d'animation d'attaque
        if self.attack_anim_timer > 0:
            self.attack_anim_timer -= dt_ms

        # Determiner la phase selon les PV
        health_ratio = self.health / self.max_health
        if health_ratio <= BOSS_PHASE_3_THRESHOLD:
            self.phase = 3
        elif health_ratio <= BOSS_PHASE_2_THRESHOLD:
            self.phase = 2

        # Regarder vers le joueur
        self.facing_right = player_rect.centerx > self.rect.centerx

        # Mouvement
        self.move_timer += dt_ms
        if self.move_timer > 2000:
            self.move_timer = 0
            self.move_direction *= -1

        # Deplacement vers le joueur (lent)
        self.is_moving = False
        if abs(self.rect.centerx - player_rect.centerx) > 150:
            if player_rect.centerx < self.rect.centerx:
                self.float_x -= self.speed
            else:
                self.float_x += self.speed
            self.is_moving = True

        # Synchroniser float_x -> rect.x
        self.rect.x = round(self.float_x)

        # Determiner l'etat d'animation
        if self.is_moving:
            self.state = "run"
        else:
            self.state = "idle"

        # Animation de course
        if self.state == "run":
            self.anim_timer += dt_ms
            if self.anim_timer >= 250:  # Change frame toutes les 250ms
                self.anim_timer = 0
                self.anim_frame = (self.anim_frame + 1) % 2

        # Attaques
        self.attack_timer -= dt_ms
        if self.attack_timer <= 0:
            self._perform_attack(player_rect, projectiles_group)
            cooldown_modifier = 1.0 - (self.phase - 1) * 0.2
            self.attack_timer = self.attack_cooldown * cooldown_modifier

        # Mise a jour de l'image
        self.image = self._get_current_image()

    def _perform_attack(self, player_rect, projectiles_group):
        """Execute une attaque selon le type de boss"""
        self.attack_anim_timer = 400  # Animation d'attaque pendant 400ms
        self.just_attacked = True  # Declenche le son de tir

        if self.boss_type == "boss3":
            # Boss 3: Attaques en rafale et en eventail
            self._attack_boss3(player_rect, projectiles_group)
        elif self.boss_type == "boss2":
            # Boss 2: Attaques en cercle et vagues
            self._attack_boss2(player_rect, projectiles_group)
        else:
            # Boss 1: Attaques simples directes
            self._attack_boss1(player_rect, projectiles_group)

    def _attack_boss1(self, player_rect, projectiles_group):
        """Attaques du Boss 1 - Simples et directes"""
        attack_type = random.choice(["single", "double", "triple"])

        if attack_type == "single":
            # Tir simple vers le joueur
            proj = BossProjectile(
                self.rect.centerx,
                self.rect.centery,
                player_rect.centerx,
                player_rect.centery,
                self.boss_type
            )
            projectiles_group.add(proj)
        elif attack_type == "double":
            # Deux tirs paralleles
            for offset_y in [-30, 30]:
                proj = BossProjectile(
                    self.rect.centerx,
                    self.rect.centery + offset_y,
                    player_rect.centerx,
                    player_rect.centery + offset_y,
                    self.boss_type
                )
                projectiles_group.add(proj)
        else:  # triple
            # Trois tirs en ligne
            for offset_y in [-40, 0, 40]:
                proj = BossProjectile(
                    self.rect.centerx,
                    self.rect.centery + offset_y,
                    player_rect.centerx,
                    player_rect.centery,
                    self.boss_type
                )
                projectiles_group.add(proj)

    def _attack_boss2(self, player_rect, projectiles_group):
        """Attaques du Boss 2 - En cercle et vagues"""
        attack_type = random.choice(["spread", "circle", "wave"])

        if attack_type == "spread":
            # Tir en eventail (3 directions)
            angles = [-30, 0, 30]
            for angle in angles:
                rad = math.radians(angle)
                dx = player_rect.centerx - self.rect.centerx
                dy = player_rect.centery - self.rect.centery
                # Rotation du vecteur
                new_dx = dx * math.cos(rad) - dy * math.sin(rad)
                new_dy = dx * math.sin(rad) + dy * math.cos(rad)
                target_x = self.rect.centerx + new_dx
                target_y = self.rect.centery + new_dy
                proj = BossProjectile(
                    self.rect.centerx,
                    self.rect.centery,
                    target_x,
                    target_y,
                    self.boss_type
                )
                projectiles_group.add(proj)
        elif attack_type == "circle":
            # Tir en cercle
            num_projectiles = 6 + self.phase * 2
            for i in range(num_projectiles):
                angle = (360 / num_projectiles) * i
                rad = math.radians(angle)
                target_x = self.rect.centerx + math.cos(rad) * 100
                target_y = self.rect.centery + math.sin(rad) * 100
                proj = BossProjectile(
                    self.rect.centerx,
                    self.rect.centery,
                    target_x,
                    target_y,
                    self.boss_type
                )
                projectiles_group.add(proj)
        else:  # wave
            # Vague de tirs horizontaux
            num = 3 + self.phase
            for i in range(num):
                offset_y = (i - num // 2) * 40
                proj = BossProjectile(
                    self.rect.centerx,
                    self.rect.centery + offset_y,
                    self.rect.centerx - 500,
                    self.rect.centery + offset_y,
                    self.boss_type
                )
                projectiles_group.add(proj)

    def _attack_boss3(self, player_rect, projectiles_group):
        """Attaques du Boss 3 - Rafales et patterns complexes"""
        attack_type = random.choice(["burst", "spiral", "rain", "cross"])

        if attack_type == "burst":
            # Rafale rapide vers le joueur
            num = 4 + self.phase
            for i in range(num):
                offset_x = random.randint(-20, 20)
                offset_y = random.randint(-30, 30)
                proj = BossProjectile(
                    self.rect.centerx + offset_x,
                    self.rect.centery + offset_y,
                    player_rect.centerx + random.randint(-50, 50),
                    player_rect.centery + random.randint(-30, 30),
                    self.boss_type
                )
                projectiles_group.add(proj)
        elif attack_type == "spiral":
            # Spirale de projectiles
            num = 8 + self.phase * 2
            for i in range(num):
                angle = (360 / num) * i + random.randint(-10, 10)
                rad = math.radians(angle)
                target_x = self.rect.centerx + math.cos(rad) * 150
                target_y = self.rect.centery + math.sin(rad) * 150
                proj = BossProjectile(
                    self.rect.centerx,
                    self.rect.centery,
                    target_x,
                    target_y,
                    self.boss_type
                )
                projectiles_group.add(proj)
        elif attack_type == "rain":
            # Pluie de projectiles d'en haut
            num = 5 + self.phase
            for i in range(num):
                start_x = self.rect.centerx - 200 + i * 80
                proj = BossProjectile(
                    start_x,
                    self.rect.top - 50,
                    start_x + random.randint(-30, 30),
                    self.rect.centery + 300,
                    self.boss_type
                )
                projectiles_group.add(proj)
        else:  # cross
            # Pattern en croix
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for dx, dy in directions:
                proj = BossProjectile(
                    self.rect.centerx,
                    self.rect.centery,
                    self.rect.centerx + dx * 200,
                    self.rect.centery + dy * 200,
                    self.boss_type
                )
                projectiles_group.add(proj)

    def take_damage(self, amount):
        """Le boss prend des degats"""
        self.health -= amount
        self.hit_flash = 100
        return self.health <= 0

    def draw(self, screen, camera_x):
        """Dessine le boss avec effets"""
        img = self.image
        # L'image de base regarde a droite, donc flip si le boss regarde a gauche
        if not self.facing_right:
            img = pygame.transform.flip(img, True, False)

        draw_rect = self.rect.move(-camera_x, 0)
        screen.blit(img, draw_rect)

        # Effet d'impact rouge quand touche
        if self.hit_flash > 0:
            flash_progress = 1.0 - (self.hit_flash / 100)
            impact_radius = int(25 + flash_progress * 40)  # Plus grand pour le boss
            impact_alpha = int(200 * (1 - flash_progress))

            impact_surf = pygame.Surface((impact_radius * 2, impact_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(impact_surf, (255, 50, 50, impact_alpha),
                             (impact_radius, impact_radius), impact_radius)
            inner_radius = int(impact_radius * 0.6)
            pygame.draw.circle(impact_surf, (255, 150, 100, impact_alpha // 2),
                             (impact_radius, impact_radius), inner_radius)

            impact_pos = (draw_rect.centerx - impact_radius, draw_rect.centery - impact_radius)
            screen.blit(impact_surf, impact_pos)

        # Barre de vie du boss
        bar_width = BOSS_WIDTH
        bar_height = 10
        bar_x = draw_rect.centerx - bar_width // 2
        bar_y = draw_rect.top - 20

        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
        health_width = int((self.health / self.max_health) * bar_width)
        health_color = RED if self.phase == 3 else ORANGE if self.phase == 2 else GREEN
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
