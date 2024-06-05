# loading_screen.py
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget

class EmptyWidget(Widget):
    pass

class Loading(Screen):

    def on_enter(self):
        self.create_layout()
        Clock.schedule_once(self.navigate_to_hub_screen, 3)


    def create_layout(self):
        layout = BoxLayout(orientation='vertical')
        self.background_image = Image(source='images/grad2.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background_image)

        layout = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.label = Label(text='НАХОДКА', font_size=50, font_name='OpenSans', size_hint_y=0.6)
        layout.add_widget(self.label)
        layout.add_widget(EmptyWidget(size_hint_y=0.4))
        
        self.add_widget(layout)


    def navigate_to_hub_screen(self, *args):
        self.manager.current = 'EntitySelector'