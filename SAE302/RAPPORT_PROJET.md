# Rapport de Projet - SAE 3.02
## Architecture distribuée et Routage en Oignon

**Groupe : [NOM DU GROUPE]**
**Membres : Quentin [NOM], [NOM 2], [NOM 3]**

---

### 1. Introduction
Dans le cadre de cette SAE, on devait créer un système de messagerie anonyme en utilisant le principe du routage en oignon. Le but est que les messages passent par plusieurs routeurs pour qu'on ne sache pas qui envoie quoi à qui. On a dû tout coder nous-mêmes, surtout la partie chiffrement, car on n'avait pas le droit aux bibliothèques toutes faites comme `cryptography` ou `json`.

### 2. Organisation et Gestion du Projet
On s'est réparti le travail pour avancer plus vite :
- **Quentin** s'est occupé de la structure globale et du serveur annuaire.
- **[NOM 2]** a géré la partie interface graphique avec PyQt5.
- **[NOM 3]** a travaillé sur l'algorithme de chiffrement RSA et la base de données.

On a utilisé Git pour partager le code et on a fait pas mal de réunions pour tester si les routeurs arrivaient bien à se parler entre eux.

### 3. Réalisation Technique

#### 3.1 Architecture
Le projet est découpé en plusieurs scripts Python :
- `directory_node.py` : C'est le "cerveau", il liste tous les routeurs qui sont en ligne.
- `onion_router.py` : C'est le script qu'on lance sur les machines intermédiaires.
- `client.py` : C'est l'appli pour envoyer et recevoir les messages.
- `crypto_utils.py` : Toutes nos fonctions de calcul pour le RSA et le XOR.

#### 3.2 Le Chiffrement (Le gros morceau)
Comme on n'avait pas le droit à `cryptography`, on a dû coder le RSA à la main. Au début, on chiffrait tout le message avec RSA, mais c'était super lent et le message devenait énorme (plusieurs Mo pour trois mots !).
Du coup, on a changé de technique : on utilise un chiffrement **hybride**. On génère une clé au hasard, on chiffre le message avec un simple XOR (très rapide), et on ne chiffre que la petite clé avec RSA. Ça marche super bien et c'est beaucoup plus léger.

#### 3.3 Base de données
On a utilisé MariaDB pour l'annuaire. Ça permet de garder la liste des routeurs même si on redémarre le serveur. On a créé une table simple avec l'IP, le port et la clé publique de chaque routeur.

### 4. Difficultés rencontrées
On a eu pas mal de soucis :
1. **Taille des messages** : Comme expliqué au-dessus, le RSA pur c'était une mauvaise idée. On a perdu deux jours là-dessus avant de passer à l'hybride.
2. **Multi-VM** : Faire marcher le tout sur plusieurs machines virtuelles a été galère à cause des adresses IP. On a dû bien configurer le réseau NAT dans VirtualBox.
3. **PyQt5 et les Threads** : L'interface freezait quand on recevait un message. On a dû apprendre à utiliser les `Signals` pour que l'affichage reste fluide.

### 5. Résultats et Conclusion
Au final, notre projet fonctionne bien. On peut choisir le nombre de "sauts" (le nombre de routeurs) et le message arrive bien à destination sans que les routeurs du milieu puissent lire le contenu.
Ça nous a permis de mieux comprendre comment fonctionne Tor et de voir que la sécurité, c'est pas si facile que ça à mettre en place !

---
**Livrables joints :**
- Code source complet
- Guide d'installation
- Documentation technique
- Vidéo de démo
