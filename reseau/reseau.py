import socket as s
import threading
from select import select


class Serveur(threading.Thread):
    nServeurs = 0

    def __init__(self):
        Serveur.nServeurs += 1
        super().__init__(name="Serveur-{}".format(Serveur.nServeurs), daemon=True)
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.serveurAllumé = False
        self.clients = []

        self.socket.bind(("", 12800))
        self.socket.listen(10)

    def start(self):
        super().start()
        self.serveurAllumé = True

    def run(self):
        while self.serveurAllumé:
            connexions_demandees, wlist, xlist = select([self.socket], [], [], 0.05)

            for connexion in connexions_demandees:
                socketClient, infoConnexion = connexion.accept()
                self.clients.append(socketClient)

            if self.clients:
                clients_a_lire, wlist, xlist = select(self.clients,
                                                      [], [], 0.05)

                for client in clients_a_lire:
                    msgRecu = client.recv(1024).decode()
                    print("Reçu {}".format(msgRecu))
                    client.send(b"5 / 5")
                    if msgRecu == "fin":
                        self.serveurAllumé = False

    def stop(self):
        print("ServeurFermeture des connexions")
        self.serveurAllumé = False
        for client in self.clients:
            client.close()

        self.socket.close()


class Client:
    nClients = 0

    def __init__(self):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.serveur = None

    def connect(self, address):