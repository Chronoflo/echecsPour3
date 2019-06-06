import json
from random import randint

import kivy
from kivy.app import App
from kivy.config import ConfigParser
from kivy.lang import Builder
from kivy.properties import NumericProperty, ReferenceListProperty, Clock, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.settings import Settings, SettingsWithSidebar
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.vector import Vector

with open('kv/demarrage.kv', encoding='utf-8') as f:
    Builder.load_string(f.read())


def lance_partie(n_joueurs):
    print("Partie lancée pour {} joueurs.".format(n_joueurs))

class MyScreenManager(ScreenManager):
    pass


class MainScreen(Screen):
    settings_popup = ObjectProperty(None, allownone=True)


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
    def __init__(self, lance_partie):
        super(DemarrageApp, self).__init__()
        self.use_kivy_settings = False
        self.settings_cls = SettingsWithSidebar
        self.lance_partie = lance_partie

    def build(self):
        return MyScreenManager()

    def build_config(self, config: ConfigParser):
        config.read("demarrage.ini")

    def build_settings(self, settings: Settings):
        pages = ("Jeu", "Graphique", "Réseau", "Autre")

        for page in pages:
            with open("json/{}.json".format(page), encoding='utf-8') as f:
                settings.add_json_panel(page, self.config, data=f.read())

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
