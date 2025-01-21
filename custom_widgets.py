import calendar

from datetime import datetime

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

class CalendarWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation = "vertical", **kwargs)
        
        # Calendar header
        self.header = BoxLayout(size_hint_y = 0.2)
        self.add_widget(self.header)
        
        # Get the current year and month
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        
        self.month_label = Label(text = f"{calendar.month_name[self.current_month]} {self.current_year}")
        self.header.add_widget(Button(text = "<", on_press = self.previous_month))
        self.header.add_widget(self.month_label)
        self.header.add_widget(Button(text = ">", on_press = self.next_month))
        
        self.days_grid = GridLayout(cols = 7, size_hint_y = 0.1)
        
        for day in calendar.day_abbr:
            self.days_grid.add_widget(Label(text = day))
        self.add_widget(self.days_grid)
        
        self.dates_grid = GridLayout(cols = 7)
        self.add_widget(self.dates_grid)
        
        self.update_calendar()
        
    def update_calendar(self):
        self.dates_grid.clear_widgets()
        month_calendar = calendar.monthcalendar(self.current_year, self.current_month)
        
        for week in month_calendar:
            for day in week:
                if day == 0:
                    self.dates_grid.add_widget(Label())
                else:
                    self.dates_grid.add_widget(Label(text = str(day)))
            
    # Update month, year and its corresponding label for the previous month        
    def previous_month(self, instance):
        self.current_month -= 1
        
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
            
        self.month_label.text = f"{calendar.month_name[self.current_month]} {self.current_year}"
        self.update_calendar()

    # Update month, year and its corresponding label for the next month
    def next_month(self, instance):
        self.current_month += 1
        
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
            
        self.month_label.text = f"{calendar.month_name[self.current_month]} {self.current_year}"
        self.update_calendar()
        