import socket
import threading
import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QTextEdit, QLineEdit
from PyQt5.QtCore import pyqtSignal

import crypto
import socket

# Si sur le même PC, laisser 127.0.0.1
IP_ANNUAIRE = '10.0.2.10' 

class RouteurWindow(QMainWindow):
    signal_log = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Routeur Oignon")
        self.resize(400, 300)
        
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        self.mon_port = random.randint(8000, 8999)
        
        self.label = QLabel(f"Port : {self.mon_port}")
        self.layout.addWidget(self.label)
        
        self.btn = QPushButton("Démarrer")
        self.btn.clicked.connect(self.demarrer)
        self.layout.addWidget(self.btn)
        
        self.logs = QTextEdit()
        self.layout.addWidget(self.logs)
        
        self.mes_clefs = None

        self.signal_log.connect(self.ecrire_log)

    def log(self, msg):
        self.signal_log.emit(msg)

    def ecrire_log(self, msg):
        self.logs.append(msg)

    def demarrer(self):
        self.btn.setEnabled(False)
        self.log("Génération des clefs...")
        
        threading.Thread(target=self.init_routeur).start()

    def init_routeur(self):
        self.mes_clefs = crypto.generer_clefs()
        pub = self.mes_clefs[0]
        self.log("Clefs OK.")
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((IP_ANNUAIRE, 9000))

            try:
                tmp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                tmp.connect((IP_ANNUAIRE, 9000))
                mon_ip = tmp.getsockname()[0]
                tmp.close()
            except:
                mon_ip = '127.0.0.1'

            msg = f"INSCRIPTION|{mon_ip}|{self.mon_port}|{pub[0]}|{pub[1]}"
            s.send(msg.encode('utf-8'))
            s.close()
            self.log(f"Inscrit à l'annuaire ({IP_ANNUAIRE}) avec IP {mon_ip}.")
        except:
            self.log("Erreur connexion annuaire.")
            return

        serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serveur.bind(('0.0.0.0', self.mon_port))
        serveur.listen(5)
        self.log("En attente de messages...")
        
        while True:
            client, addr = serveur.accept()
            threading.Thread(target=self.traiter_message, args=(client,)).start()

    def traiter_message(self, client):
        try:
            donnees = client.recv(10240).decode('utf-8')
            self.log("Message reçu !")
            
            message_clair = crypto.dechiffrer(donnees, self.mes_clefs[1])
            
            if message_clair == "Erreur":
                self.log("Echec déchiffrement.")
                return
            
            parties = message_clair.split("|", 2)
            prochain_ip = parties[0]
            prochain_port = int(parties[1])
            reste_du_message = parties[2]
            
            if prochain_ip == "FIN":
                self.log(f">>> MESSAGE FINAL : {reste_du_message}")
            else:
                self.log(f"Je passe à {prochain_port}")
                s_suivant = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s_suivant.connect((prochain_ip, prochain_port))
                s_suivant.send(reste_du_message.encode('utf-8'))
                s_suivant.close()
                
            client.close()
        except Exception as e:
            self.log(f"Erreur traitement : {e}")

app = QApplication(sys.argv)
fen = RouteurWindow()
fen.show()
sys.exit(app.exec_())
