import os

def installer():
    print("--- INSTALLATION SAE 3.02 ---")
    
    # Liste des commandes à lancer
    commandes = [
        "sudo apt update",
        "sudo apt install -y mariadb-server python3-pip python3-pyqt5 python3-sympy",
        "pip3 install mysql-connector-python --break-system-packages || pip3 install mysql-connector-python",
        "sudo systemctl start mariadb || sudo service mariadb start"
    ]

    for cmd in commandes:
        print(f"\n> Execution de : {cmd}")
        os.system(cmd)

    print("\n" + "="*30)
    print("TERMINE ! TOUT EST INSTALLE.")
    print("="*30)

if __name__ == "__main__":
    installer()
