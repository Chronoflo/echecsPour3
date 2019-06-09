from kivy.config import Config

from reseau import Serveur, Client

Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.app import App
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty, ReferenceListProperty, Clock, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.settings import Settings, SettingsWithSidebar
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

with open('kv/demarrage.kv', encoding='utf-8') as f:
    Builder.load_string(f.read())


def lance_partie(n_joueurs):
    print("Partie lancée pour {} joueurs.".format(n_joueurs))


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.last = self.current

    def to_last(self):
        self.current = self.last

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        app: DemarrageApp = App.get_running_app()
        keyname = keycode[1]

        print(keyname)
        if keyname == 'escape' or keyname == 'backspace':
            if not app.settings_open:
                if self.current != 'main':
                    self.current = 'main'
                elif keyname == 'escape':
                    quit()
            else:
                app.close_settings()
        elif keyname == 'p':
            if not app.settings_open:
                app.open_settings()
            else:
                app.close_settings()
        elif keyname == 'm':
            self.current = 'multiplayer'
        return True

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None


class MainScreen(Screen):
    settings_popup = ObjectProperty(None, allownone=True)


class MouseEvents(Widget):
    def __init__(self, **kwargs):
        super(MouseEvents, self).__init__(**kwargs)
        self.right_click = None

    def on_touch_down(self, touch):
        super(MouseEvents, self).on_touch_down(touch)
        if touch.button == 'right' and self.right_click is not None:
            self.right_click()


class NumericalInput(TextInput):
    maxLength = NumericProperty(15)

    def insert_text(self, substring, from_undo=False):
        modified = "".join([char for char in substring if char in ".0123456789"])
        if len(self.text) + len(modified) <= self.maxLength:
            super(NumericalInput, self).insert_text(modified, from_undo=from_undo)


class Chat(BoxLayout):
    test = NumericProperty(2)


class ChatTextInput(TextInput):
    pass


class MessageHistoric(Label):
    def add(self, line):
        self.text = self.text + "\n" + line


class SuperSettings(Popup):
    def __init__(self):
        super(SuperSettings, self).__init__()
        self.s = SettingsWithSidebar()
        
    def build(self):
        self.add_widget(self.s)
        return self

    def add_json_panel(self, title, config, data):
        self.s.add_json_panel(title, config, data=data)


class DemarrageApp(App):
    messagesHistoric = ObjectProperty(None)

    def __init__(self, lance_partie):
        super(DemarrageApp, self).__init__()
        self.use_kivy_settings = False
        self.settings_cls = SettingsWithSidebar
        self.settings_open = False
        self.serveur = Serveur(self.on_received)
        self.client = Client(self.on_received)
        self.lance_partie = lance_partie

    def send(self, text):
        if self.serveur.estActivé():
            self.serveur.broadcast(text)
        elif self.client.connecté:
            self.client.send(text)

    def on_received(self, msg):
        if self.messagesHistoric is not None:
            self.messagesHistoric.add(msg)

    def serveur_to_client(self):
        self.serveur.désactive()
        try:
            self.client.connect()
            self.client.send("*Connexion de {}*".format(self.config.get('gameplay', 'profile')))
            self.messagesHistoric.add("*Connecté*")
        except:
            print("Échec")

    def build(self):
        return MyScreenManager()

    def build_config(self, config: ConfigParser):
        config.read("demarrage.ini")

    def build_settings(self, settings: Settings):
        pages = ("Jeu", "Graphique", "Réseau", "Autre")

        for page in pages:
            with open("json/{}.json".format(page), encoding='utf-8') as f:
                settings.add_json_panel(page, self.config, data=f.read())

    def open_settings(self, *largs):
        super(DemarrageApp, self).open_settings(*largs)
        self.settings_open = True

    def close_settings(self, *largs):
        super(DemarrageApp, self).close_settings(*largs)
        self.settings_open = False

    def on_config_change(self, config, section, key, value):
        self.applique_parametres()

    def on_start(self):
        """ Appelé une fois que la fenêtre a été affichée. """
        self.applique_parametres()

    def applique_parametres(self):
        if self.config.get('graphics', 'fullscreen') == '1':
            self.root_window.fullscreen = 'auto'
        else:
            self.root_window.fullscreen = False


if __name__ == '__main__':
    DemarrageApp(lance_partie).run()
