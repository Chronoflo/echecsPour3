import socket as s
import threading
from select import select

sep = "\b"


def make_msg(text):
    return (text + sep).encode()


class ServeurThread(threading.Thread):
    nServeurs = 0

    def __init__(self, callback=None, connectionCallback=None, endCallback=None):
        ServeurThread.nServeurs += 1
        super().__init__(name="Serveur-{}".format(ServeurThread.nServeurs), daemon=True)
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.guiCallback = callback
        self.connectionCallback = connectionCallback
        self.endCallback = endCallback
        self.allumé = False
        self.clients = []

        self.socket.bind(("", 12800))
        self.socket.listen(10)

    def start(self):
        self.allumé = True
        print("Réseau :: Serveur en ligne")
        super().start()

    def broadcast(self, text: str):
        for client in self.clients:
            try:
                client.send(make_msg(text))
            except (ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError):
                self.clients.remove(client)
                print("Réseau :: Un client s'est déconnecté.")

    def run(self):
        while self.allumé:
            connexions_demandees, wlist, xlist = select([self.socket], [], [], 0.05)

            for connexion in connexions_demandees:
                socketClient, infoConnexion = connexion.accept()
                self.clients.append(socketClient)
                if self.connectionCallback is not None:
                    self.connectionCallback()

            if self.clients:
                clients_a_lire, wlist, xlist = select(self.clients,
                                                      [], [], 0.05)

                for client in clients_a_lire:
                    try:
                        msgRecus = client.recv(1024).decode()
                        for msgRecu in msgRecus.split(sep)[:-1]:
                            print("Reçu {}".format(msgRecu))
                            self.guiCallback(msgRecu)

                            for autreClient in self.clients:
                                if autreClient != client:
                                    autreClient.send(make_msg(msgRecu))
                            if msgRecu == "fin":
                                if self.endCallback is not None:
                                    self.endCallback()
                    except (ConnectionResetError, ConnectionRefusedError, ConnectionAbortedError):
                        self.clients.remove(client)
                        self.guiCallback("Un client s'est déconnecté.")

    def stop(self):
        print("Réseau :: Serveur : Fermeture des connexions")
        self.allumé = False
        for client in self.clients:
            client.close()

        # self.socket.close()


class Serveur:
    def __init__(self, callback, connectionCallback):
        self.serveurThread: ServeurThread = None
        self.callback = callback
        self.connectionCallback = connectionCallback

    def start(self):
        if self.serveurThread is None:
            try:
                self.serveurThread = ServeurThread(self.callback, self.connectionCallback, self.désactive)
                self.serveurThread.start()
            except:
                print("Réseau :: Échec mise en place serveur")
        else:
            print("Réseau :: Serveur déjà lancé")

    def estActivé(self):
        return self.serveurThread is not None and self.serveurThread.allumé

    def désactive(self):
        if self.serveurThread is not None:
            self.serveurThread.stop()
            self.serveurThread = None

    def broadcast(self, text):
        self.serveurThread.broadcast(text)


class ClientThread(threading.Thread):
    nClients = 0

    def __init__(self, callback=None):
        super(ClientThread, self).__init__(daemon=True)
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.callback = callback

        self.connecté = False

    def connect(self, adresse, port):
        self.socket.connect((adresse, port))
        self.connecté = True
        self.start()

    def run(self):
        while self.connecté:
            try:
                msgReçus = self.socket.recv(1024).decode()
                for msgReçu in msgReçus.split(sep)[:-1]:
                    print("Reçu {}".format(msgReçu))
                    if self.callback is not None:
                        self.callback(msgReçu)
            except (ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
                self.désactive()

    def send(self, text):
        try:
            self.socket.send(make_msg(text))
        except (ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
            self.désactive()

    def désactive(self):
        self.connecté = False
        self.socket.close()
        if self.callback is not None:
            self.callback("m: *Déconnecté*")


class Client:
    def __init__(self, callback=None):
        self.adresseCible = s.gethostname()
        self.portCible = 12800
        self.callback = callback
        self.thread = ClientThread(callback)

    def estConnecté(self):
        return self.thread.connecté and self.thread.is_alive()

    def connect(self):
        try:
            if not self.thread.connecté:
                self.thread.connect(self.adresseCible, self.portCible)
            else:
                print("ClientThread déjà connectée.")
        except (ConnectionRefusedError, ConnectionError):
            self.désactive()
            self.thread.connect(self.adresseCible, self.portCible)

    def send(self, text):
        if self.thread.connecté:
            self.thread.send(text)
        else:
            self.thread = ClientThread(self.callback)

    def désactive(self):
        self.thread.désactive()
        self.thread = ClientThread(self.callback)


if __name__ == '__main__':
    Client().connect()
