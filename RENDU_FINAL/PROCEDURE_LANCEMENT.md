# 🚀 Procédure de Lancement du Projet

Ce document explique étape par étape comment configurer vos machines virtuelles et lancer le projet de routage en oignon.

---

## 1. Configuration du Réseau (VirtualBox)
Avant de lancer les VMs, assurez-vous qu'elles peuvent communiquer entre elles.

1.  Ouvrez **VirtualBox**.
2.  Allez dans **Fichier > Outils > Gestionnaire de réseau NAT**.
3.  Créez un nouveau réseau nommé `OnionNet` (Plage IP : `10.0.2.0/24`).
4.  Pour **chaque VM** (Annuaire, Routeurs, Clients) :
    - Allez dans **Configuration > Réseau**.
    - Mode d'accès : **Réseau NAT**.
    - Nom : **OnionNet**.

---

## 2. Préparation de la VM Annuaire (Master)
L'Annuaire doit avoir une IP fixe pour que les autres nœuds le trouvent.

1.  Lancez la VM **Annuaire**.
2.  Ouvrez un terminal et forcez l'IP `10.0.2.10` :
    ```bash
    # Ajouter l'IP fixe
    sudo ip addr add 10.0.2.10/24 dev eth0
    
    # Supprimer l'ancienne IP dynamique (10.0.2.15) pour éviter les conflits
    sudo ip addr del 10.0.2.15/24 dev eth0
    ```
3.  Vérifiez avec `ip addr` (seule l'IP `10.0.2.10` doit rester sur `eth0`).
4.  **Démarrer MariaDB** (Indispensable) :
    ```bash
    sudo service mariadb start
    ```
5.  **Fixer les permissions SQL** (Si erreur "Access denied") :
    ```bash
    sudo mysql -e "CREATE USER IF NOT EXISTS 'onion'@'localhost' IDENTIFIED BY 'onion'; ALTER USER 'onion'@'localhost' IDENTIFIED BY 'onion'; GRANT ALL PRIVILEGES ON *.* TO 'onion'@'localhost' WITH GRANT OPTION; FLUSH PRIVILEGES;"
    ```
6.  Initialisez la base de données :
    ```bash
    python3 db.py
    ```

---

## 3. Lancement du Projet (Ordre de marche)

### Étape 1 : L'Annuaire
Sur la VM **Annuaire** :
1.  Lancez le script : `python3 directory.py`
2.  Cliquez sur le bouton **"Lancer le serveur"**.
3.  Le log doit afficher : `Serveur prêt sur 10.0.2.10:9000`.

### Étape 2 : Les Routeurs
Sur les VMs **Routeurs** (ou la même VM si vous simulez) :
1.  Lancez le script : `python3 router.py`
2.  Cliquez sur **"Démarrer"**.
3.  Vérifiez le log : `Inscrit à l'annuaire (10.0.2.10)`.
4.  *Répétez l'opération pour au moins 3 routeurs.*

### Étape 3 : Les Clients
Sur les VMs **Clients** :
1.  Lancez le script : `python3 client.py`
2.  Le client est prêt à envoyer et recevoir.

---

## 4. Test de Communication
1.  Sur le **Client B** (Récepteur) : Notez son port d'écoute (affiché dans l'interface).
2.  Sur le **Client A** (Émetteur) :
    - **IP Destinataire** : IP de la VM du Client B (souvent `10.0.2.x`).
    - **Port Destinataire** : Le port noté précédemment.
    - **Sauts** : Choisissez `3`.
    - **Message** : Tapez votre texte.
    - Cliquez sur **"Envoyer"**.
3.  **Vérification** : Le message doit apparaître sur le Client B après être passé par les routeurs.

---

## 💡 Astuces
- Si vous avez une erreur de base de données, relancez le script `install_dependencies.py` ou vérifiez les droits MariaDB comme expliqué dans le rapport.
- Assurez-vous que tous les fichiers (`client.py`, `crypto.py`, `db.py`, `directory.py`, `router.py`) sont présents dans le même dossier sur chaque VM.
