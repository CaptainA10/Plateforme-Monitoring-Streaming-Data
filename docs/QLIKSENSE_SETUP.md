# 📊 Guide de Connexion QlikSense à BigQuery

Ce guide explique comment connecter **QlikSense** à votre Data Warehouse **BigQuery** pour visualiser les données du projet.

## 1. Prérequis
*   Un compte **QlikSense** (SaaS ou Desktop).
*   Le fichier de clé du Service Account : `config/gcp/service-account.json`.
*   L'ID du projet GCP : `effidic-stage-2026`.

## 2. Étapes de Connexion

### A. Créer une nouvelle connexion dans Qlik
1.  Dans votre application Qlik, allez dans **Data Load Editor** ou **Data Manager**.
2.  Cliquez sur **Create new connection**.
3.  Recherchez et sélectionnez le connecteur **Google BigQuery**.

### B. Configuration de l'authentification
1.  **Authentication Method** : Choisissez `Service Account`.
2.  **Service Account Email** : Utilisez l'email présent dans votre fichier JSON (`monitoring-platform-sa@...`).
3.  **Key File** : Téléchargez ou copiez le contenu de votre fichier `service-account.json`.
4.  **Project ID** : Saisissez `effidic-stage-2026`.

### C. Sélection des données
1.  Une fois connecté, sélectionnez le dataset `monitoring_datalake`.
2.  Vous verrez les tables suivantes :
    *   `user_activity` : Données brutes.
    *   `stg_user_activity` : Données nettoyées (Vue dbt).
    *   `fct_daily_user_metrics` : Agrégations quotidiennes (Table dbt). **C'est cette table qu'il faut utiliser pour vos graphiques !**

## 3. Exemple de Visualisation
*   **KPI** : Nombre total d'événements (`SUM(event_count)`).
*   **Graphique en barres** : `activity_date` en dimension et `SUM(unique_users)` en mesure.
*   **Filtre** : Par `event_type` (CLICK, VIEW, etc.).

---
🚀 **Votre dashboard est maintenant connecté à une stack Data moderne !**
