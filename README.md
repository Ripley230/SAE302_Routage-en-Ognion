Projet SAE 3.02 : Routage en Oignon (Onion Routing)

Conception d’une architecture distribuée avec routage en oignon pour l'anonymisation des flux.

Présentation
Ce projet implémente un système de **routage en oignon** (inspiré du réseau Tor) permettant d'anonymiser les communications réseau. L'idée est de faire transiter un message à travers plusieurs nœuds intermédiaires (routeurs), où chaque nœud ne connaît que son prédécesseur et son successeur immédiat.

Fonctionnalités
- Annuaire (Master) : Serveur central gérant l'enregistrement des routeurs et la distribution de la liste aux clients.
- Routeurs Oignon : Nœuds de relais effectuant le déchiffrement d'une couche et la transmission au saut suivant.
- Client Multi-Rôles : Interface permettant d'envoyer des messages chiffrés et d'en recevoir.
- Chiffrement Hybride : Utilisation de **RSA** pour l'échange de clefs et **XOR** pour le payload (implémentation maison sans librairie crypto).
- Routage Dynamique : Choix du nombre de sauts (1 à 10) par le client.
- Interface Graphique : Interfaces modernes développées avec **PyQt5**.
- Persistance : Utilisation de **MariaDB** pour stocker l'état du réseau.

Guide d'Utilisation

1. **Démarrer l'Annuaire** : `python3 directory_node.py` -> Cliquez sur "Lancer le serveur".
2. **Démarrer les Routeurs** : Lancez 3 instances de `onion_router.py` -> Cliquez sur "Démarrer".
3. **Lancer les Clients** : `python3 client.py` (ouvrez-en deux pour tester la communication).

> [!IMPORTANT]
> Consultez le [GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md) pour les détails sur la configuration réseau entre plusieurs VMs.

## 📂 Structure du Projet
- 🛠️ `crypto_utils.py` : Cœur cryptographique (RSA, XOR, Nombres premiers).
- 🗄️ `db_utils.py` : Interface avec la base de données MariaDB.
- 📋 `directory_node.py` : Serveur d'annuaire avec interface graphique.
- 🔄 `onion_router.py` : Nœud de routage intermédiaire.
- 👤 `client.py` : Application utilisateur (Envoi/Réception).
- 📜 `install_dependencies.py` : Script d'automatisation de l'installation.

---

Contraintes du Sujet
- Bibliothèques Interdites : `json`, `cryptography` (Respecté : protocole texte et RSA maison).
- Bibliothèques Imposées : `Socket`, `Thread`, `PyQt5`, `MariaDB` (Utilisées).
- Algorithme : Chiffrement asymétrique RSA implémenté de zéro.

Auteurs
Groupe : Les pingouins
- Quentin HARTRMANN
- Akaza KOUAME


Projet réalisé dans le cadre de la SAE 3.02 - Réseaux & Télécoms (2025).



