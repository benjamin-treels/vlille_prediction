# Projet de Prédiction du Nombre de Vélos Disponibles à une Station V'Lille

## Description du Projet

Ce projet vise à développer un modèle de prédiction capable de prévoir le nombre de vélos disponibles à une station V'Lille à une date donnée. L'objectif est de permettre aux utilisateurs de mieux planifier leurs déplacements en vélo en fournissant des prévisions précises et en temps réel.

## Étape 1 : Collecte, Nettoyage et Enrichissement des Données

### Objectif

La première étape consiste à collecter les données nécessaires à partir de différentes sources, les nettoyer, les enrichir avec des métadonnées pertinentes, et les stocker dans une base de données MongoDB. 

### Sources de Données

1. **API V'Lille** : Données sur le nombre de vélos disponibles et l'état des stations.
2. **API Météo** : Données météorologiques (température, précipitations, etc.).
3. **Données de Transport** : Informations sur les stations de métro et autres moyens de transport à proximité.

### Étapes de la Phase 1

1. **Collecte des Données** :
   - **API V'Lille** : Mettre en place un script pour interroger régulièrement l'API V'Lille et stocker les données brutes dans MongoDB.
   - **API Météo** : Configurer un script pour récupérer les données météorologiques correspondantes.
   - **Données de Transport** : Recueillir les informations sur les stations de métro et autres moyens de transport.

2. **Nettoyage des Données** :
   - Gérer les données manquantes : imputer ou supprimer les valeurs manquantes.
   - Corriger les anomalies : identifier et corriger les valeurs aberrantes.

3. **Enrichissement des Données** :
   - Ajouter des métadonnées météorologiques : pour chaque enregistrement de l'API V'Lille, ajouter les données météorologiques correspondantes (pluie, pas pluie).
   - Proximité des stations de métro : ajouter un champ indiquant si une station de métro est proche (oui, non).
   - Transformation de la date : séparer la date en plusieurs champs (jour de la semaine, heure, mois, numéro de la semaine).

4. **Stockage des Données** :
   - Insérer les documents JSON enrichis dans la collection MongoDB.