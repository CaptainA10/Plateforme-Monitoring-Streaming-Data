# Rapport d'Industrialisation

Ce document détaille les étapes nécessaires pour passer ce projet du stade de **POC (Proof of Concept)** à la **Production**.

## 1. Sécurité (Security)

### État Actuel
*   Authentification : Aucune sur Kafka/Zookeeper. Basic Auth sur Airflow/Mongo.
*   Réseau : Tout est ouvert en local.
*   Secrets : Stockés en clair ou variables d'env simples.

### Cible Production
*   **Kafka** : Activer **SASL/SCRAM** ou **mTLS** pour l'authentification des clients.
*   **Chiffrement** : Activer le chiffrement SSL/TLS pour les échanges (In-Transit) et le stockage (At-Rest).
*   **IAM** : Utiliser des Service Accounts (GCP IAM / AWS IAM) pour l'accès à BigQuery/S3, au lieu de clés JSON statiques.
*   **Secrets** : Utiliser un Vault (HashiCorp Vault, AWS Secrets Manager) injecté au runtime.

## 2. Observabilité (Observability)

### État Actuel

### Cible Production
*   **Orchestrateur** : Migrer vers **Kubernetes (K8s)**.
    *   Utiliser **Helm Charts** pour déployer Kafka (Strimzi Operator) et Airflow.
    *   Utiliser **Spark on K8s** pour lancer les drivers/executors dynamiquement.
*   **IaC** : Définir toute l'infrastructure (GCP/AWS) avec **Terraform**.
*   **CI/CD** : Pipeline complet (GitHub Actions / GitLab CI) :
    1.  Lint & Test Unitaires.
    2.  Build Docker Images & Push to Registry.
    3.  Deploy to Staging (Helm Upgrade).
    4.  Tests d'Intégration (TestContainers).
    5.  Deploy to Prod.

## 4. FinOps & Scalabilité

### État Actuel
*   Ressources : Limitées à la machine locale.

### Cible Production
*   **Auto-scaling** : Configurer l'Horizontal Pod Autoscaler (HPA) sur K8s pour les consommateurs Spark en fonction du Lag Kafka.
*   **Stockage** : Configurer des Lifecycle Policies sur S3/GCS pour archiver les vieilles données (Cold Storage) et réduire les coûts.
*   **BigQuery** : Surveiller les coûts des requêtes. Utiliser le partitionnement et le clustering (déjà défini dans nos DDL) pour optimiser.

## 5. Visualisation (BI)

### État Actuel
*   Streamlit (Code-First).

### Cible Production
*   Connecter un outil Enterprise (**QlikSense**, **Tableau**) directement sur le Data Warehouse (BigQuery).
*   Utiliser Streamlit uniquement pour des apps de Data Science ou de monitoring technique spécifique.
