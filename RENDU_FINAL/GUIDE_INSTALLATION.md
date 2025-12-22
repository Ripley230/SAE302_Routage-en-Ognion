# 🛠️ Guide d'Installation et d'Utilisation

> **Ce guide détaille les étapes pour mettre en place l'environnement de test et lancer le système de routage en oignon.**

---

## 📖 Sommaire
1. [Configuration des VMs](#-configuration-des-machines-virtuelles-vm)
2. [Prérequis Logiciels](#-prérequis-logiciels)
3. [Installation et Configuration](#-installation-et-configuration)
4. [Lancement du Projet](#-lancement-du-projet)
5. [Test de Fonctionnement](#-test-de-fonctionnement)
6. [Dépannage (FAQ)](#-dépannage-faq)

---

## 🖥️ Configuration des Machines Virtuelles (VM)

Pour simuler une architecture distribuée réelle, nous recommandons l'utilisation de **VirtualBox**.

### 1. Création des VMs
1. **ISO** : Utilisez Kali Linux ou Debian.
2. **Nœuds** : Créez une VM "Master" et clonez-la pour les routeurs et clients.
3. **Ressources** : 2 Go de RAM et 20 Go de disque par VM suffisent.

### 2. Configuration du Réseau (Crucial)
1. **Réseau NAT** : Dans VirtualBox, créez un réseau NAT nommé `OnionNet` (Plage : `10.0.2.0/24`).
2. **Attribution** : Connectez toutes vos VMs à ce réseau.
3. **IP Fixe (Annuaire)** : Sur la VM Annuaire, fixez l'IP pour la stabilité :
   ```bash
   sudo ip addr add 10.0.2.10/24 dev eth0
   ```

---

## 📋 Prérequis Logiciels

### Installation Automatique (Recommandé)
Un script est fourni pour installer toutes les dépendances d'un coup sur chaque VM :
```bash
sudo python3 install_dependencies.py
```

### Installation Manuelle
Si vous préférez installer les composants séparément :
```bash
# Dépendances système
sudo apt update
sudo apt install -y mariadb-server python3-pip python3-pyqt5 python3-sympy

# Bibliothèque Python
pip3 install mysql-connector-python --break-system-packages
```

---

## ⚙️ Installation et Configuration

### 1. Base de Données (VM Annuaire uniquement)
```bash
# Démarrage du service
sudo service mariadb start

# Création de l'utilisateur et des droits
sudo mysql -e "CREATE USER IF NOT EXISTS 'onion'@'localhost' IDENTIFIED BY 'onion'; GRANT ALL PRIVILEGES ON *.* TO 'onion'@'localhost'; FLUSH PRIVILEGES;"
```

### 2. Initialisation des Tables
```bash
python3 db.py
```
*Vérifiez que le message "BDD prête" s'affiche.*

---

## 🚀 Lancement du Projet

### Étape 1 : Configuration des IPs
Dans `router.py` et `client.py`, vérifiez que la variable `IP_ANNUAIRE` correspond à l'IP de votre VM Master :
```python
IP_ANNUAIRE = '10.0.2.10'
```

### Étape 2 : Ordre de Lancement
1. **Annuaire** : `python3 directory.py` -> Cliquez sur **"Lancer le serveur"**.
2. **Routeurs** : `python3 router.py` -> Cliquez sur **"Démarrer"**.
3. **Clients** : `python3 client.py`.

---

## 🧪 Test de Fonctionnement
1. Lancez deux clients (A et B).
2. Sur le Client A, entrez l'IP et le port du Client B.
3. Choisissez **3 sauts** et envoyez un message.
4. Observez le transit du message sur les interfaces des routeurs.

---

## ❓ Dépannage (FAQ)

**Q : Les routeurs affichent "Erreur connexion annuaire"**
> Vérifiez que l'IP dans `IP_ANNUAIRE` est bien celle de la VM Master et que le serveur annuaire est lancé.

**Q : Erreur "Access denied" pour MariaDB**
> Relancez les commandes de création d'utilisateur à l'étape "Installation et Configuration".

**Q : Pas d'internet dans la VM ?**
> Passez temporairement la carte réseau en mode "NAT" simple pour les installations, puis remettez en "Réseau NAT" pour les tests.
