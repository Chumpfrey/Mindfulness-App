from kivy.core.window import Window 

from kivy.uix.boxlayout import BoxLayout    
from kivy.uix.button import Button    
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup

class FileExplorerPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.file_explorer = FileChooserListView()
        self.selection = None
        
        layout = BoxLayout(orientation = "vertical")
        
        button_layout = BoxLayout(orientation = "horizontal")
        
        layout.add_widget(self.file_explorer)
        button_layout.add_widget(Button(text = "Close", 
                                        size_hint_y = 0.2, 
                                        on_press = lambda x: self.popup.dismiss()))
        button_layout.add_widget(Button(text = "Confirm",
                                        size_hint_y = 0.2,
                                        on_press = lambda x: self.explorer_confirm()))
        layout.add_widget(button_layout)
        
        self.popup = Popup(title = "File Explorer",
                      content = layout,
                      size_hint = (0.5, 0.75),
                      size = (400, 400),
                      pos_hint = {"x": 0.25, "y": 0.1})
        
    def explorer_confirm(self):
        self.selection = self.file_explorer.selection
        print(self.selection)
        self.popup.dismiss()
       
    def get_popup(self):
        return self.popup