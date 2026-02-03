"""
Rockstar Bros - Classes Ennemis
Gere les ennemis (Hater, Rival) et le Boss avec animations
"""

import pygame
import random
from settings import (
    WHITE, RED, ORANGE, GRAY, GREEN,
    GRAVITY, MAX_FALL_SPEED,
    HATER_SPEED, HATER_HEALTH, HATER_DAMAGE, HATER_WIDTH, HATER_HEIGHT,
    HATER_DETECTION_RANGE, HATER_SCORE,
    RIVAL_SPEED, RIVAL_HEALTH, RIVAL_DAMAGE, RIVAL_WIDTH, RIVAL_HEIGHT,
    RIVAL_DETECTION_RANGE, RIVAL_SCORE,
    BOSS_HEALTH, BOSS_DAMAGE, BOSS_WIDTH, BOSS_HEIGHT, BOSS_SPEED,
    BOSS_ATTACK_COOLDOWN, BOSS_SCORE,
    BOSS_PHASE_2_THRESHOLD, BOSS_PHASE_3_THRESHOLD,
    IMG_ENEMIES_DIR,
    # Hater images
    IMG_HATER_IDLE, IMG_HATER_RUN, IMG_HATER_RUN1, IMG_HATER_ATTACK, IMG_HATER_DEAD,
    # Rival images
    IMG_RIVAL_IDLE, IMG_RIVAL_RUN1, IMG_RIVAL_RUN2, IMG_RIVAL_ATTACK, IMG_RIVAL_DEAD,
    # Boss images
    IMG_BOSS_IDLE, IMG_BOSS_RUN1, IMG_BOSS_RUN2, IMG_BOSS_JUMP, IMG_BOSS_ATTACK,
)
from entities.projectile import BossProjectile


class Enemy(pygame.sprite.Sprite):
    """Classe de base pour les ennemis avec animations"""

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
        else:  # rival
            self.width = RIVAL_WIDTH
            self.height = RIVAL_HEIGHT
            self.speed = RIVAL_SPEED
            self.max_health = RIVAL_HEALTH
            self.damage = RIVAL_DAMAGE
            self.detection_range = RIVAL_DETECTION_RANGE
            self.score_value = RIVAL_SCORE
            self.color = ORANGE

        self.health = self.max_health

        # Charger toutes les images d'animation
        self.images = {}
        self._load_images()

        # Image par defaut
        self.image = self.images.get("idle", self._get_placeholder((self.width, self.height), self.color))
        self.rect = self.image.get_rect(midbottom=(x, y))

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
        if self.enemy_type == "hater":
            img_files = {
                "idle": IMG_HATER_IDLE,
                "run1": IMG_HATER_RUN,
                "run2": IMG_HATER_RUN1,
                "attack": IMG_HATER_ATTACK,
                "dead": IMG_HATER_DEAD,
            }
        else:  # rival
            img_files = {
                "idle": IMG_RIVAL_IDLE,
                "run1": IMG_RIVAL_RUN1,
                "run2": IMG_RIVAL_RUN2,
                "attack": IMG_RIVAL_ATTACK,
                "dead": IMG_RIVAL_DEAD,
            }

        for key, filename in img_files.items():
            try:
                path = IMG_ENEMIES_DIR / filename
                img = pygame.image.load(str(path)).convert_alpha()
                self.images[key] = pygame.transform.scale(img, (self.width, self.height))
            except (pygame.error, FileNotFoundError):
                self.images[key] = None

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        return surf

    def _get_current_image(self):
        """Retourne l'image correspondant a l'etat actuel"""
        if self.is_dead:
            img = self.images.get("dead")
        elif self.state == "attack":
            img = self.images.get("attack")
        elif self.state == "run":
            frame_key = "run1" if self.anim_frame == 0 else "run2"
            img = self.images.get(frame_key)
        else:
            img = self.images.get("idle")

        if img is None:
            img = self._get_placeholder((self.width, self.height), self.color)

        return img

    def update(self, dt, player_rect, platforms=None):
        """Met a jour l'ennemi"""
        dt_ms = dt * 1000

        # Si mort, juste faire l'animation de mort
        if self.is_dead:
            self.death_timer += dt_ms
            if self.death_timer >= 2000:  # Disparait apres 2 secondes
                self.kill()
            # Mettre a jour l'image pour afficher l'image dead
            self.image = self._get_current_image()
            return

        # Flash de degats
        if self.hit_flash > 0:
            self.hit_flash -= dt_ms

        # Appliquer la gravite
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

        # Determiner l'etat
        old_state = self.state
        is_moving = False

        # Mouvement horizontal seulement si au sol
        if self.on_ground:
            dist_to_player_x = abs(self.rect.centerx - player_rect.centerx)

            if dist_to_player_x < self.detection_range:
                # Zone morte: si le joueur est trop proche horizontalement, ne pas bouger
                # Evite l'effet "toupie" quand le joueur est au-dessus
                if dist_to_player_x > 25:
                    # Poursuit le joueur
                    if player_rect.centerx < self.rect.centerx:
                        self.rect.x -= self.speed
                        self.facing_right = False
                    else:
                        self.rect.x += self.speed
                        self.facing_right = True
                    is_moving = True
                    self.state = "run"
                else:
                    # Trop proche horizontalement, s'arreter et regarder le joueur
                    self.facing_right = player_rect.centerx > self.rect.centerx
                    self.state = "idle"

                # Attaque si tres proche
                if dist_to_player_x < 80:
                    self.state = "attack"
            else:
                # Patrouille
                self.rect.x += self.speed * self.patrol_direction
                if abs(self.rect.x - self.start_x) > self.patrol_distance:
                    self.patrol_direction *= -1
                    self.facing_right = self.patrol_direction > 0
                is_moving = True
                self.state = "run"
        else:
            self.state = "idle"

        if not is_moving:
            self.state = "idle"

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

        # Effet d'impact rouge quand touche
        if self.hit_flash > 0:
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
    """Boss final - Rockstar concurrente avec animations"""

    def __init__(self, x, y):
        super().__init__()

        # Charger toutes les images
        self.images = {}
        self._load_images()

        self.image = self.images.get("idle", self._get_placeholder((BOSS_WIDTH, BOSS_HEIGHT), (200, 0, 100)))
        self.rect = self.image.get_rect(midbottom=(x, y))

        self.max_health = BOSS_HEALTH
        self.health = self.max_health
        self.damage = BOSS_DAMAGE
        self.speed = BOSS_SPEED
        self.score_value = BOSS_SCORE

        # Comportement
        self.phase = 1
        self.facing_right = False
        self.attack_cooldown = BOSS_ATTACK_COOLDOWN
        self.attack_timer = self.attack_cooldown
        self.current_attack = None
        self.hit_flash = 0

        # Animation
        self.state = "idle"  # idle, run, attack, jump
        self.anim_frame = 0
        self.anim_timer = 0
        self.attack_anim_timer = 0

        # Mouvement
        self.move_timer = 0
        self.move_direction = -1
        self.is_moving = False

    def _load_images(self):
        """Charge toutes les images d'animation du boss"""
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
                self.images[key] = pygame.transform.scale(img, (BOSS_WIDTH, BOSS_HEIGHT))
            except (pygame.error, FileNotFoundError):
                self.images[key] = None

    def _get_placeholder(self, size, color):
        """Cree une image placeholder"""
        surf = pygame.Surface(size, pygame.SRCALPHA)
        surf.fill(color)
        pygame.draw.rect(surf, (255, 255, 255), (20, 30, 30, 20))
        pygame.draw.rect(surf, (255, 255, 255), (BOSS_WIDTH - 50, 30, 30, 20))
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
            img = self._get_placeholder((BOSS_WIDTH, BOSS_HEIGHT), (200, 0, 100))

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
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
            self.is_moving = True

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
        """Execute une attaque"""
        self.attack_anim_timer = 400  # Animation d'attaque pendant 400ms

        attack_type = random.choice(["projectile", "projectile", "shockwave"])

        if attack_type == "projectile":
            num_projectiles = self.phase
            for i in range(num_projectiles):
                offset_y = (i - num_projectiles // 2) * 30
                proj = BossProjectile(
                    self.rect.centerx,
                    self.rect.centery + offset_y,
                    player_rect.centerx,
                    player_rect.centery
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
        if self.facing_right:
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
