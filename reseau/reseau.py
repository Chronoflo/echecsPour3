import socket as s
import threading
from select import select


class ServeurThread(threading.Thread):
    nServeurs = 0

    def __init__(self):
        ServeurThread.nServeurs += 1
        super().__init__(name="Serveur-{}".format(ServeurThread.nServeurs), daemon=True)
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.serveurAllumé = False
        self.clients = []

        self.socket.bind(("", 12800))
        self.socket.listen(10)

    def start(self):
        self.serveurAllumé = True
        print("Réseau :: Serveur en ligne")
        super().start()

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


class Serveur:
    def __init__(self):
        self.serveur = None

    def start(self):
        if self.serveur is None:
            self.serveur = ServeurThread()
            self.serveur.start()
        else:
            print("Réseau :: Serveur déjà lancé")


class Client:
    nClients = 0

    def __init__(self):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.serveur = None

    def connect(self, address=s.gethostname(), port=12800):
        self.socket.connect((address, port))
        self.socket.send(b"Coucou")


if __name__ == '__main__':
    Client().connect()
