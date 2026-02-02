# 🚀 Quick Start - Rockstar Bros

**Pour démarrer en 5 minutes avec Claude Code**

---

## 📦 Ce que tu as reçu

- **7 fichiers de documentation** prêts à utiliser avec Claude Code
- **Toute l'architecture** du projet définie
- **Un plan de développement** sur 5 jours
- **Les conventions** de code à suivre

---

## ⚡ Démarrage ultra-rapide

### 1. Créer le projet (30 secondes)

```bash
mkdir rockstar-bros
cd rockstar-bros
```

### 2. Copier la documentation (30 secondes)

```bash
# Copier les fichiers fournis
cp -r /chemin/vers/.claude .
cp -r /chemin/vers/docs .
cp /chemin/vers/README.md .
cp /chemin/vers/INSTALLATION.md .
```

### 3. Lancer Claude Code (5 secondes)

```bash
claude-code
```

### 4. Première commande (2 minutes)

Dans Claude Code, tape :

```
Crée la structure de base du projet : main.py, settings.py, 
et le dossier scenes/ avec base.py et menu.py. 
Utilise la structure définie dans .claude/architecture.md
```

✅ **C'est parti !**

---

## 🎯 Les 3 fichiers les plus importants

### 1. `.claude/project-context.md` ⭐⭐⭐
**Le plus important** - Vue d'ensemble complète
- Concept du jeu
- Architecture technique
- Ce qui va dans chaque fichier
- Timeline de développement

**Lis-le en premier !**

### 2. `.claude/architecture.md` ⭐⭐
Architecture détaillée
- Arborescence complète
- Flux de données
- Responsabilités par fichier
- Exemples de code

**Claude Code s'en sert automatiquement**

### 3. `.claude/asset-tracker.md` ⭐
Liste des assets à créer
- 35-40 images nécessaires
- Priorités (MVP vs complet)
- Dimensions recommandées
- Outils de création

**Pour savoir quoi créer comme sprites**

---

## 📋 Plan d'action (Jour 1)

### Matin (2-3h)

1. **Lire la doc** (30 min)
   - `README.md`
   - `.claude/project-context.md`

2. **Créer la structure** (30 min)
   ```
   Claude Code : "Crée main.py, settings.py, 
   scenes/base.py et scenes/menu.py"
   ```

3. **Joueur qui bouge** (1h)
   ```
   Claude Code : "Crée entities/player.py avec 
   mouvement gauche/droite et animation"
   ```

4. **Test** (15 min)
   ```
   python main.py
   ```

### Après-midi (2-3h)

5. **Saut + gravité** (1h)
   ```
   Claude Code : "Ajoute le saut et la gravité 
   au joueur avec détection du sol"
   ```

6. **Première plateforme** (30 min)
   ```
   Claude Code : "Crée une classe Platform et 
   ajoute-en une dans gameplay.py"
   ```

7. **Test + polish** (1h)
   - Tester le gameplay
   - Ajuster les constantes dans `settings.py`
   - Utiliser rectangles colorés comme placeholders

**Objectif fin Jour 1** : Joueur qui saute sur des plateformes ✅

---

## 💬 Commandes utiles pour Claude Code

### Structure et fichiers

```
"Crée la structure complète du projet selon .claude/architecture.md"

"Ajoute un nouveau fichier entities/enemies.py avec la classe Hater"

"Crée le système de scènes avec menu, gameplay, et game_over"
```

### Gameplay

```
"Implémente le système d'attaque : le joueur tire un projectile 
quand j'appuie sur J"

"Ajoute un ennemi Hater qui patrouille de gauche à droite"

"Crée le système de collision entre projectiles et ennemis"
```

### Système Guitar Hero

```
"Crée systems/rhythm.py avec un métronome à 120 BPM 
et détection de timing parfait"

"Ajoute la barre Guitar Hero visible en haut de l'écran 
selon la doc"
```

### Debug

```
"Ajoute un mode debug avec F1 pour afficher les hitboxes"

"Crée une fonction helper pour charger les images avec 
fallback si introuvable"
```

---

## 🎨 Assets - Par où commencer ?

### Jour 1-2 : 100% Placeholders

**Ne perds PAS de temps sur les sprites !**

```python
# Dans settings.py
PLACEHOLDER_COLORS = {
    "player": (50, 150, 255),      # Bleu
    "enemy": (150, 50, 150),       # Violet
    "projectile": (255, 255, 0),   # Jaune
    "platform": (100, 70, 40),     # Marron
}
```

Utilise des rectangles colorés pour tout.

### Jour 3 : Assets prioritaires

**Seulement si le gameplay fonctionne bien !**

Priorité absolue (9 images) :
- 2 sprites joueur (idle + run)
- 1 sprite ennemi
- 1 sprite projectile
- 1 texture plateforme
- 2 icônes UI vie (guitare pleine/vide)
- 2 éléments barre Guitar Hero

### Jour 4 : Assets complets

Si tu as le temps :
- Backgrounds (3)
- Boss (2-3 sprites)
- Écrans (menu, game over, etc.)

---

## ⚠️ Pièges à éviter

### ❌ Ne pas faire

1. **Commencer par les assets**
   > Fais d'abord le gameplay avec placeholders

2. **Coder sans tester**
   > Teste après chaque ajout (joueur bouge → saut → gravité → etc.)

3. **Tout mettre dans main.py**
   > Utilise les scènes (voir `.claude/architecture.md`)

4. **Ignorer delta time (dt)**
   > Tous les mouvements doivent utiliser `dt`

5. **Oublier le système Guitar Hero**
   > C'est la feature principale ! Fais-le fonctionner tôt

### ✅ À faire

1. **Développement itératif**
   > Une fonctionnalité à la fois

2. **Tester constamment**
   > `python main.py` après chaque ajout

3. **Suivre l'architecture**
   > Respecte la structure des scènes

4. **Commenter le code**
   > Surtout les parties complexes (collisions, boss AI)

5. **Garder settings.py propre**
   > Toutes les constantes dedans, pas dans le code

---

## 🐛 Debug rapide

### Le jeu crash au lancement

```bash
# Vérifier Python et Pygame
python --version  # Doit être 3.8+
pip show pygame   # Doit être installé

# Vérifier erreurs
python main.py
```

### Claude Code ne comprend pas

```
"Lis .claude/project-context.md et explique-moi 
comment est structuré le projet"
```

### Le joueur ne bouge pas

Vérifie dans `player.py` :
```python
# Doit utiliser dt
self.rect.x += self.velocity_x * dt  # ✅
# Pas juste
self.rect.x += 5  # ❌
```

---

## 📊 Progression recommandée

### Jour 1 (Aujourd'hui)
- [x] Lire docs principales
- [ ] Structure projet créée
- [ ] Joueur bouge + saute
- [ ] Gravité OK
- [ ] 1 plateforme

**Temps estimé** : 4-6h

### Jours 2-5
Voir le planning détaillé dans :
- `README.md` section "Objectifs par jour"
- `.claude/project-context.md` section "Workflow recommandé"

---

## 🎓 Ressources

### Documentation interne
- `.claude/project-context.md` - Le guide ultime
- `docs/STRUCTURE.md` - Comment organiser le code
- `docs/CONVENTIONS.md` - Style de code

### Documentation externe
- [Pygame Docs](https://www.pygame.org/docs/)
- [Python Docs](https://docs.python.org/3/)

### Assets gratuits
- [OpenGameArt](https://opengameart.org)
- [Kenney.nl](https://kenney.nl)
- [Itch.io](https://itch.io/game-assets/free)

---

## ✅ Checklist avant de commencer

- [ ] Documentation copiée dans le projet
- [ ] `ls .claude/` montre 3 fichiers
- [ ] Lu `README.md` et `.claude/project-context.md`
- [ ] Python 3.8+ installé
- [ ] Pygame installé
- [ ] Claude Code fonctionne

**Tout est ✅ ? Fonce ! 🚀**

---

## 🎉 Derniers conseils

1. **Prends le temps de lire la doc** (1h investie = 5h gagnées)
2. **Suis l'architecture proposée** (elle a fait ses preuves)
3. **Développe étape par étape** (pas tout d'un coup)
4. **Teste souvent** (chaque 30 min minimum)
5. **Utilise Claude Code intelligemment** (commandes claires et spécifiques)

**La doc est là pour t'aider. Claude Code aussi. Tu as tout ce qu'il faut ! 🎸🎮**

---

**Questions ? Consulte `INSTALLATION.md` pour plus de détails.**

**Bon code ! 💻**