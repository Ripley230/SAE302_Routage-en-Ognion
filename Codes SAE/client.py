# =========================
# Imports des bibliothèques
# =========================

import socket          # Gestion des sockets réseau
import sys             # Accès aux paramètres système
import random          # Génération de valeurs aléatoires
import threading       # Gestion du multithreading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QWidget, QTextEdit, QLineEdit, QSpinBox
)
from PyQt5.QtCore import pyqtSignal

import crypto          # Module de chiffrement (oignon)
import socket

# Adresse IP du serveur annuaire (liste des routeurs)
# Si tout est sur le même PC, utiliser 127.0.0.1
IP_ANNUAIRE = '10.0.2.10'


class ClientWindow(QMainWindow):
    # Signal Qt utilisé pour afficher les logs depuis les threads
    signal_log = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Paramètres de la fenêtre
        self.setWindowTitle("Client Oignon (Envoyeur & Receveur)")
        self.resize(500, 600)

        # Mise en place du layout principal
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Port aléatoire pour recevoir les messages
        self.mon_port = random.randint(9000, 9999)
        self.label_port = QLabel(f"<b>Mon Port (pour recevoir) : {self.mon_port}</b>")
        self.layout.addWidget(self.label_port)

        # -----------------
        # Zone d'envoi
        # -----------------

        self.layout.addWidget(QLabel("--- Envoi de Message ---"))

        # IP du destinataire
        self.input_dest_ip = QLineEdit("127.0.0.1")
        self.input_dest_ip.setPlaceholderText("IP du destinataire")
        self.layout.addWidget(self.input_dest_ip)

        # Port du destinataire
        self.input_dest_port = QLineEdit()
        self.input_dest_port.setPlaceholderText("Port du destinataire")
        self.layout.addWidget(self.input_dest_port)

        # Nombre de routeurs utilisés (sauts)
        self.layout.addWidget(QLabel("Nombre de routeurs (sauts) :"))
        self.spin_sauts = QSpinBox()
        self.spin_sauts.setRange(1, 10)
        self.spin_sauts.setValue(3)
        self.layout.addWidget(self.spin_sauts)

        # Message à envoyer
        self.input_msg = QLineEdit()
        self.input_msg.setPlaceholderText("Votre message...")
        self.layout.addWidget(self.input_msg)

        # Bouton d'envoi
        self.btn_send = QPushButton("Envoyer")
        self.btn_send.clicked.connect(self.envoyer)
        self.layout.addWidget(self.btn_send)

        # -----------------
        # Zone de logs
        # -----------------

        self.layout.addWidget(QLabel("--- Logs / Messages Reçus ---"))
        self.logs = QTextEdit()
        self.logs.setReadOnly(True)
        self.layout.addWidget(self.logs)

        # Liste des routeurs récupérés depuis l'annuaire
        self.routeurs = []

        # Connexion du signal aux logs
        self.signal_log.connect(self.ecrire_log)

        # Lancement du serveur d'écoute en arrière-plan
        threading.Thread(target=self.ecouter_messages, daemon=True).start()

    # Fonction pour envoyer un message dans les logs
    def log(self, msg):
        self.signal_log.emit(msg)

    # Affichage du message dans la zone de logs
    def ecrire_log(self, msg):
        self.logs.append(msg)

    # =========================
    # Réception des messages
    # =========================

    def ecouter_messages(self):
        """Serveur TCP pour recevoir des messages"""
        try:
            serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serveur.bind(('0.0.0.0', self.mon_port))
            serveur.listen(5)

            self.log(f"Prêt à recevoir des messages sur le port {self.mon_port}")

            while True:
                client, addr = serveur.accept()
                # Chaque message est traité dans un thread séparé
                threading.Thread(
                    target=self.gerer_reception,
                    args=(client,)
                ).start()
        except Exception as e:
            self.log(f"Erreur écoute : {e}")

    def gerer_reception(self, client):
        """Réception d'un message entrant"""
        try:
            msg = client.recv(10240).decode('utf-8')
            self.log(f">>> MESSAGE REÇU : {msg}")
            client.close()
        except:
            pass

    # =========================
    # Récupération des routeurs
    # =========================

    def recuperer_routeurs(self):
        """Contacte l'annuaire pour obtenir la liste des routeurs"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IP_ANNUAIRE, 9000))
            s.send("LISTE".encode('utf-8'))

            reponse = s.recv(4096).decode('utf-8')
            s.close()

            if not reponse:
                self.log("Erreur : Aucun routeur n'est inscrit dans l'annuaire.")
                return False

            # Format : ip;port;n;e|ip;port;n;e|...
            liste = reponse.split("|")
            self.routeurs = []

            for item in liste:
                parts = item.split(";")
                r = {
                    "ip": parts[0],
                    "port": int(parts[1]),
                    "clef": (int(parts[2]), int(parts[3]))
                }
                self.routeurs.append(r)

            return True
        except:
            self.log("Erreur : Impossible de joindre l'annuaire.")
            return False

    # =========================
    # Envoi du message oignon
    # =========================

    def envoyer(self):
        msg = self.input_msg.text()
        dest_ip = self.input_dest_ip.text()
        dest_port_str = self.input_dest_port.text()
        nb_sauts = self.spin_sauts.value()

        # Vérification des champs
        if not msg or not dest_port_str:
            self.log("Erreur : Remplissez le message et le port destinataire.")
            return

        dest_port = int(dest_port_str)

        # Récupération des routeurs
        if not self.recuperer_routeurs():
            return

        # Vérification du nombre de routeurs disponibles
        if len(self.routeurs) < nb_sauts:
            self.log(
                f"Erreur : Pas assez de routeurs disponibles "
                f"({len(self.routeurs)}) pour {nb_sauts} sauts."
            )
            return

        # Choix aléatoire des routeurs
        chemin = random.sample(self.routeurs, nb_sauts)
        ports_chemin = " -> ".join([str(r['port']) for r in chemin])
        self.log(f"Chemin choisi ({nb_sauts} sauts) : {ports_chemin} -> {dest_port}")

        # Message final à transmettre
        message_a_transmettre = f"{dest_ip}|{dest_port}|{msg}"

        # Chiffrement en couches (oignon)
        for routeur in reversed(chemin):
            message_chiffre = crypto.chiffrer(
                message_a_transmettre,
                routeur['clef']
            )
            message_a_transmettre = (
                f"{routeur['ip']}|{routeur['port']}|{message_chiffre}"
            )

        # Extraction du premier routeur
        parties = message_a_transmettre.split("|", 2)
        ip_premier_noeud = parties[0]
        port_premier_noeud = int(parties[1])
        payload_final = parties[2]

        # Envoi du message au premier routeur
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip_premier_noeud, port_premier_noeud))
            s.send(payload_final.encode('utf-8'))
            s.close()
            self.log("Message envoyé !")
        except Exception as e:
            self.log(f"Erreur envoi : {e}")


# =========================
# Lancement de l'application
# =========================

app = QApplication(sys.argv)
fen = ClientWindow()
fen.show()
sys.exit(app.exec_())
