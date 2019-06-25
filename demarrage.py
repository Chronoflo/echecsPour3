import os
import random
import threading
from math import pi, cos, sin

from kivy.clock import Clock
from kivy.config import Config
from kivy.metrics import dp, cm
from kivy.uix.behaviors import CoverBehavior
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.video import Video

from Interface import affichage
from reseau.reseau import Serveur, Client
from fonctions import rand_sign

Config.set('input', 'mouse', 'mouse,disable_multitouch')
from kivy.app import App
from kivy.config import ConfigParser
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty, ListProperty, \
    BooleanProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.settings import Settings, SettingsWithSidebar, SettingItem, SettingSpacer, SettingOptions
import kivy.uix.settings
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
import kivy
from kivy.core.audio import SoundLoader
sound = SoundLoader.load("video/poney.mp3")
if sound:
    print(sound)
    print("Sound found at %s" % sound.source)
    print("Sound is %.3f seconds" % sound.length)
    sound.play()
kivy.uix.settings.__all__ += tuple("SettingSuperOptions")

with open('kv/demarrage.kv', encoding='utf-8') as f:
    Builder.load_string(f.read())


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

        # print(keyname)
        if keyname == 'escape' or keyname == 'backspace':
            if not app.settings_open:
                if self.current != 'main':
                    self.current = 'main'
                elif keyname == 'escape':
                    app.stop()
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


# class SuperVideo(RelativeLayout):
#     video = ObjectProperty(None, allownone=True)
#     video = Video()
#     video.opacity
#     video.bind(loaded=self.on_loaded)
#     def


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


class DanceAvecLesBouttons(Button):
    theta_i = NumericProperty()
    vitesse_i = NumericProperty()
    rayon = NumericProperty()
    pulsation = NumericProperty()

    def oscille(self, dt):
        root = App.get_running_app().root
        self.t += dt
        sommet = root.width / 2, root.height * 0.8
        theta = self.theta_i * cos(self.pulsation * self.t) + self.vitesse_i * sin(self.pulsation * self.t)
        pos = self.pos
        self.pos = sommet[0] + self.rayon * sin(theta) - self.width / 2,\
                   sommet[1] - self.rayon * cos(theta) - self.height / 2

    def __init__(self, *trucs, **autres_trucs):
        super(DanceAvecLesBouttons, self).__init__()
        self.t = 0
        self.theta_i = rand_sign() * (random.random() * .2 + .2)
        Clock.schedule_interval(self.oscille, 0)


class SettingSuperOptions(SettingOptions):
    addPopup = ObjectProperty(None, allownone=True)
    hasNewOption = BooleanProperty(False)

    def _create_add_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.80 * Window.width, dp(300))
        self.addPopup = popup = Popup(
            content=content, title='Ajouter', size_hint=(None, None), size=(popup_width, '95dp'))
        textInput = TextInput(multiline=False, hint_text='nom')

        def on_validate():
            newProfileOptions = App.get_running_app().newProfileOptions
            if textInput.text:
                self.options.append(textInput.text)
                self.value = textInput.text
                newProfileOptions.append(textInput.text)
                self._update_popup()
                popup.dismiss()

        textInput.on_text_validate = on_validate
        textInput.height = textInput.minimum_height
        content.add_widget(textInput)

        popup.open()
        textInput.focus = True

    def _create_popup(self, instance):
        # crée la popup
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            content=content, title=self.title, size_hint=(None, None),
            size=(popup_width, '400dp'))
        popup.height = len(self.options) * dp(55) + dp(150)

        # ajoute toutes les options
        content.add_widget(Widget(size_hint_y=None, height=1))
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid)
            btn.bind(on_release=self._set_option)
            content.add_widget(btn)

        content.add_widget(SettingSpacer())

        add_btn = Button(text='Ajouter', size_hint_y=None, height=dp(50))
        add_btn.bind(on_release=self._create_add_popup)
        cancel_btn = Button(text='Annuler', size_hint_y=None, height=dp(50))
        cancel_btn.bind(on_release=popup.dismiss)
        content.add_widget(add_btn)
        content.add_widget(cancel_btn)

        # and open the popup !
        popup.open()

    def _update_popup(self):
        content, popup = self.popup.content, self.popup

        content.clear_widgets()
        popup.height = len(self.options) * dp(55) + dp(150)
        uid = str(self.uid)
        for option in self.options:
            state = 'down' if option == self.value else 'normal'
            btn = ToggleButton(text=option, state=state, group=uid)
            btn.bind(on_release=self._set_option)
            content.add_widget(btn)

        content.add_widget(SettingSpacer())
        add_btn = Button(text='Ajouter', size_hint_y=None, height=dp(50))
        add_btn.bind(on_release=self._create_add_popup)
        cancel_btn = Button(text='Annuler', size_hint_y=None, height=dp(50))
        cancel_btn.bind(on_release=self.popup.dismiss)
        content.add_widget(add_btn)
        content.add_widget(cancel_btn)


class DemarrageApp(App):
    messagesHistoric = ObjectProperty(None)
    newProfileOptions = ListProperty([])
    player = StringProperty()
    numéroJoueur = NumericProperty(0)
    otherPlayers = ListProperty(['Vide', 'Vide'])
    applicationJeu = ObjectProperty(affichage)

    def __init__(self):
        super(DemarrageApp, self).__init__()
        self.use_kivy_settings = False
        self.settings_cls = SettingsWithSidebar
        self.settings_open = False
        self.serveur = Serveur(self.on_received, self.on_external_connection)
        self.client = Client(self.on_received)

        self.jeu = None
        self.plateau = None
        self.listeJoueurs = None

    def créer_partie(self, joueurs=()):

        if self.jeu is None or not self.jeu.is_alive():
            if len(joueurs) == 0:
                self.jeu = threading.Thread(daemon=True, target=affichage, args=(self.player, self.player, *self.otherPlayers,
                                                                                 self.sur_déplacement_pièce, self.sur_attente_autres_joueurs),
                                            kwargs={'siege_chaud': False})
                self.send("c: {};{};{}".format(self.player, *self.otherPlayers))
            else:
                self.jeu = threading.Thread(daemon=True, target=affichage, args=(self.player, *joueurs, self.sur_déplacement_pièce, self.sur_attente_autres_joueurs),
                                            kwargs={'siege_chaud': False})
            self.jeu.start()

    def siege_chaud(self):
        if self.jeu is None or not self.jeu.is_alive():
            self.jeu = threading.Thread(daemon=True, target=affichage,
                                        args=(self.player, self.player, "Joueur vert", "Joueur bleu"),
                                        kwargs={'siege_chaud': True})
            self.jeu.start()

    def partie_solo(self):
        if self.jeu is None or not self.jeu.is_alive():
            self.jeu = threading.Thread(daemon=True, target=affichage,
                                        args=(self.player, self.player, "IA", "IA 2"),
                                        kwargs={'siege_chaud': False})
            self.jeu.start()

    def ajouter_IA(self):
        if self.otherPlayers[0] == 'Vide':
            self.otherPlayers[0] = 'IA'
        elif self.otherPlayers[1] == 'Vide':
            self.otherPlayers[1] = 'IA 2'

    def sur_déplacement_pièce(self, pos_piece, pos_cible):
        self.send("g: {};{}".format(pos_piece, pos_cible))

    def sur_attente_autres_joueurs(self, plateau, listeJoueurs):
        self.plateau = plateau
        self.listeJoueurs = listeJoueurs

    def send_msg(self, text):
        self.send("m: " + "[i]" + self.player + "[/i]: " + text)

    def send(self, text):
        if self.serveur.estActivé() or self.client.estConnecté():
            print("Envoyé {}".format(" | ".join(text.split("\b"))))
        if self.serveur.estActivé():
            self.serveur.broadcast(text)
        elif self.client.estConnecté():
            self.client.send(text)

    def on_external_connection(self):
        self.send("p: " + ", ".join([self.config.get('gameplay', 'profile')] + self.otherPlayers))

    def on_received(self, text):
        id, contenu = text[0], text[3:]
        if id == 'm':
            if self.messagesHistoric is not None:
                self.messagesHistoric.add(contenu)
        elif id == 'p':
            joueurs = [joueur for joueur in contenu.split(', ') if joueur != self.player]
            if len(joueurs) == 1:
                for i in range(2):
                    if self.otherPlayers[i] == 'Vide':
                        self.otherPlayers[i] = joueurs[0]
                        break
            elif len(joueurs):
                if self.otherPlayers[0] == 'Vide':
                    self.otherPlayers[0] = joueurs[0]
                if len(joueurs) >= 2:
                    self.otherPlayers[1] = joueurs[1]
            else:
                if contenu == self.player:
                    print("Ce profil est déjà utilisé.")
                else:
                    raise ValueError("Un message de profils doit contenir au moins un profil.")
        elif id == 'd':
            joueur = contenu
            self.otherPlayers[self.otherPlayers.index(joueur)] = 'Vide'
        elif id == 'c':
            self.créer_partie(contenu.split(";"))
        elif id == 'g':
            if self.plateau is not None:
                self.plateau.sur_déplacement_validé(*[[int(i) for i in str_couple[1:-1].split(', ')] for str_couple in contenu.split(";")])
            if self.listeJoueurs is not None:
                self.listeJoueurs.joueur_suivant()

    def serveur_to_client(self):
        self.serveur.désactive()
        try:
            self.client.connect()
            self.client.send("m: *Connexion de {}*".format(self.player))
            self.client.send("p: {}".format(self.player))
            self.messagesHistoric.add("*Connecté*")
        except ValueError:
            print("Échec")

    def build(self):
        return MyScreenManager()

    def build_config(self, config: ConfigParser):
        if os.path.isfile('demarrage.ini'):
            config.read("demarrage.ini")
        else:
            config.read('default.ini')
        self.player = config.get('gameplay', 'profile')

    def build_settings(self, settings: Settings):
        settings.register_type("superoptions", SettingSuperOptions)
        pages = ("Jeu", "Graphique", "Réseau", "Autre")

        for page in pages:
            file_path = "json/{}.json".format(page)
            if not os.path.isfile(file_path):
                file_path = "json/default_{}.json".format(page)

            with open(file_path, encoding='utf-8') as f:
                settings.add_json_panel(page, self.config, data=f.read())

    def open_settings(self, *largs):
        super(DemarrageApp, self).open_settings(*largs)
        self.settings_open = True

    def close_settings(self, *largs):
        super(DemarrageApp, self).close_settings(*largs)
        self.settings_open = False

    def on_config_change(self, config, section, key, value):
        self.player = config.get('gameplay', 'profile')
        self.applique_parametres()

    def on_start(self):
        """ Appelé une fois que la fenêtre a été affichée. """
        self.applique_parametres()

    def on_stop(self):
        self.send("m: *{p} s'est déconnecté*\bd: {p}".format(p=self.player))
        threading.Timer(1, self.serveur.désactive)
        threading.Timer(1, self.client.désactive)

        if self.newProfileOptions:
            res = ""
            file_path = "json/Jeu.json"
            if not os.path.isfile(file_path):
                file_path = "json/default_Jeu.json"

            with open(file_path, encoding='utf-8') as f:
                for line in f:
                    if line.strip()[:9] == '"options"':
                        res += '        "options": {}],\n'.format(
                            line[19:-3] + ', ' + ", ".join(['"' + name + '"' for name in self.newProfileOptions]))
                    else:
                        res += line
            self.newProfileOptions = []

            with open('json/Jeu.json', 'w', encoding='utf-8') as f:
                f.write(res)

    def applique_parametres(self):
        if self.config.get('graphics', 'fullscreen') == '1':
            self.root_window.fullscreen = 'auto'
        else:
            self.root_window.fullscreen = False


if __name__ == '__main__':
    DemarrageApp().run()
