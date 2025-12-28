import socket
import threading
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtCore import pyqtSignal

import db

class AnnuaireWindow(QMainWindow):
    signal_log = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Annuaire (Master)")
        self.resize(400, 300)
        
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        self.label = QLabel("Serveur Annuaire")
        self.layout.addWidget(self.label)
        
        self.btn = QPushButton("Lancer le serveur")
        self.btn.clicked.connect(self.lancer_serveur)
        self.layout.addWidget(self.btn)
        
        self.logs = QTextEdit()
        self.layout.addWidget(self.logs)
        
        db.init_bdd()
        
        self.signal_log.connect(self.ecrire_log)

    def lancer_serveur(self):
        self.btn.setEnabled(False)
        self.log("Démarrage...")
        t = threading.Thread(target=self.ecouter)
        t.daemon = True
        t.start()

    def log(self, message):
        self.signal_log.emit(message)

    def ecrire_log(self, message):
        self.logs.append(message)

    def ecouter(self):
        serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur.bind(('0.0.0.0', 9000))
        serveur.listen(5)

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_locale = s.getsockname()[0]
            s.close()
        except:
            ip_locale = "127.0.0.1"
            
        self.log(f"Serveur prêt sur {ip_locale}:9000 (Ecoute sur toutes les interfaces)")
        
        while True:
            client, adresse = serveur.accept()

            threading.Thread(target=self.gerer_client, args=(client,)).start()

    def gerer_client(self, client):
        try:
            message = client.recv(1024).decode('utf-8')
            self.log(f"Reçu : {message}")
            parties = message.split("|")
            commande = parties[0]
            
            if commande == "INSCRIPTION":
                ip = parties[1]
                port = int(parties[2])
                e = parties[3]
                n = parties[4]
                db.ajouter_routeur(ip, port, e, n)
                client.send("OK".encode('utf-8'))
                self.log(f"Routeur inscrit : {port}")
                
            elif commande == "LISTE":
                routeurs = db.lire_routeurs()
                liste_txt = []
                for r in routeurs:
                    info = f"{r[0]};{r[1]};{r[2]};{r[3]}"
                    liste_txt.append(info)
                
                reponse = "|".join(liste_txt)
                client.send(reponse.encode('utf-8'))
                self.log("Liste envoyée")
                
            client.close()
        except Exception as e:
            self.log(f"Erreur : {e}")



app = QApplication(sys.argv)
fen = AnnuaireWindow()
fen.show()
sys.exit(app.exec_())
