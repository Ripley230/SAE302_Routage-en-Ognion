# 📚 Documentation Technique - Routage en Oignon

> **Description détaillée de l'architecture, des protocoles et des algorithmes implémentés.**

---

## 📖 Sommaire
1. [Architecture du Système](#-architecture-du-système)
2. [Modules Techniques](#-modules-techniques)
3. [Protocole de Communication](#-protocole-de-communication)
4. [Algorithme de Routage en Oignon](#-algorithme-de-routage-en-oignon)
5. [Analyse de l'Algorithme (Forces & Faiblesses)](#-analyse-de-lalgorithme-forces--faiblesses)
6. [Améliorations Possibles](#-améliorations-possibles)

---

## 🏗️ Architecture du Système

Le système repose sur une architecture distribuée composée de trois types de nœuds :

### 1. Annuaire (Master)
- **Fichier** : `directory.py`
- **Rôle** : Serveur central qui maintient la liste des routeurs actifs.
- **Fonctionnement** : Écoute sur le port 9000, enregistre les routeurs et fournit la liste aux clients.
- **Base de données** : Utilise MariaDB pour la persistance des nœuds.

### 2. Routeur Oignon
- **Fichier** : `router.py`
- **Rôle** : Nœud intermédiaire de relais.
- **Fonctionnement** : Génère une paire de clefs RSA, s'enregistre à l'annuaire, et traite les paquets entrants en déchiffrant une couche.

### 3. Client
- **Fichier** : `client.py`
- **Rôle** : Interface utilisateur pour l'envoi et la réception.
- **Fonctionnement** : Récupère la liste des routeurs, construit l'oignon de chiffrement et initie la communication.

---

## 🛠️ Modules Techniques

### `crypto.py`
Module central gérant toute la logique cryptographique sans bibliothèques externes interdites.

- **`generer_clefs()`** : Génère des clefs RSA (e, n) et (d, n) en utilisant `sympy` pour la recherche de nombres premiers.
- **`chiffrer(message, clef_publique)`** : Implémente un **chiffrement hybride**. Une clef secrète est générée, chiffrée par RSA, et le message est chiffré par XOR avec cette clef.
- **`dechiffrer(message_chiffre, clef_privee)`** : Opération inverse pour retrouver le message clair.

### `db.py`
Gère l'interaction avec la base de données MariaDB.
- Stockage des IPs, ports et clefs publiques des routeurs.
- Nettoyage automatique des doublons lors de la réinscription.

---

## 📡 Protocole de Communication

Le protocole utilise des chaînes de caractères avec des séparateurs personnalisés (pas de JSON).

| Action | Format du Message |
| :--- | :--- |
| **Inscription** | `INSCRIPTION|IP|PORT|E|N` |
| **Demande Liste** | `LISTE` |
| **Réponse Liste** | `IP1;PORT1;E1;N1|IP2;PORT2;E2;N2|...` |
| **Relais Paquet** | `IP_SUIVANTE|PORT_SUIVANT|PAYLOAD_CHIFFRE` |

---

## 🧅 Algorithme de Routage en Oignon

### 1. Construction de l'Oignon (Côté Client)
Le client construit le message de l'intérieur vers l'extérieur :
1. Il définit la destination finale : `IP_DEST|PORT_DEST|MESSAGE_CLAIR`.
2. Pour chaque routeur du chemin (en partant du dernier) :
   - Il chiffre le bloc actuel avec la clef publique du routeur.
   - Il encapsule le résultat avec l'adresse du routeur suivant.

### 2. Traitement par un Routeur
1. Réception du paquet.
2. Déchiffrement avec la clef privée.
3. Extraction de l'IP/Port du prochain saut.
4. Transmission du reste du message (toujours chiffré pour les nœuds suivants).

---

## 🛡️ Analyse de l'Algorithme (Forces & Faiblesses)

### Forces
- **Anonymat** : Aucun nœud (sauf le premier) ne connaît l'expéditeur. Aucun nœud (sauf le dernier) ne connaît le destinataire.
- **Chiffrement en couches** : Le message est protégé par plusieurs couches de chiffrement indépendantes.
- **Indépendance** : Pas de dépendance à des bibliothèques de haut niveau (cryptography, json).

### Faiblesses
- **Taille des clefs** : RSA avec des nombres premiers de 1024 bits est cassable par des puissances de calcul modernes.
- **Chiffrement XOR** : Bien que rapide, le XOR simple est vulnérable à l'analyse de fréquence si la clef est trop courte ou réutilisée.
- **Point de défaillance** : L'annuaire central est un "Single Point of Failure".

---

## 🚀 Améliorations Possibles
1. **Sécurité** : Implémenter AES pour le chiffrement symétrique au lieu du XOR.
2. **Fiabilité** : Ajouter un système de "Heartbeat" pour détecter les routeurs hors-ligne.
3. **Anonymat** : Utiliser une DHT (Table de hachage distribuée) pour supprimer l'annuaire central.
