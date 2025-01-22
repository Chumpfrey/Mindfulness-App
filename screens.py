import time

from kivy.clock import Clock

from kivy.core.window import Window 

from kivy.uix.boxlayout import BoxLayout    
from kivy.uix.button import Button     
from kivy.uix.label import Label
from kivy.uix.settings import MenuSidebar
from kivy.uix.settings import SettingsWithNoMenu
from kivy.uix.screenmanager import Screen    
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider

from popups import FileExplorerPopup
from custom_widgets import CalendarWidget

class Home(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Establish general layout of different widget in home
        home_layout = BoxLayout(orientation = "vertical", size_hint_y = None)
        home_layout.bind(minimum_height = home_layout.setter("height"))    # Dynamically adjust height
        
        # Add calendar to home
        calendar = CalendarWidget(size_hint_y = None, height = 500)
        home_layout.add_widget(calendar)
        
        home_layout.add_widget(Button(text = "Restart last session", size_hint_y = None, height = 100))
        home_layout.add_widget(Button(text = "Start next session", size_hint_y = None, height = 100))
        
        # Add scroll functionality to home page
        scroll = ScrollView(do_scroll_x = False)
        scroll.add_widget(home_layout)
        
        # Implement final view
        self.add_widget(scroll)
        

# The page that shows all possible sessions        
class Sessions(Screen):
    def __init__(self, screen_manager ,**kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        
        # All the possible sessions displayed
        sessions_layout = BoxLayout(orientation = "vertical", size_hint_y = None)
        sessions_layout.bind(minimum_height = sessions_layout.setter("height"))    # Dynamically adjust height
        
        # Button that navigates to each individual sessions
        sessions_layout.add_widget(Button(text = "Session 1", size_hint_y = None, height = 100, on_press = lambda x: self.switch_to(screen_name = "sesh1")))
        sessions_layout.add_widget(Button(text = "Session 2", size_hint_y = None, height = 100, on_press = lambda x: self.switch_to(screen_name = "sesh2")))
        sessions_layout.add_widget(Button(text = "Session 3", size_hint_y = None, height = 100, on_press = lambda x: self.switch_to(screen_name = "sesh3")))
        sessions_layout.add_widget(Button(text = "Session 4", size_hint_y = None, height = 100, on_press = lambda x: self.switch_to(screen_name = "sesh4")))
        
        # Screen only allows so many session buttons you can reasonably see
        # Adds scroll functionallity to help when session number increases
        scroll = ScrollView(do_scroll_x = False)
        scroll.add_widget(sessions_layout)
        
        self.add_widget(scroll)
        
    # Switch the current page displayed to whatever is specified
    def switch_to(self, screen_name):
        self.screen_manager.current = screen_name 
        
# Screen for users to create their own experience
class CustomSessions(Screen):
    def __init__(self, screen_manager, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        
        # All the possible sessions displayed
        sessions_layout = BoxLayout(orientation = "vertical", size_hint_y = None)
        sessions_layout.bind(minimum_height = sessions_layout.setter("height"))    # Dynamically adjust height
        
        # Add scroll functionality to home page
        scroll = ScrollView(do_scroll_x = False)
        scroll.add_widget(sessions_layout)
        
        # Implement final view
        self.add_widget(scroll)

# Screen for a specific, individual session in sessions page        
class Session(Screen):
    def __init__(self, voiceover = None, background_audio = None, duration = 600, alarm = None, **kwargs):
        super().__init__(**kwargs)
        session_layout = BoxLayout(orientation = "vertical")
        
        self.alarm = alarm
        self.duration = duration
        self.start_time = time.monotonic()
        self.end_time = self.start_time + self.duration
        self.background_audio = background_audio
        self.voiceover = voiceover
        self.label = Label(text = str(self.end_time - time.monotonic()))
        
        self.timer = self.label
        session_layout.add_widget(self.timer)
        
        self.add_widget(session_layout)
        
        self.schedule = None
       
    # Start the counter when entering the session page 
    def on_pre_enter(self):
        self.background_audio.play()
        self.start_time = time.monotonic()
        self.end_time = self.start_time + self.duration
        self.schedule = Clock.schedule_interval(self.update_timer, 1.0 / 60.0)
    
    # Stop the schedule that updates the timer label on leaving the page
    def on_pre_leave(self):
        self.schedule.cancel()
        self.background_audio.stop()
        self.alarm.stop()
    
    # Change the label text to the proper amount of time remaining
    def update_timer(self, dt):
        if time.monotonic() < self.end_time:
            self.timer.text = str(int(self.end_time - time.monotonic()))
        else:
            self.schedule.cancel()
            self.alarm.play()
            self.label.text = "Session completed."

# Standard settings page       
class Settings(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        sidebar_layout = BoxLayout(orientation = "vertical")
        self.sidebar = MenuSidebar()
        self.sidebar.remove_widget(self.sidebar.close_button)
        
        self.settings = SettingsWithNoMenu()
        
        sidebar_layout.add_widget(Button(text = "General"))
        sidebar_layout.add_widget(Button(text = "Alarm"))
        sidebar_layout.add_widget(Button(text = "Background Audio"))
        sidebar_layout.add_widget(Button(text = "Voiceover"))
        
        self.sidebar.add_widget(sidebar_layout)
        self.settings.add_widget(self.sidebar)
        self.add_widget(self.settings)
    
    def on_pre_enter(self, *args):
        popup = FileExplorerPopup()
        popup.get_popup().open()
        
        
class Sources(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text = "Citation"))