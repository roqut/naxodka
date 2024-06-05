from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle


class EmptyWidget(Widget):
    pass

class RoundedButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create a rounded rectangle for the button
        with self.canvas.before:
            Color(0.3804, 0.3020, 0.8667, 1)  # white color
            self.rounded_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[5, 5, 5, 5])
        self.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
        
    def update_rounded_rect(self, instance, value):
        self.rounded_rect.pos = instance.pos
        self.rounded_rect.size = instance.size

class EntitySelector(Screen):
    def __init__(self, **kwargs):
        super(EntitySelector, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.background_image = Image(source='images/under.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background_image)

        label = Label(text='НАХОДКА', font_size=50, font_name='OpenSans', size_hint_y=0.3)
        layout.add_widget(EmptyWidget(size_hint_y=0.3))
        layout.add_widget(label)

        #первый layout с кнопкой для общего с кнопками
        button_layout_1 = BoxLayout(orientation='horizontal', size_hint_y=0.05)
        button1 = RoundedButton(text='ОРГАНИЗАЦИЯ', font_size=25, size_hint_x=0.8, font_name='OpenSans',
                         halign='left', color=(1, 1, 1, 1),
                         background_color=(0, 0, 0, 0), background_normal='')

        button1.bind(on_press=self.navigate_to_org)

        button_layout_1.add_widget(EmptyWidget(size_hint_x=0.1))
        button_layout_1.add_widget(button1)
        button_layout_1.add_widget(EmptyWidget(size_hint_x=0.1))

        #второй layout с кнопкой для общего с кнопками
        button_layout_2 = BoxLayout(orientation='horizontal', size_hint_y=0.05)
        button2 = RoundedButton(text='ПОЛЬЗОВАТЕЛЬ', font_size=25, size_hint_x=0.8, font_name='OpenSans', 
                         halign='left', color=(1, 1, 1, 1),
                         background_color=(0, 0, 0, 0), background_normal='')
        button2.bind(on_press=self.navigate_to_user)

        button_layout_2.add_widget(EmptyWidget(size_hint_x=0.1))
        button_layout_2.add_widget(button2)
        button_layout_2.add_widget(EmptyWidget(size_hint_x=0.1))
        
        #общий layout с кнопками
        buttons_layout = BoxLayout(orientation='vertical')
        buttons_layout.add_widget(EmptyWidget(size_hint_y=0.14))
        buttons_layout.add_widget(button_layout_1)
        buttons_layout.add_widget(EmptyWidget(size_hint_y=0.03))
        buttons_layout.add_widget(button_layout_2)
        buttons_layout.add_widget(EmptyWidget(size_hint_y=0.13))
        layout.add_widget(buttons_layout)

        

        self.add_widget(layout)

    def navigate_to_org(self, *args):
        self.manager.current = 'LoginSelector'
    
    def navigate_to_user(self, *args):
        self.manager.current = 'ChooseOrg'
