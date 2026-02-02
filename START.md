# Setup macOS — Rockstar-Bros (Python / Pygame)

Guide complet pour configurer et travailler sur le projet **Rockstar-Bros** sous macOS.

---

## ✅ Prérequis

Avant de commencer, assure-toi d'avoir installé :

- **Python 3** (version 3.8 ou supérieure recommandée)
- **Git**
- **VS Code** (recommandé) ou un autre éditeur de code

### Vérifier Python
```bash
python3 --version
```

Si Python n'est pas installé, télécharge-le depuis [python.org](https://www.python.org/downloads/).

---

## 📦 Installation initiale (première fois)

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd Rockstar-Bros
```

### 2. Créer l'environnement virtuel
```bash
python3 -m venv .venv
```

### 3. Activer l'environnement virtuel
```bash
source .venv/bin/activate
```

✅ **Vérification** : tu dois voir `(.venv)` au début de ta ligne de commande.

### 4. Mettre à jour pip
```bash
python3 -m pip install --upgrade pip
```

### 5. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 6. Vérifier l'installation de Pygame
```bash
python3 -c "import pygame; print('✅ Pygame installé correctement')"
```

---

## 🚀 Routine quotidienne (à chaque session de travail)

### 1. Naviguer vers le projet
```bash
cd /chemin/vers/Rockstar-Bros
```

### 2. Activer l'environnement virtuel
```bash
source .venv/bin/activate
```

### 3. Récupérer les dernières modifications
```bash
git pull
```

### 4. Mettre à jour les dépendances (si nécessaire)

Si quelqu'un a ajouté de nouvelles librairies :
```bash
pip install -r requirements.txt
```

### 5. Lancer le jeu
```bash
python3 main.py
```

---

## 📚 Ajouter une nouvelle librairie (procédure obligatoire)

**⚠️ Règle d'équipe** : Chaque fois qu'un membre ajoute une librairie, il doit suivre cette procédure complète.

### Étapes à suivre dans l'ordre

#### 1. Activer l'environnement virtuel
```bash
source .venv/bin/activate
```

#### 2. Installer la nouvelle librairie
```bash
pip install <nom_de_la_librairie>
```

#### 3. Mettre à jour requirements.txt
```bash
pip freeze > requirements.txt
```

#### 4. Commit et push
```bash
git add requirements.txt
git commit -m "Add <nom_de_la_librairie> dependency"
git push
```

### Exemple complet
```bash
# Activer le venv
source .venv/bin/activate

# Installer la librairie
pip install requests

# Mettre à jour requirements.txt
pip freeze > requirements.txt

# Commit
git add requirements.txt
git commit -m "Add requests dependency"
git push
```

### ✅ Après le push

Les autres membres de l'équipe devront faire :
```bash
git pull
pip install -r requirements.txt
```

---

## 🔒 .gitignore (vérification importante)

Assure-toi que ton fichier `.gitignore` contient **au minimum** :
```gitignore
# Environnement virtuel
.venv/
venv/
env/

# Python
__pycache__/
*.pyc
*.pyo
*.pyd

# macOS
.DS_Store

# IDE
.vscode/
.idea/
```

**⚠️ Ne jamais commit le dossier `.venv/`** — chaque développeur doit créer le sien localement.

---

## 🛠️ Dépannage

### Le venv n'est pas activé

**Symptôme** : `pip install` installe les packages globalement ou `import` ne fonctionne pas.

**Solution** :
```bash
source .venv/bin/activate
```

**Vérification** :
```bash
which python
# Doit afficher : /chemin/vers/Rockstar-Bros/.venv/bin/python

python3 -m pip --version
# Doit montrer le pip du venv
```

### Les imports ne fonctionnent pas
```bash
# Vérifier que tu es dans le bon environnement
source .venv/bin/activate

# Réinstaller les dépendances
pip install -r requirements.txt

# Tester l'import
python3 -c "import pygame"
```

### Réinitialiser complètement l'environnement

Si quelque chose ne fonctionne pas :
```bash
# Désactiver le venv
deactivate

# Supprimer l'ancien venv
rm -rf .venv

# Recréer tout
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📋 Récapitulatif des commandes essentielles

| Action | Commande |
|--------|----------|
| Activer le venv | `source .venv/bin/activate` |
| Désactiver le venv | `deactivate` |
| Installer les dépendances | `pip install -r requirements.txt` |
| Ajouter une librairie | `pip install <lib>` puis `pip freeze > requirements.txt` |
| Lancer le jeu | `python main.py` |
| Mettre à jour le projet | `git pull` puis `pip install -r requirements.txt` |

---

## 🎮 C'est parti !

Tu es maintenant prêt à coder sur Rockstar-Bros. N'oublie pas :

1. ✅ Toujours activer le venv avant de travailler
2. ✅ Faire `git pull` et `pip install -r requirements.txt` régulièrement
3. ✅ Suivre la procédure complète quand tu ajoutes une librairie

Bon développement ! 🚀