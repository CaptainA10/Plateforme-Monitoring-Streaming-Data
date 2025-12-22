# 📂 Sources et Signification des Données

Ce document explique d'où proviennent les données de la plateforme et ce qu'elles représentent concrètement.

## 1. Activité Utilisateur (Simulée)
**Source** : `src/ingestion/main.py` (via `UserActivityProducer`)

### Qu'est-ce que c'est ?
Ce sont des données générées artificiellement pour simuler le comportement d'utilisateurs sur un site web ou une application mobile.

### Que représentent-elles ?
Chaque événement représente une action précise :
- **CLICK** : L'utilisateur a cliqué sur un élément.
- **VIEW** : L'utilisateur a consulté une page.
- **PURCHASE** : L'utilisateur a effectué un achat.
- **LOGIN/LOGOUT** : Connexion ou déconnexion.

**Champs clés** :
- `user_id` : Identifiant unique de l'utilisateur fictif.
- `event_type` : Le type d'action (voir ci-dessus).
- `timestamp` : Date et heure précises de l'action.
- `page_id` : La page concernée par l'action.

---

## 2. Flux Wikimedia (Temps Réel)
**Source** : `src/ingestion/wikimedia_producer.py` (via l'API EventStreams de Wikimedia)

### Qu'est-ce que c'est ?
Ce sont des données **réelles** provenant directement des serveurs de la fondation Wikimedia (Wikipedia, Wikidata, etc.).

### Que représentent-elles ?
Chaque événement représente une **modification en temps réel** effectuée sur un projet Wikimedia.
- **Modifications de pages** : Un utilisateur a ajouté ou supprimé du contenu.
- **Créations de pages** : Un nouvel article a été publié.
- **Actions de bots** : Modifications automatiques effectuées par des scripts.

**Champs clés** :
- `user` : Nom de l'utilisateur (ou IP) ayant fait la modification.
- `title` : Titre de la page modifiée (ex: "Paris", "Intelligence Artificielle").
- `wiki` : Le projet concerné (ex: `frwiki` pour Wikipédia en français).
- `bot` : Indique si la modification a été faite par un robot (`true`) ou un humain (`false`).

---

## 3. Pourquoi ces deux sources ?
- **L'activité utilisateur** permet de tester la plateforme avec des données structurées et prévisibles (idéal pour le monitoring métier).
- **Le flux Wikimedia** permet de tester la montée en charge (scalability) avec un flux de données réel, massif et continu (idéal pour le monitoring technique).

---
🚀 **Ces données alimentent vos dashboards pour vous donner une vision complète de la santé de votre système.**
