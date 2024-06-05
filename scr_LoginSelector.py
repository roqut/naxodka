from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle
from db import Database
import constants

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

class ClickableLabel(ButtonBehavior, Label):
    def __init__(self, **kwargs):
        super(ClickableLabel, self).__init__(**kwargs)
        self.normal_color = (1, 1, 1, 1)  # default color
        self.hover_color = (0.8, 0.8, 0.8, 1)  # hover color

class LoginSelector(Screen):
    def __init__(self, **kwargs):
        super(LoginSelector, self).__init__(**kwargs)
        self.build_ui()

    def build_ui(self):
        layout = BoxLayout(orientation='vertical')

        self.background_image = Image(source='images/upper2.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background_image)

        label = Label(text='        ВХОД В \nОРГАНИЗАЦИЮ', font_size=40, font_name='OpenSans', size_hint_y=0.55)
        layout.add_widget(label)

        center_layout = BoxLayout(orientation='vertical', size_hint_x=0.72)

        label_login = Label(text='Логин:', font_size=20, font_name='OpenSans',
                             size_hint_y=0.08, halign='left', padding=(30, 55, 0, 0))
        label_login.bind(width=self.update_text_size)
        self.input_login = TextInput(size_hint_y=0.03, font_size=20, multiline=False)
        self.input_login.padding = (self.input_login.width*0.15, self.input_login.height*0.08, 0.0, 0.0)

        label_pass = Label(text='Пароль:', font_size=20, font_name='OpenSans', 
                           size_hint_y=0.055, halign='left', padding=(30, 25, 0, 0))
        label_pass.bind(width=self.update_text_size)
        self.input_pass = TextInput(size_hint_y=0.03, font_size=20, multiline=False)
        self.input_pass.padding = (self.input_pass.width*0.15, self.input_pass.height*0.08, 0.0, 0.0)

        button_to_admin = RoundedButton(text='Вход                   --->', font_size=25, 
                         halign='left', padding=(30, 0, 0, 0), size_hint_y=0.04, color=(1, 1, 1, 1),
                         background_color=(0, 0, 0, 0), background_normal='')
        button_to_admin.bind(on_press=self.auth_admins)
        button_to_admin.bind(width=self.update_text_size)
        

        button_to_reg_org = ClickableLabel(text='Регистрация', font_size=16, padding=(25, 0, 0, 30), 
                         size_hint_y=0.07, halign='left', underline=True)
        button_to_reg_org.bind(width=self.update_text_size)
        button_to_reg_org.bind(on_press=self.navigate_to_reg_org)

        center_layout.add_widget(EmptyWidget(size_hint_y=0.04))
        center_layout.add_widget(label_login)
        center_layout.add_widget(self.input_login)
        center_layout.add_widget(label_pass)
        center_layout.add_widget(self.input_pass)
        center_layout.add_widget(EmptyWidget(size_hint_y=0.03))
        center_layout.add_widget(button_to_admin)
        center_layout.add_widget(button_to_reg_org)

        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.14)
        back_button = Button(text='<---', size_hint_y=0.1, font_size=25, 
                                      background_color=(0, 0, 0, 0), 
                                      padding=(10, 0, 0, 10))
        back_button.bind(on_press=self.back_to_select_entity)
        left_layout.add_widget(EmptyWidget(size_hint_y=0.9))
        left_layout.add_widget(back_button)

        under_layout = BoxLayout(orientation='horizontal')
        under_layout.add_widget(left_layout)
        under_layout.add_widget(center_layout)
        under_layout.add_widget(EmptyWidget(size_hint_x=0.14))
        layout.add_widget(under_layout)

        self.add_widget(layout)

    def auth_admins(self, *args):
        self.db = Database("safu", "auth_for_admin", "error")
        query = "SELECT login, password FROM safu_admins_auth"
        rows = self.db.fetch_all(query)
        self.db.close()
        
        if (self.input_login.text, self.input_pass.text) in rows:
            constants.what_admin=self.input_login.text
            
            self.manager.current = 'AdminMain'
        else:
            print('error')

    def update_text_size(self, instance: Widget, value: float)-> None:
        instance.text_size = (instance.width, None)

    def navigate_to_reg_org(self, *args) -> None:
        self.manager.current = 'Registration'
    
    def back_to_select_entity(self, *args) -> None:
        self.manager.current = 'EntitySelector'