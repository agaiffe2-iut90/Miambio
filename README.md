# Miambio

Ce projet est une application web simple de gestion de base de données pour une entreprise fictive nommée *Miambio* rélaisée avec Flask et une base données MySQL dans un groupe de 4 étudiants.

## Sommaire

1. [Installation](#installation)
2. [Utilisation](#utilisation)
3. [Auteurs](#auteurs)
4. [Statut du projet](#statut-du-projet)

## Installation

1. Récupérer le projet
```bash
git clone https://github.com/agaiffe2-iut90/Miambio
cd Miambio
```

2. Configurer la base de donnée
    - Exécuter le fichier [sql_miambio.sql](sql_miambio.sql) dans une base de données MySQL
    - Changer les informations de connexion à la base de données dans le fichier [app.py](projet_flask/app.py)

3. Activer l'environnement virtuel
```bash
cd flask_app
source venv/bin/activate
```

4. Lancer l'application
```
/bin/bash launcher.sh
```

## Utilisation

Une fois lancé, le site permet de consulter, ajouter, modifier et supprimer des enregistrements concernant l'activité de *Miambio* dans la base données.

## Auteurs

- [Anna GAIFFE](https://github.com/agaiffe2-iut90)
- [Nathan PONTHIEU](https://github.com/nponthie-iut90)
- [Simone-désirée ZIGGAR](https://github.com/sdziggar-iut90)
- [Mickaël MARCO](https://github.com/mmarco-iut90)

## Statut du projet

Le projet est terminé, il a eu lieu de octobre à novembre 2023.
