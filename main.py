from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
import webbrowser
import datetime

# Fondo Estilo PS5 Premium
Window.clearcolor = get_color_from_hex('#00050a')

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        layout.add_widget(Label(text='OJEDA STATION', font_size='55sp', bold=True, color=get_color_from_hex('#0088FF')))
        layout.add_widget(Label(text='VERSION ELITE V.10.5', font_size='16sp', color=get_color_from_hex('#555555')))
        
        btn_start = Button(text='INICIAR SESIÓN', size_hint=(None, None), size=(350, 110),
                          pos_hint={'center_x': 0.5}, background_normal='',
                          background_color=get_color_from_hex('#00439c'), font_size='22sp', bold=True)
        btn_start.bind(on_press=lambda x: setattr(self.manager, 'current', 'main_os'))
        layout.add_widget(btn_start)
        self.add_widget(layout)

class OjedaStationOS(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        main_layout = BoxLayout(orientation='vertical')

        # --- BARRA SUPERIOR DINÁMICA ---
        self.top_bar = BoxLayout(size_hint_y=None, height=70, padding=[20, 10])
        self.time_label = Label(text="", bold=True, font_size='18sp', color=get_color_from_hex('#00CCFF'))
        self.top_bar.add_widget(self.time_label)
        main_layout.add_widget(self.top_bar)
        Clock.schedule_interval(self.update_time, 1)

        # --- CONTENEDOR DE APPS (SCROLL) ---
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        content = GridLayout(cols=1, spacing=12, padding=[25, 10, 25, 50], size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # --- CATEGORÍA: JUEGOS AAA ---
        self.add_sec(content, "BIBLIOTECA DE JUEGOS", '#ff9f1c')
        juegos = [
            ("ROBLOX", "com.roblox.client"), ("FREE FIRE", "com.dts.freefireth"),
            ("MINECRAFT", "com.mojang.minecraftpe"), ("COD MOBILE", "com.activision.callofduty.shooter"),
            ("BRAWL STARS", "com.supercell.brawlstars"), ("CLASH ROYALE", "com.supercell.clashroyale"),
            ("GENSHIN IMPACT", "com.miHoYo.GenshinImpact"), ("POKEMON GO", "com.nianticlabs.pokemongo"),
            ("PUBG MOBILE", "com.tencent.ig"), ("STUMBLE GUYS", "com.kitkagames.fallbuddy")
        ]
        for name, pkg in juegos:
            self.add_btn(content, name, '#111111', f"https://play.google.com/store/apps/details?id={pkg}", True)

        # --- CATEGORÍA: MULTIMEDIA ---
        self.add_sec(content, "CENTRO MULTIMEDIA", '#e63946')
        media = [
            ("YOUTUBE", '#FF0000', "https://www.youtube.com"), ("NETFLIX", '#E50914', "https://www.netflix.com"),
            ("SPOTIFY", '#1DB954', "https://open.spotify.com"), ("TWITCH", '#9146FF', "https://www.twitch.tv"),
            ("DISNEY+", '#006E99', "https://www.disneyplus.com"), ("PRIME VIDEO", '#00A8E1', "https://www.primevideo.com"),
            ("HBO MAX", '#5822b4', "https://www.hbomax.com"), ("CRUNCHYROLL", '#f47521', "https://www.crunchyroll.com")
        ]
        for name, col, url in media:
            self.add_btn(content, name, col, url)

        # --- CATEGORÍA: REDES SOCIALES ---
        self.add_sec(content, "COMUNIDAD Y REDES", '#4361ee')
        social = [
            ("DISCORD", '#5865F2', "https://discord.com"), ("WHATSAPP", '#25D366', "https://web.whatsapp.com"),
            ("INSTAGRAM", '#E1306C', "https://www.instagram.com"), ("TIKTOK", '#000000', "https://www.tiktok.com"),
            ("REDDIT", '#FF4500', "https://www.reddit.com"), ("X / TWITTER", '#0f1419', "https://x.com"),
            ("TELEGRAM", '#24A1DE', "https://web.telegram.org"), ("PINTEREST", '#E60023', "https://www.pinterest.com")
        ]
        for name, col, url in social:
            self.add_btn(content, name, col, url)

        # --- CATEGORÍA: HERRAMIENTAS Y SISTEMA ---
        self.add_sec(content, "HERRAMIENTAS DE SISTEMA", '#8d99ae')
        tools = [
            ("GOOGLE CHROME", '#4285F4', "https://www.google.com"), ("PLAY STORE", '#003566', "https://play.google.com/store"),
            ("GOOGLE MAPS", '#34A853', "https://maps.google.com"), ("CALCULADORA", '#333333', "https://www.google.com/search?q=calculadora"),
            ("TRADUCTOR", '#4285F4', "https://translate.google.com"), ("WIKIPEDIA", '#FFFFFF', "https://www.wikipedia.org"),
            ("SOPORTE OJEDA", '#0088FF', "https://support.google.com"), ("AJUSTES CUENTA", '#555555', "https://myaccount.google.com")
        ]
        for name, col, url in tools:
            self.add_btn(content, name, col, url)

        # BOTÓN DE APAGADO
        btn_off = Button(text="APAGAR ESTACIÓN", size_hint_y=None, height=120, background_color=get_color_from_hex('#780000'), bold=True)
        btn_off.bind(on_press=App.get_running_app().stop)
        content.add_widget(btn_off)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def update_time(self, *args):
        self.time_label.text = f"OJEDA OS | {datetime.datetime.now().strftime('%H:%M:%S')}"

    def add_sec(self, layout, text, col):
        layout.add_widget(Label(text=text, font_size='22sp', bold=True, color=get_color_from_hex(col), size_hint_y=None, height=90))

    def add_btn(self, layout, text, col, url, is_game=False):
        btn = Button(text=f"LAUNCH: {text}" if is_game else text, size_hint_y=None, height=115,
                    background_normal='', background_color=get_color_from_hex(col),
                    color=(0,0,0,1) if col == '#FFFFFF' else (1,1,1,1), font_size='18sp', bold=True)
        btn.bind(on_press=lambda x: webbrowser.open(url))
        layout.add_widget(btn)

class OjedaApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(OjedaStationOS(name='main_os'))
        return sm

if __name__ == '__main__':
    OjedaApp().run()
  
