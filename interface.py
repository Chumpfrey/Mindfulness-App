import json

import time

from kivy.animation import Animation    

from kivy.app import App  

from kivy.config import ConfigParser

from kivy.core.audio import SoundLoader
from kivy.core.audio import Sound
from kivy.core.window import Window 

from kivy.uix.boxlayout import BoxLayout    
from kivy.uix.button import Button    
from kivy.uix.floatlayout import FloatLayout   
from kivy.uix.image import Image
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.screenmanager import ScreenManager

from screens import Home, Sessions, Session, CustomSessions, Sources, Settings

class GUILayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load alarm once instead of n times
        # n being the total number of sessions
        self.alarm = SoundLoader.load("aud\\alarms\\lofi-alarm-clock-243766.mp3")
        
        # Add all the primary pages we want to navigate to
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Home(name = "home"))
        self.screen_manager.add_widget(Sessions(name = "sessions", screen_manager = self.screen_manager))
        self.screen_manager.add_widget(CustomSessions(name = "custom_sessions", screen_manager = self.screen_manager))
        #self.screen_manager.add_widget(Settings(name = "settings"))
        self.screen_manager.add_widget(Sources(name = "sources"))
        
        # Load background audio
        sesh1_aud = SoundLoader.load("aud\\bgm\\calming-rain-257596.mp3")
        sesh1_aud.volume = 0.1
        
        # Specific session under sessions page
        self.screen_manager.add_widget(Session(name = "sesh1", duration = 10, alarm = self.alarm, background_audio = sesh1_aud))
        self.screen_manager.add_widget(Session(name = "sesh2", alarm = self.alarm))
        self.screen_manager.add_widget(Session(name = "sesh3", alarm = self.alarm))
        self.screen_manager.add_widget(Session(name = "sesh4", alarm = self.alarm))
        
        self.add_widget(self.screen_manager)
        
        # Side panel navigation options
        self.settings_btn = Button(text = "Settings", on_press = lambda x: self.open_settings())
        self.side_panel = BoxLayout(orientation = "vertical", size_hint = (0.3, 1), pos_hint = {"x": -1, "y": 0})
        self.side_panel.add_widget(Button(text = "Home", on_press = lambda x: self.switch_to("home")))
        self.side_panel.add_widget(Button(text = "Sessions", on_press = lambda x: self.switch_to("sessions")))
        self.side_panel.add_widget(Button(text = "Custom Sessions", on_press = lambda x: self.switch_to("custom_sessions")))
        self.side_panel.add_widget(self.settings_btn)
        self.side_panel.add_widget(Button(text = "Sources", on_press = lambda x: self.switch_to("sources")))
        
        self.add_widget(self.side_panel)
        
        # Hamburger menu button 
        self.menu_icon = Image(source = "imgs\Hamburger_icon.svg.png", size_hint = (0.1, 0.1), pos_hint = {"x": 0, "top": 1})    # Source img
        
        self.hamburger_menu = Button(text = "", size_hint = (0.1, 0.1), pos_hint = {"x": 0, "top": 1})
        self.hamburger_menu.bind(on_press = self.toggle_side_panel)
        
        self.add_widget(self.hamburger_menu)
        self.add_widget(self.menu_icon)
        
        # Panel state tracking
        self.panel_open = False
        
    def toggle_side_panel(self, instance):
        if self.panel_open:
            animation = Animation(pos_hint = {"x": -1, "y": 0}, duration = 0.3)    # Closing animation
            self.panel_open = False
        else:
            animation = Animation(pos_hint = {"x": 0, "y": 0}, duration = 0.3)    # Opening navigation
            self.panel_open = True
        animation.start(self.side_panel)
        
    def switch_to(self, screen_name):
        self.screen_manager.current = screen_name    # Switch the current page to the specified page
        self.toggle_side_panel(None)    # Close the side navigation panel

# Primary way to interact with the app
class GUI(App):
    def build(self):  
        self.settings_cls = SettingsWithSidebar
        
        layout = GUILayout() 
        layout.settings_btn.bind(on_press = lambda x: self.open_settings())
        return layout
    
    def build_config(self, config):
        config.setdefaults("Sound", {
            "key1": "1",
            "key2": "24",
            "key3": "Dark"
        })
        config.setdefaults("Graphics", {
            "key4": "Hello",
            "key5": "/"
        })
    
    def build_settings(self, settings):
        settings.add_json_panel("General", self.config, "settings.json")
        
    def on_config_change(self, config, section, key, value):
        self.config.write()

# Launch the app
if __name__ == "__main__":
    GUI().run()