# =========================
# Gestion de la base MySQL
# =========================

import mysql.connector  # Bibliothèque pour se connecter à MySQL / MariaDB

# Paramètres de connexion à la base
USER = 'onion'
PASSWORD = 'onion'
HOST = 'localhost'
DATABASE = 'onion_routing_db'


def get_connexion():
    """
    Établit une connexion à la base de données.
    Essaye d'abord avec le socket Linux, puis avec l'adresse IP.
    """
    try:
        # Connexion via socket (souvent utilisé sous Linux)
        bdd = mysql.connector.connect(
            user=USER,
            password=PASSWORD,
            host='localhost',
            database=DATABASE,
            unix_socket='/run/mysqld/mysqld.sock'
        )
        return bdd
    except:
        try:
            # Connexion classique via TCP/IP
            bdd = mysql.connector.connect(
                user=USER,
                password=PASSWORD,
                host='127.0.0.1',
                database=DATABASE
            )
            return bdd
        except Exception as e:
            print(f"Erreur de connexion BDD : {e}")
            return None


def init_bdd():
    """
    Initialise la base de données :
    - crée la base si elle n'existe pas
    - crée la table routeurs si elle n'existe pas
    """
    try:
        # Connexion sans préciser la base (pour pouvoir la créer)
        try:
            bdd = mysql.connector.connect(
                user=USER,
                password=PASSWORD,
                host='localhost',
                unix_socket='/run/mysqld/mysqld.sock'
            )
        except:
            bdd = mysql.connector.connect(
                user=USER,
                password=PASSWORD,
                host='127.0.0.1'
            )

        cursor = bdd.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
        bdd.close()

        # Connexion à la base créée
        bdd = get_connexion()
        cursor = bdd.cursor()

        # Création de la table des routeurs
        sql = """
        CREATE TABLE IF NOT EXISTS routeurs (
            ip VARCHAR(50),
            port INT,
            e TEXT,
            n TEXT
        )
        """
        cursor.execute(sql)
        bdd.commit()
        bdd.close()

        print("BDD prête.")
        return True

    except Exception as e:
        print("Erreur init:", e)
        return False


def ajouter_routeur(ip, port, e, n):
    """
    Ajoute un routeur dans la base de données.
    Supprime l'ancien enregistrement s'il existe déjà.
    """
    bdd = get_connexion()
    if not bdd:
        return

    cursor = bdd.cursor()

    # Suppression du routeur s'il existe déjà
    cursor.execute(
        "DELETE FROM routeurs WHERE ip=%s AND port=%s",
        (ip, port)
    )

    # Insertion du routeur
    cursor.execute(
        "INSERT INTO routeurs (ip, port, e, n) VALUES (%s, %s, %s, %s)",
        (ip, port, str(e), str(n))
    )

    bdd.commit()
    bdd.close()


def lire_routeurs():
    """
    Récupère la liste de tous les routeurs enregistrés.
    """
    bdd = get_connexion()
    if not bdd:
        return []

    cursor = bdd.cursor()
    cursor.execute("SELECT ip, port, e, n FROM routeurs")
    resultats = cursor.fetchall()
    bdd.close()

    return resultats
