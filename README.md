# Backend IGL

## Prérequis

Avant de lancer ce projet backend, assurez-vous de remplir les prérequis suivants :

- **Python** : Version 3.8 ou supérieure installée. [Télécharger Python](https://www.python.org/downloads/)
- **MySQL** : Version 5.7 ou supérieure installée. [Télécharger MySQL](https://dev.mysql.com/downloads/)
- **Pip** : Installé avec Python.
- **Environnement virtuel (recommandé)** : Créez un environnement virtuel pour isoler les dépendances.

## Installation et Configuration

Suivez les étapes ci-dessous pour configurer et exécuter le projet backend :

### 1. Cloner le repo

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Installer les dépendances

Créez et activez un environnement virtuel (recommandé) :

```bash
python -m venv venv
source venv/bin/activate  # Sous Windows : `venv\Scripts\activate`
```

Installez les dépendances nécessaires :

```bash
pip install -r requirements.txt
```

### 3.Configuration de MySQL

Assurez-vous que MySQL est installé et en cours d'exécution sur votre machine. Vous aurez besoin des informations suivantes pour configurer la base de données :

- Nom de la base de données
- Utilisateur
- Mot de passe
- Hôte
- Port

### 4.Créer le fichier .env

Créez un fichier .env à la racine du projet et ajoutez-y le contenu suivant en remplaçant les valeurs par vos informations réelles :

```
DATABASE_NAME="IGL_db"
DATABASE_USER="root"
DATABASE_PASSWORD="root"
DATABASE_HOST="0.0.0.0"
DATABASE_PORT=3306
CLOUD_NAME="doxcskw0g"
API_KEY="75573411298282"
API_SECRET="R4MVoxcGx_aNXZXrb_Iogwq6Y"
DEFAULT_FROM_EMAIL="votreemail@example.com"
EMAIL_PORT=587
EMAIL_HOST_USER="votreemail@example.com"
EMAIL_HOST_PASSWORD="générez_une_clé_depuis_votre_fournisseur_d'email"
```

---

> **_NOTE:_** Utilisez un mot de passe fort et sécurisé pour vos identifiants d'email et de base de données. Le `EMAIL_HOST_PASSWORD `doit être généré depuis votre fournisseur d'email (par exemple, Google App Passwords).

---

### 5.Appliquer les migrations de la base de données

Exécutez les commandes suivantes pour appliquer les migrations de la base de données :

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Démarrer le serveur de développement

Lancez le serveur avec :

```bash
python manage.py runserver
```

Le serveur sera accessible localement à l'adresse `http://127.0.0.1:8000`

## Exécution des Tests

Vous pouvez exécuter les scripts de test pour des applications spécifiques comme suit :

### 1. Tests pour l'application `utilisateur`

Exécutez la commande suivante :

```bash
cd utilisateur/
python tests_utilisateurs.py
```

### 1. Tests pour l'application `dpi`

Exécutez la commande suivante :

```bash
cd dpi/
python tests_dpi.py
```

## Notes Supplémentaires

- Assurez-vous que votre fichier `.env` est correctement configuré avant de lancer le projet.
- Utilisez un environnement virtuel pour éviter les conflits de dépendances.
- Utilisez des mots de passe forts et sécurisés pour vos paramètres d'email et de base de données.
