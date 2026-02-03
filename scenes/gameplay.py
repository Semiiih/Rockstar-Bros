"""
Rockstar Bros - Scene de gameplay
Coeur du jeu: gestion du niveau, collisions, systeme rythme
"""

import pygame
import random
import math
from scenes.base import Scene
from entities import Player, Projectile, Enemy, Boss, Platform, Pickup
from settings import (
    WIDTH, HEIGHT, WHITE, YELLOW, RED, GREEN, BLUE, PURPLE, ORANGE, GRAY, DARK_GRAY,
    STATE_PAUSE, STATE_GAME_OVER, STATE_VICTORY, CONTROLS,
    GROUND_Y,
    PLAYER_MAX_HEALTH, PLAYER_WIDTH, PLAYER_HEIGHT,
    PROJECTILE_SPEED,
    ULTIMATE_CHARGE_MAX, ULTIMATE_CHARGE_PER_HIT,
    ULTIMATE_BASE_DAMAGE, ULTIMATE_DAMAGE_PER_PERFECT, ULTIMATE_DAMAGE_PER_GOOD,
    ULTIMATE_DAMAGE_PER_OK, ULTIMATE_CHARGE_PER_PICKUP, ULTIMATE_NOTE_COUNT,
    NOTE_FALL_SPEED, NOTE_SPAWN_INTERVAL,
    HIT_ZONE_PERFECT, HIT_ZONE_GOOD, HIT_ZONE_OK,
    NOTE_SIZE, LANE_WIDTH, LANE_COUNT, TRACK_HEIGHT, TRACK_WIDTH,
    TRACK_X, TRACK_Y, HIT_LINE_Y, LANE_COLORS, LANE_KEYS,
    PICKUP_NOTE_SCORE, PICKUP_MEDIATOR_ULTIMATE,
    LEVEL_NAMES, LEVEL_LENGTHS,
    IMG_BG_DIR, IMG_BG_LEVEL1, IMG_BG_LEVEL2, IMG_BG_BOSS,
    FONT_METAL_MANIA, FONT_ROAD_RAGE,
    HUD_MARGIN, HUD_HEALTH_SIZE,
    SND_DIR, SND_MUSIC_LEVEL1, SND_MUSIC_LEVEL2, SND_MUSIC_BOSS, SND_VICTORY,
)


class GameplayScene(Scene):
    """Scene principale du jeu"""

    def __init__(self, game):
        super().__init__(game)

        # Groupes de sprites
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player_projectiles = pygame.sprite.Group()
        self.boss_projectiles = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()

        # Entites principales
        self.player = None
        self.boss = None

        # Camera
        self.camera_x = 0

        # Niveau
        self.current_level = 1
        self.level_width = LEVEL_LENGTHS[1]

        # Systeme ULTIME (Guitar Hero - notes qui tombent)
        self.ultimate_active = False
        self.ultimate_notes = []  # Liste des notes actives: {"lane": 0-2, "y": position}
        self.ultimate_notes_spawned = 0
        self.ultimate_spawn_timer = 0
        self.ultimate_results = []  # Liste des resultats ("PERFECT", "GOOD", "OK", "MISS")
        self.ultimate_total_damage = 0
        self.ultimate_lane_pressed = [False, False, False]  # Etat des touches F, G, H

        # Feedback timing
        self.timing_feedback = ""
        self.timing_feedback_timer = 0

        # UI
        self.font = None
        self.font_big = None

        # Background
        self.background = None

        # Debug
        self.debug_hitboxes = False

        # Celebration (apres avoir battu le boss)
        self.celebration_active = False
        self.celebration_timer = 0
        self.celebration_particles = []

        # Affichage des degats
        self.damage_numbers = []  # Liste: {"x", "y", "damage", "timer", "color"}

        # Animation timer pour effets visuels
        self.animation_time = 0

    def enter(self, **kwargs):
        """Initialisation a l'entree dans le niveau"""
        # Charger les polices - Road Rage pour le HUD, Metal Mania pour les gros textes
        try:
            self.font = pygame.font.Font(str(FONT_ROAD_RAGE), 26)
            self.font_big = pygame.font.Font(str(FONT_METAL_MANIA), 48)
        except (pygame.error, FileNotFoundError):
            self.font = pygame.font.Font(None, 26)
            self.font_big = pygame.font.Font(None, 48)

        # Recuperer les donnees du jeu
        self.current_level = self.game.game_data["current_level"]
        character_id = self.game.game_data["selected_character"]

        # Reset des groupes
        self.all_sprites.empty()
        self.platforms.empty()
        self.enemies.empty()
        self.player_projectiles.empty()
        self.boss_projectiles.empty()
        self.pickups.empty()

        # Creer le joueur
        self.player = Player(character_id, 100, GROUND_Y)
        self.player.health = self.game.game_data["lives"]
        self.player.ultimate_charge = self.game.game_data.get("ultimate_charge", 0)
        self.all_sprites.add(self.player)

        # Charger le niveau
        self._load_level()

        # Reset camera
        self.camera_x = 0

        # Reset rythme
        self.beat_timer = 0
        self.combo = 0

        # Reset celebration
        self.celebration_active = False
        self.celebration_timer = 0
        self.celebration_particles = []

        # Reset affichage des degats
        self.damage_numbers = []

        # Jouer la musique du niveau
        self._play_level_music()

    def _play_level_music(self):
        """Charge et joue la musique du niveau actuel"""
        music_files = {
            1: SND_MUSIC_LEVEL1,
            2: SND_MUSIC_LEVEL2,
            3: SND_MUSIC_BOSS,
        }
        try:
            music_file = music_files.get(self.current_level, SND_MUSIC_LEVEL1)
            music_path = SND_DIR / music_file
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # -1 = boucle infinie
        except (pygame.error, FileNotFoundError) as e:
            print(f"Impossible de charger la musique du niveau: {e}")

    def _load_level(self):
        """Charge le niveau actuel"""
        self.level_width = LEVEL_LENGTHS.get(self.current_level, 3000)
        self._load_background()

        if self.current_level == 1:
            self._setup_level_1()
        elif self.current_level == 2:
            self._setup_level_2()
        elif self.current_level == 3:
            self._setup_level_3()

    def _load_background(self):
        """Charge le background du niveau"""
        bg_files = {
            1: IMG_BG_LEVEL1,
            2: IMG_BG_LEVEL2,
            3: IMG_BG_BOSS,
        }
        try:
            path = IMG_BG_DIR / bg_files.get(self.current_level, IMG_BG_LEVEL1)
            self.background = pygame.image.load(str(path)).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except (pygame.error, FileNotFoundError):
            self.background = None

    def _setup_level_1(self):
        """Configure le niveau 1 - Coulisses (tutoriel)"""
        # Sol avec quelques trous (tutoriel)
        ground_segments = [
            (0, GROUND_Y, 700),      # Debut
            (800, GROUND_Y, 500),    # Apres premier trou
            (1400, GROUND_Y, 600),   # Milieu
            (2100, GROUND_Y, 900),   # Fin
        ]
        for x, y, w in ground_segments:
            ground = Platform(x, y, w, HEIGHT - GROUND_Y + 100, is_ground=True)
            self.platforms.add(ground)

        # Plateformes (incluant celles au-dessus des trous)
        platform_positions = [
            (300, 520, 200, 30),
            (600, 450, 150, 30),
            (720, 550, 100, 30),   # Au-dessus du trou 1
            (900, 380, 180, 30),
            (1200, 480, 200, 30),
            (1320, 550, 100, 30),  # Au-dessus du trou 2
            (1600, 400, 150, 30),
            (2000, 550, 120, 30),  # Au-dessus du trou 3
            (2400, 450, 180, 30),
            (2700, 520, 150, 30),
        ]
        for x, y, w, h in platform_positions:
            plat = Platform(x, y, w, h)
            self.platforms.add(plat)

        # Ennemis (Haters uniquement)
        enemy_positions = [
            (500, GROUND_Y, "hater"),
            (800, GROUND_Y, "hater"),
            (1100, GROUND_Y, "hater"),
            (1500, GROUND_Y, "hater"),
            (1900, GROUND_Y, "hater"),
            (2300, GROUND_Y, "hater"),
        ]
        for x, y, etype in enemy_positions:
            enemy = Enemy(x, y, etype)
            self.enemies.add(enemy)

        # Pickups
        pickup_positions = [
            (400, 480, "note"),
            (700, 410, "note"),
            (1000, 340, "mediator"),
            (1400, 440, "note"),
            (1800, 360, "note"),
            (2200, 400, "mediator"),
        ]
        for x, y, ptype in pickup_positions:
            pickup = Pickup(x, y, ptype)
            self.pickups.add(pickup)

    def _setup_level_2(self):
        """Configure le niveau 2 - Scene (challenge)"""
        # Sol avec trous
        ground_segments = [
            (0, GROUND_Y, 800),
            (1000, GROUND_Y, 600),
            (1800, GROUND_Y, 800),
            (2800, GROUND_Y, 1200),
        ]
        for x, y, w in ground_segments:
            ground = Platform(x, y, w, HEIGHT - GROUND_Y + 100, is_ground=True)
            self.platforms.add(ground)

        # Plateformes (plus vertical)
        platform_positions = [
            (300, 500, 150, 30),
            (500, 400, 120, 30),
            (700, 300, 150, 30),
            (850, 450, 100, 30),  # Au-dessus du trou
            (950, 550, 80, 30),
            (1100, 480, 150, 30),
            (1400, 380, 120, 30),
            (1600, 280, 150, 30),
            (1700, 450, 100, 30),
            (2000, 500, 200, 30),
            (2400, 400, 150, 30),
            (2700, 300, 180, 30),
            (3000, 450, 150, 30),
            (3400, 380, 200, 30),
        ]
        for x, y, w, h in platform_positions:
            plat = Platform(x, y, w, h)
            self.platforms.add(plat)

        # Ennemis (Haters et Rivals)
        enemy_positions = [
            (400, GROUND_Y, "hater"),
            (600, GROUND_Y, "hater"),
            (1200, GROUND_Y, "rival"),
            (1500, GROUND_Y, "hater"),
            (2100, GROUND_Y, "rival"),
            (2500, GROUND_Y, "hater"),
            (2900, GROUND_Y, "rival"),
            (3200, GROUND_Y, "hater"),
            (3600, GROUND_Y, "rival"),
        ]
        for x, y, etype in enemy_positions:
            enemy = Enemy(x, y, etype)
            self.enemies.add(enemy)

        # Pickups
        pickup_positions = [
            (350, 460, "note"),
            (550, 360, "note"),
            (750, 260, "mediator"),
            (1150, 440, "note"),
            (1450, 340, "ampli"),
            (1650, 240, "note"),
            (2050, 460, "note"),
            (2450, 360, "mediator"),
            (2750, 260, "note"),
            (3050, 410, "ampli"),
            (3450, 340, "note"),
        ]
        for x, y, ptype in pickup_positions:
            pickup = Pickup(x, y, ptype)
            self.pickups.add(pickup)

    def _setup_level_3(self):
        """Configure le niveau 3 - Boss Arena"""
        # Sol de l'arene
        ground = Platform(0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y + 100, is_ground=True)
        self.platforms.add(ground)

        # Quelques plateformes pour esquiver
        platform_positions = [
            (200, 500, 150, 30),
            (WIDTH - 350, 500, 150, 30),
            (WIDTH // 2 - 75, 400, 150, 30),
        ]
        for x, y, w, h in platform_positions:
            plat = Platform(x, y, w, h)
            self.platforms.add(plat)

        # Boss
        self.boss = Boss(WIDTH - 200, GROUND_Y)
        self.enemies.add(self.boss)

    def handle_event(self, event):
        """Gere les evenements"""
        if event.type == pygame.KEYDOWN:
            # Pause (pas pendant l'ultime)
            if event.key in CONTROLS["pause"] and not self.ultimate_active:
                self.game.change_scene(STATE_PAUSE)
                return

            # Debug
            if event.key in CONTROLS["debug_hitbox"]:
                self.debug_hitboxes = not self.debug_hitboxes
            if event.key in CONTROLS["debug_skip"]:
                self._complete_level()
            if event.key in CONTROLS["debug_invincible"]:
                self.player.debug_invincible = not self.player.debug_invincible

            # Pendant la sequence ultime: F, G, H pour les 3 pistes
            if self.ultimate_active:
                for i, key in enumerate(LANE_KEYS):
                    if event.key == key:
                        self._ultimate_hit_lane(i)
                return

            # Attaque normale
            if event.key in CONTROLS["attack"]:
                self._player_attack()

            # Lancer l'ultime
            if event.key in CONTROLS["ultimate"]:
                self._player_ultimate()

        elif event.type == pygame.KEYUP:
            # Relacher les touches pendant l'ultime
            if self.ultimate_active:
                for i, key in enumerate(LANE_KEYS):
                    if event.key == key:
                        self.ultimate_lane_pressed[i] = False

    def _player_attack(self):
        """Le joueur attaque - attaque simple sans timing"""
        if not self.player.can_attack():
            return
        if self.ultimate_active:
            return  # Pas d'attaque normale pendant l'ultime
        if self.player.is_crouching:
            return  # Pas d'attaque quand accroupi

        # Creer le projectile (degats fixes)
        direction = 1 if self.player.facing_right else -1
        proj_x = self.player.rect.centerx + (30 * direction)
        proj = Projectile(proj_x, self.player.rect.centery, direction, 1.0)
        self.player_projectiles.add(proj)

        self.player.attack()

    def _player_ultimate(self):
        """Le joueur utilise son ultime - demarre la sequence Guitar Hero"""
        if not self.player.can_use_ultimate():
            return
        if self.ultimate_active:
            return  # Deja en cours

        # Consommer la charge
        self.player.use_ultimate()

        # Demarrer la sequence Guitar Hero
        self.ultimate_active = True
        self.ultimate_notes = []
        self.ultimate_notes_spawned = 0
        self.ultimate_spawn_timer = 0
        self.ultimate_results = []
        self.ultimate_total_damage = ULTIMATE_BASE_DAMAGE
        self.ultimate_lane_pressed = [False, False, False]
        self.player.state = "ultimate"

    def _ultimate_hit_lane(self, lane):
        """Le joueur appuie sur une touche (F=0, G=1, H=2)"""
        if not self.ultimate_active:
            return
        if self.ultimate_lane_pressed[lane]:
            return  # Deja appuye

        self.ultimate_lane_pressed[lane] = True

        # Chercher la note la plus proche sur cette piste
        closest_note = None
        closest_dist = float('inf')

        for note in self.ultimate_notes:
            if note["lane"] == lane:
                dist = abs(note["y"] - HIT_LINE_Y)
                if dist < closest_dist:
                    closest_dist = dist
                    closest_note = note

        # Verifier le timing
        if closest_note and closest_dist <= HIT_ZONE_OK:
            # Determiner le resultat
            if closest_dist <= HIT_ZONE_PERFECT:
                result = "PERFECT!"
                self.ultimate_total_damage += ULTIMATE_DAMAGE_PER_PERFECT
            elif closest_dist <= HIT_ZONE_GOOD:
                result = "GOOD!"
                self.ultimate_total_damage += ULTIMATE_DAMAGE_PER_GOOD
            else:
                result = "OK"
                self.ultimate_total_damage += ULTIMATE_DAMAGE_PER_OK

            self.ultimate_results.append(result)
            self.timing_feedback = result
            self.timing_feedback_timer = 300

            # Supprimer la note
            self.ultimate_notes.remove(closest_note)
        else:
            # Appui sans note = pas de penalite, juste ignorer
            pass

    def _finish_ultimate(self):
        """Termine la sequence ultime et lance l'attaque"""
        self.ultimate_active = False
        self.player.state = "attack"
        self.player.attack_anim_timer = 500  # Animation d'attaque pendant 500ms

        # Creer le projectile ultime avec les degats accumules
        direction = 1 if self.player.facing_right else -1

        # Projectile principal puissant - utilise l'image ultimate du joueur
        proj = Projectile(
            self.player.rect.centerx,
            self.player.rect.centery,
            direction,
            self.ultimate_total_damage
        )
        proj.speed = PROJECTILE_SPEED * 1.5

        # Utiliser l'image ultimate du joueur pour le projectile
        ult_img = self.player.images.get("ultimate")
        if ult_img:
            # Agrandir l'image pour l'effet visuel
            proj.image = pygame.transform.scale(ult_img, (PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2))
            if direction < 0:
                proj.image = pygame.transform.flip(proj.image, True, False)
        else:
            # Fallback: placeholder colore
            proj.image = pygame.Surface((PLAYER_WIDTH * 2, PLAYER_HEIGHT * 2), pygame.SRCALPHA)
            color = (255, 200, 0) if self.player.character_id == 1 else (255, 150, 50)
            proj.image.fill(color)

        proj.rect = proj.image.get_rect(center=proj.rect.center)
        self.player_projectiles.add(proj)

        # Afficher les degats totaux
        self.timing_feedback = f"DAMAGE: {self.ultimate_total_damage}!"
        self.timing_feedback_timer = 1000

    def update(self, dt):
        """Met a jour le gameplay"""
        dt_ms = dt * 1000

        # Timer pour animations visuelles (toujours actif)
        self.animation_time += dt

        # Pendant l'ultime: TOUT EST FIGE sauf la sequence Guitar Hero
        if self.ultimate_active:
            self._update_ultimate_sequence(dt_ms)
            # Feedback timer uniquement
            if self.timing_feedback_timer > 0:
                self.timing_feedback_timer -= dt_ms
            return  # Ne pas mettre a jour le reste du jeu

        # Pendant la celebration: animation seulement
        if self.celebration_active:
            self._update_celebration(dt_ms)
            return

        # Input joueur normal
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)

        # Mise a jour des entites
        self.player.update(dt, self.platforms)

        for proj in self.player_projectiles:
            proj.update(dt)

        for proj in self.boss_projectiles:
            proj.update(dt)

        for pickup in self.pickups:
            pickup.update(dt)

        # Mise a jour des ennemis
        # Liste des ennemis normaux pour eviter les collisions entre eux
        normal_enemies = [e for e in self.enemies if not isinstance(e, Boss)]
        for enemy in self.enemies:
            if isinstance(enemy, Boss):
                enemy.update(dt, self.player.rect, self.boss_projectiles)
            else:
                enemy.update(dt, self.player.rect, self.platforms, normal_enemies)

        # Empecher les ennemis de se chevaucher
        self._resolve_enemy_collisions()

        # Verifier les chutes dans le vide
        self._check_fall_death()

        # Collisions
        self._check_collisions()

        # Camera
        self._update_camera()

        # Feedback timer
        if self.timing_feedback_timer > 0:
            self.timing_feedback_timer -= dt_ms

        # Verifier fin de niveau
        self._check_level_end()

        # Verifier game over
        if self.player.health <= 0:
            self.game.game_data["score"] = self.game.game_data.get("score", 0)
            self.game.change_scene(STATE_GAME_OVER)

    def _update_ultimate_sequence(self, dt_ms):
        """Met a jour la sequence Guitar Hero avec notes qui tombent"""
        # Spawn de nouvelles notes
        self.ultimate_spawn_timer += dt_ms
        if self.ultimate_spawn_timer >= NOTE_SPAWN_INTERVAL:
            if self.ultimate_notes_spawned < ULTIMATE_NOTE_COUNT:
                self.ultimate_spawn_timer = 0
                # Creer une note sur une piste aleatoire
                lane = random.randint(0, LANE_COUNT - 1)
                self.ultimate_notes.append({
                    "lane": lane,
                    "y": TRACK_Y  # Commence en haut
                })
                self.ultimate_notes_spawned += 1

        # Faire tomber les notes
        notes_to_remove = []
        for note in self.ultimate_notes:
            note["y"] += NOTE_FALL_SPEED

            # Note ratee (passee sous la ligne de frappe)
            if note["y"] > HIT_LINE_Y + HIT_ZONE_OK + NOTE_SIZE:
                notes_to_remove.append(note)
                self.ultimate_results.append("MISS")
                self.timing_feedback = "MISS"
                self.timing_feedback_timer = 300

        for note in notes_to_remove:
            self.ultimate_notes.remove(note)

        # Verifier si la sequence est terminee
        if self.ultimate_notes_spawned >= ULTIMATE_NOTE_COUNT and len(self.ultimate_notes) == 0:
            self._finish_ultimate()

    def _check_fall_death(self):
        """Verifie si des entites sont tombees dans le vide"""
        fall_limit = HEIGHT + 50  # En dessous de l'ecran

        # Joueur tombe dans le vide
        if self.player.rect.top > fall_limit:
            self.player.health = 0  # Mort instantanee

        # Ennemis tombent dans le vide
        for enemy in list(self.enemies):
            if enemy.rect.top > fall_limit:
                enemy.kill()

    def _resolve_enemy_collisions(self):
        """Empeche les ennemis de se chevaucher"""
        # Filtrer les ennemis vivants seulement (pas le boss, pas les morts)
        enemies_list = [e for e in self.enemies if not isinstance(e, Boss) and not e.is_dead]

        # Distance minimale entre ennemis pour eviter l'oscillation
        min_separation = 10

        for i, enemy1 in enumerate(enemies_list):
            for enemy2 in enemies_list[i + 1:]:
                # Calculer la distance entre les centres
                dist_x = abs(enemy1.rect.centerx - enemy2.rect.centerx)
                min_dist = (enemy1.rect.width + enemy2.rect.width) // 2 + min_separation

                # Si trop proches (meme sans chevauchement strict)
                if dist_x < min_dist and enemy1.rect.colliderect(enemy2.rect.inflate(min_separation * 2, 0)):
                    # Calculer combien il faut pousser
                    push_amount = (min_dist - dist_x) // 2 + 1

                    # Pousser les ennemis dans des directions opposees
                    if enemy1.rect.centerx < enemy2.rect.centerx:
                        enemy1.rect.x -= push_amount
                        enemy2.rect.x += push_amount
                    else:
                        enemy1.rect.x += push_amount
                        enemy2.rect.x -= push_amount

    def _check_collisions(self):
        """Verifie toutes les collisions"""
        # Projectiles joueur -> Ennemis
        for proj in self.player_projectiles:
            for enemy in self.enemies:
                if proj.rect.colliderect(enemy.rect):
                    proj.kill()
                    is_dead = enemy.take_damage(proj.damage)
                    self.player.add_ultimate_charge(ULTIMATE_CHARGE_PER_HIT)

                    if is_dead:
                        self.game.game_data["score"] += enemy.score_value
                        if isinstance(enemy, Boss):
                            self.boss = None
                        enemy.kill()
                    break

        # Projectiles boss -> Joueur
        for proj in self.boss_projectiles:
            if proj.rect.colliderect(self.player.rect):
                proj.kill()
                if self.player.take_damage(proj.damage):
                    self.game.game_data["lives"] = self.player.health

        # Ennemis -> Joueur (contact)
        for enemy in self.enemies:
            if hasattr(enemy, 'is_dead') and enemy.is_dead:
                continue  # Ignorer les ennemis morts
            if self.player.rect.colliderect(enemy.rect):
                # Verifier si le joueur saute sur la tete de l'ennemi (pas le boss)
                if (not isinstance(enemy, Boss) and
                    self.player.velocity_y > 0 and
                    self.player.rect.bottom <= enemy.rect.top + 30):
                    # Tuer l'ennemi en sautant dessus
                    enemy.is_dead = True
                    enemy.state = "dead"
                    self.game.game_data["score"] += enemy.score_value
                    # Faire rebondir le joueur
                    self.player.velocity_y = -10
                    self.player.rect.bottom = enemy.rect.top
                else:
                    # Collision normale - le joueur prend des degats
                    if self.player.take_damage(enemy.damage):
                        self.game.game_data["lives"] = self.player.health
                        # Repousser le joueur
                        knockback = -5 if self.player.rect.centerx < enemy.rect.centerx else 5
                        self.player.rect.x += knockback * 10

        # Joueur -> Pickups
        for pickup in self.pickups:
            if self.player.rect.colliderect(pickup.rect):
                self._collect_pickup(pickup)
                pickup.kill()

    def _collect_pickup(self, pickup):
        """Collecte un pickup"""
        if pickup.pickup_type == "note":
            self.game.game_data["score"] += PICKUP_NOTE_SCORE
        elif pickup.pickup_type == "mediator":
            self.player.add_ultimate_charge(PICKUP_MEDIATOR_ULTIMATE)
        elif pickup.pickup_type == "ampli":
            # Boost temporaire (a implementer si besoin)
            self.game.game_data["score"] += PICKUP_NOTE_SCORE * 2

    def _update_camera(self):
        """Met a jour la position de la camera"""
        # La camera suit le joueur
        target_x = self.player.rect.centerx - WIDTH // 3

        # Limiter aux bords du niveau
        target_x = max(0, min(target_x, self.level_width - WIDTH))

        # Lissage
        self.camera_x += (target_x - self.camera_x) * 0.1

    def _check_level_end(self):
        """Verifie si le niveau est termine"""
        if self.celebration_active:
            return  # Deja en celebration

        if self.current_level == 3:
            # Niveau boss - victoire si boss mort
            if self.boss is None or self.boss not in self.enemies:
                self._start_celebration()
        else:
            # Autres niveaux - atteindre la fin
            if self.player.rect.right >= self.level_width - 50:
                self._complete_level()

    def _start_celebration(self):
        """Demarre l'animation de celebration apres avoir battu le boss"""
        self.celebration_active = True
        self.celebration_timer = 0
        self.celebration_particles = []
        # Generer des particules initiales
        for _ in range(50):
            self._spawn_celebration_particle()

        # Jouer la musique de victoire
        try:
            music_path = SND_DIR / SND_VICTORY
            pygame.mixer.music.load(str(music_path))
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
        except (pygame.error, FileNotFoundError) as e:
            print(f"Impossible de charger la musique de victoire: {e}")

    def _spawn_celebration_particle(self):
        """Cree une particule de celebration (confetti)"""
        particle = {
            "x": random.randint(0, WIDTH),
            "y": random.randint(-50, 0),
            "vel_x": random.uniform(-2, 2),
            "vel_y": random.uniform(2, 5),
            "color": random.choice([YELLOW, PURPLE, GREEN, ORANGE, WHITE]),
            "size": random.randint(5, 12),
            "rotation": random.uniform(0, 360),
            "rot_speed": random.uniform(-5, 5),
        }
        self.celebration_particles.append(particle)

    def _update_celebration(self, dt_ms):
        """Met a jour l'animation de celebration"""
        self.celebration_timer += dt_ms

        # Ajouter de nouvelles particules
        if len(self.celebration_particles) < 100 and random.random() < 0.3:
            self._spawn_celebration_particle()

        # Mettre a jour les particules
        for particle in self.celebration_particles[:]:
            particle["x"] += particle["vel_x"]
            particle["y"] += particle["vel_y"]
            particle["rotation"] += particle["rot_speed"]

            # Supprimer si hors ecran
            if particle["y"] > HEIGHT + 50:
                self.celebration_particles.remove(particle)

        # Apres 7 secondes, passer a l'ecran de victoire
        if self.celebration_timer >= 7000:
            self._complete_level()

    def _complete_level(self):
        """Complete le niveau actuel"""
        # Sauvegarder l'etat du joueur avant de changer de niveau
        self.game.game_data["lives"] = self.player.health
        self.game.game_data["ultimate_charge"] = self.player.ultimate_charge

        if self.current_level < 3:
            # Passer au niveau suivant
            self.game.game_data["current_level"] += 1
            self.enter()
        else:
            # Victoire!
            self.game.change_scene(STATE_VICTORY)

    def draw(self, screen):
        """Dessine le gameplay"""
        # Background
        if self.background:
            # Parallax simple
            bg_offset = int(self.camera_x * 0.3) % WIDTH
            screen.blit(self.background, (-bg_offset, 0))
            screen.blit(self.background, (WIDTH - bg_offset, 0))
        else:
            self._draw_placeholder_bg(screen)

        # Plateformes
        for platform in self.platforms:
            draw_rect = platform.rect.move(-self.camera_x, 0)
            if draw_rect.right > 0 and draw_rect.left < WIDTH:
                screen.blit(platform.image, draw_rect)

        # Pickups
        for pickup in self.pickups:
            draw_rect = pickup.rect.move(-self.camera_x, 0)
            if draw_rect.right > 0 and draw_rect.left < WIDTH:
                screen.blit(pickup.image, draw_rect)

        # Ennemis
        for enemy in self.enemies:
            if isinstance(enemy, Boss):
                enemy.draw(screen, self.camera_x)
            else:
                enemy.draw(screen, self.camera_x)

        # Projectiles
        for proj in self.player_projectiles:
            draw_rect = proj.rect.move(-self.camera_x, 0)
            screen.blit(proj.image, draw_rect)

        for proj in self.boss_projectiles:
            draw_rect = proj.rect.move(-self.camera_x, 0)
            screen.blit(proj.image, draw_rect)

        # Joueur
        player_draw_rect = self.player.rect.move(-self.camera_x, 0)
        # Effet de clignotement si invincible
        if self.player.invincible:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                screen.blit(self.player.image, player_draw_rect)
        else:
            screen.blit(self.player.image, player_draw_rect)

        # Debug hitboxes
        if self.debug_hitboxes:
            self._draw_debug_hitboxes(screen)

        # HUD
        self._draw_hud(screen)

        # Barre Guitar Hero (UNIQUEMENT pendant l'ultime)
        if self.ultimate_active:
            self._draw_ultimate_overlay(screen)
            self._draw_rhythm_bar(screen)

        # Feedback timing
        if self.timing_feedback_timer > 0:
            self._draw_timing_feedback(screen)

        # Celebration (apres avoir battu le boss)
        if self.celebration_active:
            self._draw_celebration(screen)

    def _draw_celebration(self, screen):
        """Dessine l'animation de celebration"""
        # Fond semi-transparent dore
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 215, 0, 50))  # Or transparent
        screen.blit(overlay, (0, 0))

        # Dessiner les particules (confettis)
        for particle in self.celebration_particles:
            # Dessiner un rectangle tourne (confetti)
            size = particle["size"]
            color = particle["color"]
            x, y = int(particle["x"]), int(particle["y"])

            # Simple rectangle pour le confetti
            pygame.draw.rect(screen, color, (x - size//2, y - size//2, size, size))

        # Texte "BOSS VAINCU!" avec effet de pulsation
        pulse = 1.0 + math.sin(self.celebration_timer / 200) * 0.15
        font_size = int(72 * pulse)
        try:
            font = pygame.font.Font(str(FONT_METAL_MANIA), font_size)
        except (pygame.error, FileNotFoundError):
            font = pygame.font.Font(None, font_size)

        # Ombre du texte
        shadow_text = font.render("BOSS VAINCU!", True, (50, 50, 50))
        shadow_rect = shadow_text.get_rect(center=(WIDTH // 2 + 4, HEIGHT // 3 + 4))
        screen.blit(shadow_text, shadow_rect)

        # Texte principal
        text = font.render("BOSS VAINCU!", True, YELLOW)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(text, text_rect)

        # Sous-texte
        try:
            sub_font = pygame.font.Font(str(FONT_ROAD_RAGE), 28)
        except (pygame.error, FileNotFoundError):
            sub_font = pygame.font.Font(None, 28)
        sub_text = sub_font.render("Tu es une vraie Rockstar!", True, WHITE)
        sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 160))
        screen.blit(sub_text, sub_rect)

        # Compte a rebours avant victoire
        remaining = max(0, 7000 - self.celebration_timer) // 1000 + 1
        countdown_text = sub_font.render(f"Victoire dans {remaining}...", True, GRAY)
        countdown_rect = countdown_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(countdown_text, countdown_rect)

    def _draw_placeholder_bg(self, screen):
        """Dessine un fond placeholder"""
        # Gradient selon le niveau
        colors = {
            1: ((40, 30, 50), (60, 40, 70)),   # Coulisses - violet sombre
            2: ((50, 40, 30), (80, 60, 40)),   # Scene - marron/orange
            3: ((60, 20, 30), (90, 30, 40)),   # Boss - rouge sombre
        }
        c1, c2 = colors.get(self.current_level, ((30, 30, 40), (50, 50, 60)))

        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(c1[0] + (c2[0] - c1[0]) * ratio)
            g = int(c1[1] + (c2[1] - c1[1]) * ratio)
            b = int(c1[2] + (c2[2] - c1[2]) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

    def _draw_debug_hitboxes(self, screen):
        """Dessine les hitboxes en mode debug"""
        # Joueur
        player_rect = self.player.rect.move(-self.camera_x, 0)
        pygame.draw.rect(screen, GREEN, player_rect, 2)

        # Ennemis
        for enemy in self.enemies:
            enemy_rect = enemy.rect.move(-self.camera_x, 0)
            pygame.draw.rect(screen, RED, enemy_rect, 2)

        # Projectiles
        for proj in self.player_projectiles:
            proj_rect = proj.rect.move(-self.camera_x, 0)
            pygame.draw.rect(screen, YELLOW, proj_rect, 2)

        for proj in self.boss_projectiles:
            proj_rect = proj.rect.move(-self.camera_x, 0)
            pygame.draw.rect(screen, ORANGE, proj_rect, 2)

    def _draw_hud(self, screen):
        """Dessine le HUD"""
        # Vie (coeurs/guitares)
        for i in range(PLAYER_MAX_HEALTH):
            x = HUD_MARGIN + i * (HUD_HEALTH_SIZE + 10)
            y = HUD_MARGIN

            if i < self.player.health:
                color = RED
            else:
                color = GRAY

            # Dessiner un coeur simple
            pygame.draw.circle(screen, color, (x + 10, y + 15), 10)
            pygame.draw.circle(screen, color, (x + 25, y + 15), 10)
            pygame.draw.polygon(screen, color, [
                (x, y + 20),
                (x + 35, y + 20),
                (x + 17, y + 40)
            ])

        # Score
        score_text = self.font.render(f"Score: {self.game.game_data['score']}", True, WHITE)
        screen.blit(score_text, (WIDTH - 200, HUD_MARGIN))

        # Combo
        if self.combo > 1:
            combo_text = self.font_big.render(f"x{self.combo}", True, YELLOW)
            screen.blit(combo_text, (WIDTH - 100, HUD_MARGIN + 30))

        # Niveau
        level_name = LEVEL_NAMES[self.current_level - 1]
        level_text = self.font.render(f"Niveau {self.current_level}: {level_name}", True, WHITE)
        screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HUD_MARGIN))

        # Jauge ultime
        ult_bar_width = 150
        ult_bar_height = 15
        ult_x = HUD_MARGIN
        ult_y = HUD_MARGIN + 60

        # Effet special quand ultime au max
        if self.player.can_use_ultimate():
            # Effet de pulsation (scale)
            pulse = 1.0 + math.sin(self.animation_time * 8) * 0.08
            pulse_width = int(ult_bar_width * pulse)
            pulse_height = int(ult_bar_height * pulse)
            pulse_x = ult_x - (pulse_width - ult_bar_width) // 2
            pulse_y = ult_y - (pulse_height - ult_bar_height) // 2

            # Glow effect (halo lumineux)
            glow_alpha = int(100 + math.sin(self.animation_time * 6) * 55)
            glow_surface = pygame.Surface((pulse_width + 20, pulse_height + 20), pygame.SRCALPHA)
            glow_color = (255, 200, 0, glow_alpha)
            pygame.draw.rect(glow_surface, glow_color, (0, 0, pulse_width + 20, pulse_height + 20), border_radius=8)
            screen.blit(glow_surface, (pulse_x - 10, pulse_y - 10))

            # Couleur qui oscille entre violet et or
            color_shift = (math.sin(self.animation_time * 10) + 1) / 2
            ult_r = int(150 + color_shift * 105)
            ult_g = int(0 + color_shift * 215)
            ult_b = int(255 - color_shift * 255)
            ult_color = (ult_r, ult_g, ult_b)

            # Fond
            pygame.draw.rect(screen, DARK_GRAY, (pulse_x, pulse_y, pulse_width, pulse_height), border_radius=4)
            # Barre remplie
            pygame.draw.rect(screen, ult_color, (pulse_x, pulse_y, pulse_width, pulse_height), border_radius=4)
            # Effet de brillance qui se deplace
            shine_x = int((math.sin(self.animation_time * 4) + 1) / 2 * (pulse_width - 30))
            shine_surface = pygame.Surface((30, pulse_height), pygame.SRCALPHA)
            for i in range(30):
                alpha = int(150 * (1 - abs(i - 15) / 15))
                pygame.draw.line(shine_surface, (255, 255, 255, alpha), (i, 0), (i, pulse_height))
            screen.blit(shine_surface, (pulse_x + shine_x, pulse_y))
            # Bordure
            pygame.draw.rect(screen, YELLOW, (pulse_x, pulse_y, pulse_width, pulse_height), 2, border_radius=4)

            # Label avec effet
            label_color = (255, int(200 + math.sin(self.animation_time * 8) * 55), 0)
            ult_label = self.font.render("ULTIME PRET!", True, label_color)
        else:
            # Jauge normale
            pygame.draw.rect(screen, GRAY, (ult_x, ult_y, ult_bar_width, ult_bar_height))
            ult_fill = int((self.player.ultimate_charge / ULTIMATE_CHARGE_MAX) * ult_bar_width)
            pygame.draw.rect(screen, BLUE, (ult_x, ult_y, ult_fill, ult_bar_height))
            pygame.draw.rect(screen, WHITE, (ult_x, ult_y, ult_bar_width, ult_bar_height), 2)
            ult_label = self.font.render("ULTIME 'K'", True, WHITE)

        screen.blit(ult_label, (ult_x, ult_y + 18))

        # Debug info
        if self.debug_hitboxes:
            debug_text = self.font.render(
                f"DEBUG | Invincible: {self.player.debug_invincible} | F1:Hitbox F2:Skip F3:Godmode",
                True, YELLOW
            )
            screen.blit(debug_text, (10, HEIGHT - 30))

    def _draw_ultimate_overlay(self, screen):
        """Dessine l'overlay Guitar Hero pendant la sequence ultime"""
        # Fond semi-transparent
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        # Titre ULTIMATE
        title = self.font_big.render("ULTIMATE!", True, YELLOW)
        title_rect = title.get_rect(center=(WIDTH // 2, 50))
        screen.blit(title, title_rect)

        # Degats accumules
        dmg_text = self.font_big.render(f"Damage: {self.ultimate_total_damage}", True, ORANGE)
        dmg_rect = dmg_text.get_rect(center=(WIDTH // 2, 90))
        screen.blit(dmg_text, dmg_rect)

        # Compteur de notes
        notes_left = ULTIMATE_NOTE_COUNT - len(self.ultimate_results)
        count_text = self.font.render(f"Notes: {notes_left}/{ULTIMATE_NOTE_COUNT}", True, WHITE)
        count_rect = count_text.get_rect(center=(WIDTH // 2, 120))
        screen.blit(count_text, count_rect)

    def _draw_rhythm_bar(self, screen):
        """Dessine la piste Guitar Hero avec les 3 colonnes (F, G, H)"""
        # Fond de la piste
        track_rect = pygame.Rect(TRACK_X, TRACK_Y, TRACK_WIDTH, TRACK_HEIGHT)
        pygame.draw.rect(screen, (20, 20, 30), track_rect)

        # Dessiner les 3 pistes (colonnes)
        for i in range(LANE_COUNT):
            lane_x = TRACK_X + i * LANE_WIDTH
            lane_color = LANE_COLORS[i]

            # Fond de la piste (plus sombre)
            dark_color = (lane_color[0] // 4, lane_color[1] // 4, lane_color[2] // 4)
            pygame.draw.rect(screen, dark_color,
                           (lane_x + 2, TRACK_Y, LANE_WIDTH - 4, TRACK_HEIGHT))

            # Separateurs entre pistes
            pygame.draw.line(screen, GRAY, (lane_x, TRACK_Y), (lane_x, TRACK_Y + TRACK_HEIGHT), 2)

        # Ligne de frappe (zone cible)
        pygame.draw.line(screen, WHITE,
                        (TRACK_X, HIT_LINE_Y),
                        (TRACK_X + TRACK_WIDTH, HIT_LINE_Y), 4)

        # Zones de timing sur la ligne de frappe
        for i in range(LANE_COUNT):
            lane_x = TRACK_X + i * LANE_WIDTH + LANE_WIDTH // 2
            lane_color = LANE_COLORS[i]

            # Cercle cible (plus brillant si touche pressee)
            if self.ultimate_lane_pressed[i]:
                pygame.draw.circle(screen, lane_color, (lane_x, HIT_LINE_Y), NOTE_SIZE // 2 + 5)
                pygame.draw.circle(screen, WHITE, (lane_x, HIT_LINE_Y), NOTE_SIZE // 2, 3)
            else:
                dark_color = (lane_color[0] // 2, lane_color[1] // 2, lane_color[2] // 2)
                pygame.draw.circle(screen, dark_color, (lane_x, HIT_LINE_Y), NOTE_SIZE // 2)
                pygame.draw.circle(screen, lane_color, (lane_x, HIT_LINE_Y), NOTE_SIZE // 2, 2)

        # Dessiner les notes qui tombent
        for note in self.ultimate_notes:
            lane_x = TRACK_X + note["lane"] * LANE_WIDTH + LANE_WIDTH // 2
            lane_color = LANE_COLORS[note["lane"]]

            # Note (cercle colore)
            pygame.draw.circle(screen, lane_color, (lane_x, int(note["y"])), NOTE_SIZE // 2)
            pygame.draw.circle(screen, WHITE, (lane_x, int(note["y"])), NOTE_SIZE // 2, 2)

            # Trainee lumineuse
            pygame.draw.line(screen, lane_color,
                           (lane_x, int(note["y"]) - NOTE_SIZE // 2),
                           (lane_x, int(note["y"]) - NOTE_SIZE), 4)

        # Bordure de la piste
        pygame.draw.rect(screen, WHITE, track_rect, 3)

        # Labels des touches (F, G, H)
        key_names = ["F", "G", "H"]
        for i in range(LANE_COUNT):
            lane_x = TRACK_X + i * LANE_WIDTH + LANE_WIDTH // 2
            key_text = self.font_big.render(key_names[i], True, LANE_COLORS[i])
            key_rect = key_text.get_rect(center=(lane_x, TRACK_Y + TRACK_HEIGHT + 30))
            screen.blit(key_text, key_rect)

        # Afficher les resultats (cercles colores en bas)
        result_colors = {"PERFECT!": YELLOW, "GOOD!": GREEN, "OK": BLUE, "MISS": RED}
        start_x = TRACK_X
        for i, result in enumerate(self.ultimate_results[-8:]):  # Max 8 derniers resultats
            color = result_colors.get(result, WHITE)
            pygame.draw.circle(screen, color, (start_x + i * 30 + 15, TRACK_Y + TRACK_HEIGHT + 70), 10)

    def _draw_timing_feedback(self, screen):
        """Dessine le feedback de timing"""
        colors = {
            "PERFECT!": YELLOW,
            "GOOD!": GREEN,
            "OK": BLUE,
            "MISS": RED,
        }
        color = colors.get(self.timing_feedback, WHITE)

        # Taille selon importance
        if self.timing_feedback == "PERFECT!":
            font = self.font_big
        else:
            font = self.font

        text = font.render(self.timing_feedback, True, color)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))

        # Fond semi-transparent
        bg_rect = text_rect.inflate(20, 10)
        bg_surf = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surf.fill((0, 0, 0, 150))
        screen.blit(bg_surf, bg_rect)

        screen.blit(text, text_rect)
