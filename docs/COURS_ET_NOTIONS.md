# [COURS_ET_NOTIONS.md] Architecture & Data Contracts

## 1. Architecture Lambda vs Architecture Kappa

Dans le monde du Big Data et du Streaming, deux modèles d'architecture prédominent : **Lambda** et **Kappa**. Comprendre leurs différences est crucial pour justifier nos choix technologiques.

### 1.1. Architecture Lambda (L'approche "Ceinture et Bretelles")
Historiquement (années 2010), les systèmes de streaming (Storm, early Spark Streaming) n'étaient pas assez fiables ou précis (gestion du "exactly-once" difficile) pour être l'unique source de vérité.

*   **Concept** : On divise le système en trois couches (layers) :
    1.  **Batch Layer (Master Dataset)** : Stocke toutes les données brutes (HDFS/S3) et recalcule les vues complètes périodiquement (ex: toutes les nuits). C'est la source de vérité, lente mais fiable.
    2.  **Speed Layer** : Traite les données en temps réel pour compenser la latence du Batch Layer. Ses résultats sont approximatifs ou temporaires.
    3.  **Serving Layer** : Fusionne les résultats du Batch et du Speed pour la requête utilisateur.
*   **Inconvénients** : Complexité opérationnelle majeure. Il faut maintenir deux bases de code (une pour le batch, une pour le stream) qui font souvent la même chose (ex: compter des clics). "Viola le principe DRY (Don't Repeat Yourself)".

### 1.2. Architecture Kappa (L'approche "Stream First")
Avec la maturation de Kafka (rétention longue durée) et des moteurs de streaming (Flink, Spark Structured Streaming), le streaming est devenu fiable et capable de garantir le "exactly-once".

*   **Concept** : **Tout est un flux**. On supprime la Batch Layer.
    *   Le traitement temps réel est l'unique chemin de transformation.
    *   Si on veut recalculer l'historique (ex: changement de règle métier), on "rejoue" (Replay) les données depuis Kafka (qui agit comme buffer persistant) ou depuis un Data Lake, à travers le **même moteur de streaming**.
*   **Avantages** :
    *   **Simplicité** : Une seule base de code à maintenir.
    *   **Cohérence** : Pas de divergence de logique entre batch et stream.
*   **Pourquoi pour ce projet ?** : Nous visons une plateforme "Monitoring & Streaming". La fraîcheur de la donnée est critique. PySpark Streaming nous permet de gérer l'état et le watermarking efficacement. Nous adopterons une approche **Kappa** pour simplifier l'industrialisation.

---

## 2. Contrats de Données & Schema Registry

Dans un système distribué découplé (comme Kafka), les Producteurs et les Consommateurs ne se connaissent pas. Cela crée un risque majeur : le **Data Drift** structurel.

### 2.1. Le Problème
Imaginez un Producteur qui envoie un événement JSON : `{"id": 123, "price": 10.5}`.
Le Consommateur s'attend à ce format.
Demain, le Producteur change le format : `{"id": "123", "cost": 10.5}` (renommage de champ, changement de type).
**Résultat** : Le Consommateur crashe ou ingère des données corrompues (NULLs). C'est la cause #1 des incidents Data en production.

### 2.2. La Solution : Schema Registry
Le Schema Registry est un composant central (serveur) qui stocke les versions des schémas (Avro, Protobuf, JSON Schema).

*   **Fonctionnement** :
    1.  **Au build/deploy** : Le Producteur enregistre son schéma dans le Registry.
    2.  **Au runtime (Produce)** : Avant d'envoyer un message, le Producteur vérifie (ou sérialise) avec l'ID du schéma. Kafka ne reçoit que les données binaires + l'ID du schéma.
    3.  **Au runtime (Consume)** : Le Consommateur lit l'ID, récupère le schéma depuis le Registry, et désérialise.

### 2.3. Règles d'Évolution (Compatibility Modes)
Le Registry force le respect de règles strictes lors de la mise à jour d'un schéma :
*   **Backward Compatibility** : Le nouveau schéma peut lire les anciennes données. (Essentiel pour le Replay).
    *   *Règle* : On ne peut que *ajouter* des champs optionnels ou *supprimer* des champs obligatoires.
*   **Forward Compatibility** : L'ancien schéma peut lire les nouvelles données.
*   **Full Compatibility** : Les deux.

### 2.4. Bonnes Pratiques Industrielles
*   **Contrats Avro** : Préférez Avro pour le Big Data (compact, binaire, support natif Spark/Kafka).
*   **CI/CD Gate** : Interdire le déploiement d'un Producteur si son schéma casse la compatibilité (via `mvn schema-registry:test-compatibility` ou équivalent).
*   **Ownership** : Le schéma appartient au Producteur (Domain Owner), mais doit être validé par la Data Platform.

---

## 3. Avro & Producers (Deep Dive)

### 3.1. Pourquoi Avro ?
Apache Avro est un format de sérialisation de données orienté ligne (row-oriented), très populaire dans l'écosystème Hadoop/Spark/Kafka.
*   **Schéma JSON** : Le schéma est défini en JSON, lisible par l'humain.
*   **Binaire Compact** : Les données sont sérialisées en binaire. Contrairement au JSON, on ne répète pas les noms de champs à chaque message ("id": 1, "id": 2...). On gagne 30-50% de volume réseau/stockage.
*   **Évolution de Schéma** : Avro gère nativement les valeurs par défaut, facilitant l'évolution (ajout de colonnes).

### 3.2. Structure d'un Schéma Avro
Un schéma Avro typique contient :
*   `type`: "record" (objet).
*   `name`: Nom de l'événement.
*   `fields`: Liste des champs avec leur type (`string`, `int`, `long`, `boolean`, `float`, `double`, `bytes`).
*   **Types complexes** : `enum` (liste finie), `array` (liste), `map` (clé-valeur), `union` (ex: `["null", "string"]` pour un champ optionnel).

### 3.3. Pattern Producer Robuste
Écrire un Producer Kafka de qualité production demande de gérer plusieurs aspects :
1.  **Asynchronisme** : `producer.produce()` est asynchrone. Il ne bloque pas. Il ajoute le message dans un buffer local.
2.  **Callbacks** : Pour savoir si le message a bien été reçu par le Broker, on utilise une fonction de callback (`on_delivery`). C'est là qu'on loggue les erreurs.
3.  **Flush** : Il faut appeler `producer.flush()` avant d'arrêter le programme pour vider le buffer local.
4.  **Sérialisation** : Utiliser `AvroSerializer` de `confluent-kafka` pour transformer l'objet Python (Dict) en octets Avro, en validant automatiquement le schéma.

---

## 4. Stockage : Data Lake vs Data Warehouse

### 4.1. Data Lake (Le "Fourre-tout" Organisé)
*   **Objectif** : Stocker TOUTES les données, brutes, sans perte d'information. C'est la "Bronze Layer".
*   **Technologie** : Object Storage (S3, GCS) ou NoSQL (MongoDB, Cassandra).
*   **Schema** : "Schema-on-Read". On ne valide pas la structure à l'écriture. On stocke le JSON/Avro tel quel.
*   **Usage** : Data Science, Replay (Architecture Kappa), Audit.

### 4.2. Data Warehouse (L'Entrepôt Structuré)
*   **Objectif** : Stocker des données nettoyées, structurées et optimisées pour l'analyse SQL. C'est la "Silver/Gold Layer".
*   **Technologie** : Bases colonnaires (BigQuery, Snowflake, Redshift).
*   **Schema** : "Schema-on-Write". La donnée doit correspondre à la table SQL.
*   **Usage** : BI, Dashboards, Reporting.

### 4.3. Notre Stratégie
1.  **MongoDB (Raw)** : Nous utilisons Mongo comme Data Lake temporaire/chaud. Chaque événement Kafka est inséré tel quel.
2.  **BigQuery (Analytics)** : Nous utilisons BigQuery pour les requêtes analytiques. Les données y seront chargées (via dbt ou Spark) dans un format structuré.

### 4.4. Pourquoi BigQuery est rapide ? (Stockage Colonnaire)
Contrairement à une base classique (Postgres) qui stocke ligne par ligne, BigQuery stocke colonne par colonne.
*   Si je fais `SELECT AVG(price) FROM sales`, BigQuery ne lit QUE la colonne `price`. Il ignore les 50 autres colonnes.
*   **Partitionnement** : On découpe la table par jour (`partition by DATE(timestamp)`). Une requête sur "hier" ne scannera pas les données de "l'année dernière".

---

## 5. Streaming Processing (PySpark)

### 5.1. Structured Streaming
Spark Structured Streaming traite les flux de données comme des **tables infinies** (Unbounded Tables).
*   Chaque nouvel événement est une ligne ajoutée à la table.
*   On utilise la même API que pour le Batch (DataFrames).

### 5.2. Le Problème du "Late Data" & Watermarking
En streaming, les données n'arrivent jamais dans l'ordre parfait (problèmes réseau, horloges désynchronisées).
*   **Event Time** : L'heure à laquelle l'événement s'est produit (dans le payload).
*   **Processing Time** : L'heure à laquelle le serveur reçoit l'événement.
*   **Watermark** : C'est le seuil de tolérance au retard. "J'accepte les données vieilles de 10 minutes maximum".
    *   Si `Watermark = 10 min` et qu'il est 12h00, Spark maintient l'état des agrégations jusqu'à 11h50. Tout événement plus vieux est ignoré. Cela permet de libérer la mémoire (State Store).

### 5.3. Windowing (Fenêtrage)
Pour faire des agrégations (ex: "Nombre de clics par minute"), on découpe le temps en fenêtres.
*   **Tumbling Window** : Fenêtres fixes, non chevauchantes. (ex: [12:00-12:05], [12:05-12:10]).
*   **Sliding Window** : Fenêtres glissantes. (ex: "Toutes les 5 minutes, donne-moi le compte des 10 dernières minutes").

---

## 6. Fiabilité & Production (Reliability)

### 6.1. Checkpointing (Le "Save Game")
En streaming, une application peut crasher à tout moment.
*   **Problème** : Si je redémarre, est-ce que je relis tout depuis le début ? Est-ce que je perds des données ?
*   **Solution** : Le Checkpointing. Spark écrit périodiquement son état (offsets Kafka lus, état des agrégations) dans un dossier fiable (HDFS, S3, ou Volume Docker).
*   **Au redémarrage** : Spark lit ce dossier et reprend *exactement* là où il s'était arrêté. C'est la clé du "Fault Tolerance".

### 6.2. Dead Letter Queue (DLQ)
Parfois, un message est corrompu ("Poison Pill"). Si le parser plante, tout le job plante.
*   **Stratégie** : Ne jamais faire crasher le job pour une erreur de donnée.
*   **Implémentation** :
    1.  `try/catch` dans le code de parsing.
    2.  Si erreur, on redirige le message vers un topic Kafka spécial `dlq_topic` ou un dossier `bad_records`.
    3.  On continue le traitement des autres messages.

### 6.3. Backfill (Reprise d'historique)
Dans une architecture Kappa, si on change la logique (ex: nouvelle formule de calcul), on peut relancer le traitement sur les données passées.
*   On lance un **nouveau job** avec un nouveau `checkpointLocation`.
*   On lui dit de lire Kafka depuis `earliest`.
*   Il va retraiter tout l'historique avec le nouveau code.

---

## 7. Orchestration (Airflow)

### 7.1. Pourquoi orchestrer ?
Même avec du streaming, on a besoin de traitements Batch périodiques :
*   **Reporting** : Générer un PDF tous les matins.
*   **Maintenance** : Compacter les petits fichiers Parquet (Small Files Problem).
*   **Réconciliation** : Vérifier que les données dans BigQuery correspondent à Kafka.

### 7.2. Concepts Airflow
Apache Airflow est la référence pour l'orchestration ("Workflow as Code").
*   **DAG (Directed Acyclic Graph)** : Le workflow (ex: "Daily Stats").
*   **Operator** : Une tâche unitaire (ex: `BashOperator`, `PythonOperator`, `SparkSubmitOperator`).
*   **Sensor** : Une tâche qui attend qu'une condition soit remplie (ex: "Attendre que le fichier soit arrivé").
*   **Schedule** : La fréquence d'exécution (ex: `@daily`, `0 0 * * *`).

### 7.3. Notre DAG "Daily Aggregation"
Nous allons créer un DAG qui :
1.  Se lance tous les jours à minuit.
2.  Lance un job Spark Batch.
3.  Ce job lit les données brutes de la veille (dans MongoDB ou Data Lake).
4.  Calcule des statistiques globales.
5.  Les sauvegarde pour le Dashboarding.

---

## 8. Visualisation (BI)

### 8.1. Le "Dernier Kilomètre" de la Data
C'est la seule partie que l'utilisateur final voit. Si le dashboard est lent ou moche, tout le travail d'ingénierie est "inutile" à ses yeux.

### 8.2. Outils du Marché
*   **Enterprise BI (QlikSense, Tableau, PowerBI)** :
    *   *Avantages* : Drag & Drop, Gouvernance, Sécurité, Self-Service pour les métiers.
    *   *Inconvénients* : Coûteux, lourd à déployer, "Boîte noire".
*   **Code-First BI (Streamlit, Dash, Shiny)** :
    *   *Avantages* : 100% Python, Versionnable (Git), Gratuit, Flexible.
    *   *Inconvénients* : Demande des compétences de dev, moins de fonctionnalités "out of the box" (export PDF, gestion des droits fine).

### 8.3. Notre Choix : Streamlit
Pour ce POC, nous utilisons **Streamlit** car :
1.  C'est du Python pur (cohérent avec notre stack).
2.  C'est léger et rapide à itérer.
3.  Ça permet de faire du **Real-Time** (polling) facilement.

### 8.4. Architecture QlikSense (Cible)
Dans une vraie prod, on connecterait QlikSense à **BigQuery**.
*   **Direct Query** : Qlik interroge BigQuery en direct (bien pour le temps réel, coûteux).
*   **Import** : Qlik charge les données en mémoire (In-Memory) toutes les heures. (Ultra rapide pour l'utilisateur).
### 8. BigQuery vs MongoDB : Lequel choisir ?

Dans notre architecture, nous utilisons les deux pour des raisons différentes :

| Caractéristique | MongoDB (Data Lake) | BigQuery (Data Warehouse) |
| :--- | :--- | :--- |
| **Type** | NoSQL (Document) | SQL (Colonnaire) |
| **Usage** | Stockage brut, rapide, flexible | Analyse complexe, BI, agrégations |
| **Schéma** | Schema-on-Read (Flexible) | Schema-on-Write (Strict) |
| **Performance** | Excellente pour les écritures unitaires | Excellente pour les scans de gros volumes |
| **Coût** | Coût serveur (RAM/CPU) | Coût au volume de données scannées |

**Pourquoi les deux ?** 
On stocke tout dans **MongoDB** (notre "Landing Zone") pour ne rien perdre, puis on envoie les données structurées vers **BigQuery** pour que les analystes puissent faire des requêtes SQL performantes sans ralentir la production.
