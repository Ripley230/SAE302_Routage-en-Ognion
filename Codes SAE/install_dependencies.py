# =========================
# Script d'installation SAE 3.02
# =========================

import os   # Permet d'exécuter des commandes système


def installer():
    """
    Lance automatiquement l'installation des outils nécessaires
    pour le projet SAE 3.02.
    """
    print("--- INSTALLATION SAE 3.02 ---")

    # Liste des commandes Linux à exécuter
    commandes = [
        "sudo apt update",
        # Installation des paquets nécessaires :
        # - mariadb-server : base de données
        # - python3-pip : gestion des paquets Python
        # - python3-pyqt5 : interface graphique
        # - python3-sympy : calculs mathématiques (RSA)
        "sudo apt install -y mariadb-server python3-pip python3-pyqt5 python3-sympy",

        # Installation du connecteur MySQL pour Python
        # L'option --break-system-packages est utilisée sur certaines distributions
        "pip3 install mysql-connector-python --break-system-packages || pip3 install mysql-connector-python",

        # Démarrage du service MariaDB
        "sudo systemctl start mariadb || sudo service mariadb start"
    ]

    # Exécution des commandes une par une
    for cmd in commandes:
        print(f"\n> Execution de : {cmd}")
        os.system(cmd)

    # Message de fin
    print("\n" + "=" * 30)
    print("TERMINE ! TOUT EST INSTALLE.")
    print("=" * 30)


# Point d'entrée du script
if __name__ == "__main__":
    installer()
