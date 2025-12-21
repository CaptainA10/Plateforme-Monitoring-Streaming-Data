# [ROADMAP.md] Feuille de Route du Projet

Cette feuille de route découpe le projet en 8 modules logiques pour une implémentation progressive et robuste.

## Module 1 : Socle Infrastructure & DevOps
*   **Objectif** : Mettre en place l'environnement de développement et les pipelines CI/CD.
*   **Livrables** :
    *   Structure Git du projet.
    *   `docker-compose.yml` de base (Kafka, Zookeeper, Spark Master/Worker).
    *   Pipeline GitHub Actions (Linter, Tests unitaires).
    *   Configuration des secrets (fichier `.env` template).

## Module 2 : Ingestion & Contrats de Données
*   **Objectif** : Ingérer les données sources avec validation de schéma stricte.
*   **Livrables** :
    *   Déploiement du Schema Registry (Apicurio ou Confluent).
    *   Définition des schémas Avro (Events).
    *   Développement de Producteurs Python (Mock Data Generators) respectant les contrats.
    *   Tests de compatibilité de schéma dans la CI.

## Module 3 : Stockage & Data Lake
*   **Objectif** : Préparer les destinations de stockage (Raw & Analytics).
*   **Livrables** :
    *   Configuration MongoDB (Stockage Raw/Logs).
    *   Configuration Google BigQuery (Datasets, Tables partitionnées).
    *   Gestion des connecteurs (Kafka Connect ou écriture directe).

## Module 4 : Traitement Streaming (Core)
*   **Objectif** : Implémenter le cœur du traitement temps réel avec PySpark.
*   **Livrables** :
    *   Jobs PySpark Streaming de base (Read Kafka -> Console).
    *   Désérialisation Avro dans Spark.
    *   Transformations stateless (Filtrage, Mapping).

## Module 5 : Gestion d'État & Fiabilité
*   **Objectif** : Gérer les agrégations complexes et la tolérance aux pannes.
*   **Livrables** :
    *   Agrégations fenêtrées (Windowing) avec Watermarking.
    *   Gestion du State Store (HDFS/S3/Local).
    *   Checkpointing et Reprise sur erreur.
    *   Gestion des "Late Data".

## Module 6 : Transformation & Qualité (dbt)
*   **Objectif** : Modéliser les données dans l'entrepôt et assurer la qualité.
*   **Livrables** :
    *   Projet dbt connecté à BigQuery.
    *   Modèles Silver/Gold (Nettoyage, Agrégation métier).
    *   Tests de qualité de données (dbt test).
    *   Documentation générée (dbt docs).

## Module 7 : Orchestration (Airflow)
*   **Objectif** : Ordonnancer les tâches batch et surveiller les streams.
*   **Livrables** :
    *   Installation d'Airflow (via Docker).
    *   DAGs pour lancer/relancer les jobs Spark Streaming.
    *   DAGs pour lancer les transformations dbt.
    *   Alerting en cas d'échec.

## Module 8 : Visualisation & Observabilité
*   **Objectif** : Restituer la valeur métier et monitorer la plateforme.
*   **Livrables** :
    *   Dashboards QlikSense connectés à BigQuery.
    *   Monitoring technique (Lag Kafka, Latence Spark).
    *   Dashboard de Data Observability (Fraîcheur, Volume).
    *   Optimisation FinOps (Analyse des coûts BigQuery).
