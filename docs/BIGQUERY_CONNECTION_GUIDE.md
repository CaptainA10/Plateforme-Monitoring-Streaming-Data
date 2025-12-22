# 🔍 Guide de Connexion BigQuery (Simba Driver)

Ce guide détaille comment configurer une connexion à BigQuery en utilisant les paramètres fournis, typiquement pour des outils comme **QlikSense**, **Power BI**, **Tableau** ou via un driver **ODBC/JDBC**.

## 1. Authentification (Service Account)

Pour une connexion automatisée et partagée, il est recommandé d'utiliser un **Service Account**.

- **Mechanism** : `Service Account`
- **Email** : `monitoring-platform-sa@effidic-stage-2026.iam.gserviceaccount.com`
- **Key File Path** : Utilisez le fichier local `config/gcp/service-account.json`.
  > [!IMPORTANT]
  > Assurez-vous que le chemin vers le fichier JSON est accessible par l'application qui tente de se connecter.

## 2. Propriétés de la Base de Données

- **Catalog (Project)** : `effidic-stage-2026`
- **Dataset** : `monitoring_datalake`
- **Minimum TLS** : `1.2` (Recommandé pour la sécurité)

## 3. Options Avancées (Simba Driver)

Voici les valeurs optimales basées sur votre demande pour maximiser les performances :

| Paramètre | Valeur | Description |
| :--- | :--- | :--- |
| **Rows Per Block** | `16384` | Nombre de lignes par bloc de données. |
| **Default String Column Length** | `65535` | Taille par défaut pour les colonnes de type String. |
| **Query Timeout** | `30` | Temps d'attente max pour une requête (secondes). |
| **Retry Timeout** | `300` | Temps d'attente max pour les tentatives (secondes). |
| **Max String Length** | `4096` | Optimisation du chargement pour les chaînes longues. |

### High-Throughput API (HTAPI)
Si vous manipulez de gros volumes de données, activez ces options :
- **Min Query Results Size for HTAPI** : `1000`
- **Ratio of Results to Rows Per Block** : `3`

## 4. Résumé de la Configuration

| Champ | Valeur |
| :--- | :--- |
| **Name** | `Google_BigQuery` |
| **Dialect** | `Google BigQuery` |
| **Language Dialect** | `Standard SQL` |

---
🚀 **Note** : Si vous rencontrez une erreur `403 Forbidden`, vérifiez que l'API BigQuery est activée sur le projet `effidic-stage-2026` et que la facturation est configurée.
