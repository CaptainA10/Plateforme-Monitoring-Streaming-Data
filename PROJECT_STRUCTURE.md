# [PROJECT_STRUCTURE.md] Structure Git Idéale

Voici la structure de dossiers recommandée pour garantir la modularité, la testabilité et la séparation des responsabilités (SoC).

```text
/
├── .github/                    # Workflows CI/CD (GitHub Actions)
│   └── workflows/
│       ├── ci-python.yml       # Linter, Unit Tests
│       └── ci-dbt.yml          # dbt test
├── config/                     # Fichiers de configuration centralisés
│   ├── airflow.cfg
│   ├── spark-defaults.conf
│   └── schemas/                # Schémas Avro/Protobuf (Source of Truth)
│       └── user_activity.avsc
├── dags/                       # DAGs Airflow
│   ├── ingestion_dag.py
│   └── transformation_dag.py
├── dbt_project/                # Projet dbt (Transformation)
│   ├── models/
│   ├── tests/
│   └── dbt_project.yml
├── docker/                     # Dockerfiles et scripts d'init
│   ├── spark/
│   ├── airflow/
│   └── init-scripts/           # Scripts de création de topics Kafka, BQ datasets
├── docs/                       # Documentation projet
│   ├── ADR/                    # Architecture Decision Records
│   ├── COURS_ET_NOTIONS.md
│   └── ROADMAP.md
├── notebooks/                  # Notebooks Jupyter pour l'exploration (Dev)
├── src/                        # Code source applicatif
│   ├── common/                 # Librairies partagées (Logging, Config loader)
│   ├── ingestion/              # Producteurs Kafka, Connectors custom
│   └── streaming/              # Jobs PySpark Streaming
│       ├── jobs/
│       └── utils/
├── tests/                      # Tests unitaires et d'intégration
│   ├── unit/
│   └── integration/
├── .env.example                # Template des variables d'environnement
├── .gitignore
├── docker-compose.yml          # Orchestration locale des conteneurs
├── Makefile                    # Commandes raccourcies (make up, make test)
├── README.md
└── requirements.txt            # Dépendances Python globales (ou par module)
```

## Justification des choix
*   **`src/` séparé** : Isole le code métier des configurations et des outils d'orchestration.
*   **`config/schemas/`** : Centralise les contrats de données. C'est le point de vérité pour le Schema Registry.
*   **`docker/`** : Permet de maintenir des images Docker custom (ex: Spark avec dépendances spécifiques) proprement.
*   **`dbt_project/`** : Isolé à la racine car c'est un sous-projet à part entière.
