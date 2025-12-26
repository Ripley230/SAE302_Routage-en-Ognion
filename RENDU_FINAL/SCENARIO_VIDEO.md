# Scénario de Démonstration Vidéo - Projet Onion Routing

Ce document décrit étape par étape comment réaliser la vidéo de démonstration (durée conseillée : 5-10 minutes).

---

## 0. ARCHITECTURE VM : CHOIX TECHNIQUES

**Question : 1 VM par routeur ou une seule VM ?**
- **Option Idéale (5 VMs) :** 1 Annuaire, 3 Routeurs, 1 Client. C'est la plus réaliste.
- **Option Optimisée (3 VMs) :** 1 Annuaire, 1 VM "Réseau" (lançant les 3 routeurs), 1 Client.
- **Option Légère (1 VM) :** Tout sur la même machine. 

> [!TIP]
> Pour la vidéo, l'**Option Optimisée (3 VMs)** est un excellent compromis. Elle montre bien la séparation des rôles sans surcharger votre ordinateur.

---

## 1. PRÉPARATION (Hors caméra)

1.  **Installer les dépendances** sur chaque VM (voir `GUIDE_INSTALLATION.md`).
2.  **Copier les fichiers** : Assurez-vous que chaque VM a le dossier `RENDU_FINAL`.
3.  **Configurer l'IP de l'Annuaire** : Dans `onion_router.py` et `client.py`, vérifiez que `IP_ANNUAIRE` pointe vers l'IP de votre VM Annuaire (ex: `10.0.2.10`).

---

## 2. DÉROULEMENT DE LA VIDÉO

### Introduction (0:00 - 1:00)
- Montrez l'arborescence du projet.
- Expliquez brièvement le rôle de chaque fichier :
  - `directory.py` : Le serveur annuaire.
  - `router.py` : Le nœud de routage.
  - `client.py` : L'application utilisateur.
  - `crypto.py` : Les outils de chiffrement.
  - `db.py` : La gestion de la base de données.
- **Commentaire :** "Nous allons présenter notre implémentation d'un routage en oignon distribué."

### Séquence 1 : Lancement de l'Infrastructure (1:00 - 2:30)
1.  **VM Annuaire** : Lancez `directory_node.py` et cliquez sur "Lancer le serveur".
2.  **VM Routeurs** : Lancez 3 instances de `onion_router.py`. Cliquez sur "Démarrer" pour chacun.
3.  **Montrez l'Annuaire** : On voit les 3 routeurs s'inscrire en temps réel avec leurs clefs publiques RSA.

### Séquence 2 : Démonstration de l'Anonymisation (2:30 - 5:00)
1.  **VM Client** : Lancez deux clients (A et B).
2.  **Configuration** : Sur le Client A, entrez l'IP/Port du Client B. Choisissez **3 sauts**.
3.  **Focus sur le Chiffrement** : Avant de cliquer sur envoyer, expliquez que le client va :
    - Récupérer la liste des routeurs.
    - Chiffrer le message pour R3, puis pour R2, puis pour R1.
4.  **Envoi** : Cliquez sur "Envoyer".
5.  **Suivi du Paquet** :
    - Montrez la console du **Routeur 1** : "Paquet reçu -> Déchiffrement couche 1 -> Envoi vers Routeur 2".
    - Montrez la console du **Routeur 2** : "Paquet reçu -> Déchiffrement couche 2 -> Envoi vers Routeur 3".
    - Montrez la console du **Routeur 3** : "Paquet reçu -> Déchiffrement couche 3 -> Envoi vers Client B".
6.  **Réception** : Montrez le Client B recevant le message en clair.

### Séquence 3 : Analyse Technique (5:00 - 7:00)
- Ouvrez `crypto_utils.py`.
- Expliquez l'algorithme de chiffrement hybride (RSA pour la clef, XOR pour le message).
- **Points forts/faibles** : Mentionnez que le XOR est simple mais que le chiffrement en couches garantit que personne (sauf le destinataire) ne voit le message complet.

### Conclusion (7:00 - 8:00)
- Résumé des objectifs atteints (AC23.01 à AC23.05).
- Fin de la démonstration.

---

## 3. CONSEILS POUR L'ENREGISTREMENT
- **Logiciel** : Utilisez OBS Studio ou SimpleScreenRecorder.
- **Audio** : Parlez clairement ou ajoutez des sous-titres lisibles.
- **Fluidité** : Préparez vos fenêtres à l'avance pour ne pas perdre de temps à les redimensionner.

