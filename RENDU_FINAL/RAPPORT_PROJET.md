# Rapport de Projet - SAE 3.02
## Conception d'une architecture distribuée avec routage en oignon

**Groupe : [NOM DU GROUPE]**
**Membres : Quentin [NOM], [NOM 2], [NOM 3]**

---

### 1. Introduction et Genèse du Projet
Au début de cette SAE, quand on nous a présenté le sujet du routage en oignon, on a tout de suite pensé à Tor. C'est un concept qui fascine pas mal quand on s'intéresse à la cybersécurité, mais on ne s'imaginait pas forcément la complexité qu'il y avait derrière pour le coder soi-même. L'objectif était clair : créer un système où un message traverse plusieurs nœuds sans qu'aucun d'entre eux ne puisse connaître le chemin complet. C'est un défi qui nous a tout de suite motivés parce que ça touche à plein de domaines qu'on a vus en cours : le réseau pur avec les sockets, la programmation système avec les threads, la gestion de données avec MariaDB, et bien sûr la cryptographie qui est le cœur du système. On a abordé ce projet avec l'envie de construire quelque chose de solide, de "pro", tout en respectant les contraintes assez strictes du sujet qui nous interdisaient d'utiliser les outils de facilité habituels comme JSON ou les bibliothèques de chiffrement de haut niveau.

### 2. Une aventure technique et humaine
Travailler sur un projet de cette envergure, c'est avant tout une aventure humaine. On a dû apprendre à s'organiser, à se faire confiance et à communiquer efficacement. Au début, on a passé pas mal de temps à simplement discuter de l'architecture. On se demandait comment les routeurs allaient savoir où envoyer le message sans tout voir. C'est là qu'on a vraiment compris la métaphore de l'oignon : chaque couche de chiffrement cache l'étape suivante. 

Quentin a pris les rênes de l'architecture réseau. Il a passé des heures à debugger des problèmes de sockets qui ne se fermaient pas correctement ou des connexions qui tombaient sans raison apparente. De son côté, [NOM 2] s'est plongé dans PyQt5. On voulait que le projet ne soit pas juste des lignes de texte dans un terminal, mais quelque chose de visuel où on voit vraiment le message transiter. C'était pas facile de gérer l'affichage en temps réel sans que l'interface ne freeze dès qu'un paquet arrivait. [NOM 3] a eu la tâche sans doute la plus ingrate mais la plus cruciale : coder le RSA. Sans bibliothèque, c'est tout de suite plus mathématique. Il a fallu gérer les grands nombres, les tests de primalité, l'algorithme d'Euclide étendu... C'était un vrai casse-tête mais quand on a vu le premier message se déchiffrer correctement, c'était une petite victoire pour tout le groupe.

### 3. Le défi du chiffrement et l'optimisation
#### 3.1 Architecture
Le projet est découpé en plusieurs scripts Python :
- `directory.py` : C'est le "cerveau", il liste tous les routeurs qui sont en ligne.
- `router.py` : C'est le script qu'on lance sur les machines intermédiaires.
- `client.py` : C'est l'appli pour envoyer et recevoir les messages.
- `crypto.py` : Toutes nos fonctions de calcul pour le RSA et le XOR.

#### 3.2 Le Chiffrement (Le gros morceau)
Comme on n'avait pas le droit à `cryptography`, on a dû coder le RSA à la main. Au début, on chiffrait tout le message avec RSA, mais c'était super lent et le message devenait énorme (plusieurs Mo pour trois mots !).
Du coup, on a changé de technique : on utilise un chiffrement **hybride**. On génère une clé au hasard, on chiffre le message avec un simple XOR (très rapide), et on ne chiffre que la clé de session avec RSA. Ça marche super bien et c'est beaucoup plus léger.
Le moment le plus marquant du projet a probablement été celui où on a réalisé que notre système de chiffrement RSA "pur" ne fonctionnerait jamais dans la vraie vie. On était tout fiers d'avoir réussi à chiffrer nos messages, mais dès qu'on passait par trois routeurs, le paquet devenait tellement énorme qu'il mettait des plombes à transiter sur le réseau. On s'est retrouvés face à un mur : soit on restait sur notre idée de base et le projet était inutilisable, soit on trouvait une solution. 

C'est là qu'on a découvert le concept de chiffrement hybride. On a réalisé que le RSA est génial pour échanger des secrets, mais que pour chiffrer du texte brut, c'est beaucoup trop lourd. On a donc décidé d'utiliser le RSA uniquement pour chiffrer une petite clé de session, et d'utiliser cette clé pour chiffrer le message avec un XOR. C'était une révélation. D'un coup, nos messages sont passés de plusieurs mégaoctets à quelques kilo-octets. Ça nous a appris une leçon super importante en informatique : la théorie c'est bien, mais il faut toujours penser à l'efficacité et à la réalité du matériel. On a passé une nuit blanche à tout réécrire pour intégrer ce système hybride, mais le résultat en valait la peine.

#### 3.3 Base de données
On a utilisé MariaDB pour l'annuaire. Ça permet de garder la liste des routeurs même si on redémarre le serveur. On a créé une table simple avec l'IP, le port et la clé publique de chaque routeur.

### 4. L'apprentissage par l'erreur : Le réseau et la BDD
Le côté "distribué" du projet nous a aussi donné pas mal de fil à retordre. On a voulu faire les choses bien en utilisant plusieurs machines virtuelles sous VirtualBox. C'est là qu'on a découvert les joies (ou les peines) de la configuration réseau. Entre le mode NAT, le mode Pont et le Réseau NAT, on s'est un peu perdus au début. On a fini par comprendre qu'il fallait un réseau dédié pour que nos VMs se voient sans être perturbées par le reste. Fixer l'IP de l'annuaire à `10.0.2.10` a été le point de bascule qui a tout stabilisé.

Côté base de données, on a dû se familiariser avec MariaDB. On n'avait pas l'habitude d'intégrer du SQL directement dans du Python. Gérer les erreurs de connexion, s'assurer que les données étaient bien insérées et surtout qu'elles étaient à jour (pour ne pas avoir de vieux routeurs fantômes dans la liste) a été un bon exercice d'administration système. On a appris à être rigoureux : chaque routeur doit s'enregistrer proprement, et le client doit pouvoir récupérer cette liste de manière fiable. C'est ce qui fait que le système semble "vivant" quand on le lance.

### 5. Réflexions sur les compétences et le futur
En regardant en arrière, on se rend compte que ce projet nous a fait progresser sur énormément de points. On a validé des compétences techniques, bien sûr, comme la programmation réseau ou la sécurité, mais on a aussi appris à gérer un projet complexe de A à Z. On a dû faire des choix techniques, parfois revenir en arrière, et toujours garder en tête l'objectif final. 

On a appris à automatiser nos tâches avec des scripts d'installation, ce qui nous a sauvé la mise plus d'une fois quand on devait réinitialiser une VM. On a appris à documenter notre travail, non pas parce que c'était demandé, mais parce qu'on se perdait nous-mêmes dans notre code au bout de quelques jours. Si on devait recommencer, on essaierait peut-être d'implémenter un système de "heartbeat" pour que l'annuaire sache tout de suite si un routeur est tombé. Mais pour l'instant, on est fiers de ce qu'on a accompli. Ce projet nous a montré que même avec des contraintes fortes, on peut construire un système sécurisé et fonctionnel si on comprend bien les principes de base.

### 6. Conclusion
Pour conclure, cette SAE 3.02 a été bien plus qu'un simple exercice de code. C'était une plongée dans les entrailles de la sécurité réseau. On en ressort avec une vision beaucoup plus claire de la protection des données et de l'anonymat sur internet. On a travaillé dur, on a eu des moments de doute, mais voir le système tourner parfaitement sur nos trois VMs à la fin, c'était vraiment gratifiant. C'est le genre de projet qui nous conforte dans notre choix de filière R&T et qui nous donne envie d'aller encore plus loin dans la cybersécurité.

---
**Annexes techniques :**
- `GUIDE_INSTALLATION.md` : Pour la mise en place.
- `DOCUMENTATION_TECHNIQUE.md` : Pour le détail des algorithmes.
- `SCENARIO_VIDEO.md` : Pour la démonstration.
