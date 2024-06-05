# scr_ChooseOrg.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import SpinnerOption
from kivy.uix.spinner import Spinner
import constants
from db import Database
list_organizations = ['Северный (Арктический) Федеральный Университет', 
                      'Северный Государственный Медицинский Университет', 
                      'Гумрф Арктический морской институт имени В. И. Воронина']

class EmptyWidget(Widget):
    pass

class SpinnerOptionWithWrap(SpinnerOption):
    def __init__(self, **kwargs):
        super(SpinnerOptionWithWrap, self).__init__(**kwargs)
        self.text_size = (300, None)  # фиксированная ширина текста
        self.rect = None  # атрибут для хранения ссылки на Rectangle
        self.color = (0, 0, 0, 1)
        self.background_color = (0, 0, 0, 0)
        
        with self.canvas.before:
            Color(1, 1, 1, 1)  # белый цвет фона
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        if self.rect:
            self.canvas.before.remove(self.rect)  # удаление старого Rectangle
        self.rect = RoundedRectangle(size=(instance.size[0], instance.size[1]-10), pos=(instance.pos[0], instance.pos[1]+5), radius=(5, 5, 5, 5))
        self.canvas.before.add(self.rect)  # добавление нового Rectangle
    
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

class ChooseOrg(Screen):
    def __init__(self, **kwargs):
        super(ChooseOrg, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.background_image = Image(source='images/under.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background_image)

        self.list_organizations = self.import_organizations()

        label = Label(text='НАХОДКА', font_size=50, font_name='OpenSans', size_hint_y=0.3)
        layout.add_widget(label)
        layout.add_widget(EmptyWidget(size_hint_y=0.2))

        # layout со списком
        add_layout_1 = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        self.list_org = Spinner(text='Выберите организацию', font_size=20, font_name='OpenSans', 
                                size_hint_x=0.7, background_color=(0, 0, 0, 0), halign='center')
        self.list_org.values = set([org[1] for org in self.list_organizations])
        self.list_org.option_cls = SpinnerOptionWithWrap
        self.list_org.text_size = (300, None)
        with self.list_org.canvas.before:
            Color(0, 0, 0, 1)
            rect = RoundedRectangle(size=(self.list_org.size[0], self.list_org.size[1]-10),
                                          pos=(self.list_org.pos[0], self.list_org.pos[1]+5), radius=(10, 10, 10, 10))
        def update_rect(instance, value):
            rect.pos = instance.pos
            rect.size = instance.size
        self.list_org.bind(pos=update_rect, size=update_rect)

        add_layout_1.add_widget(EmptyWidget(size_hint_x=0.15))
        add_layout_1.add_widget(self.list_org)
        add_layout_1.add_widget(EmptyWidget(size_hint_x=0.15))
        layout.add_widget(add_layout_1)
        
        # layout с кнопкой
        add_layout_2 = BoxLayout(orientation='horizontal', size_hint_y=0.05)
        button_search = RoundedButton(text='НАЙТИ', font_size=25, size_hint_x=0.6, font_name='OpenSans', 
                         halign='left', color=(1, 1, 1, 1),
                         background_color=(0, 0, 0, 0), background_normal='')
        button_search.bind(on_press=self.navigate_to_main_user)

        add_layout_2.add_widget(EmptyWidget(size_hint_x=0.2))
        add_layout_2.add_widget(button_search)
        add_layout_2.add_widget(EmptyWidget(size_hint_x=0.2))
        
        under_layout = BoxLayout(orientation='horizontal', size_hint_y=0.26)
        left_under_layout = BoxLayout(orientation='vertical', size_hint_x=0.2)
        button_back = Button(text='<---', font_size=25, size_hint_y=0.2, 
                         color=(1, 1, 1, 1), background_color=(0, 0, 0, 0), background_normal='')
        button_back.bind(on_press=self.back_to_entity_selector)

        left_under_layout.add_widget(EmptyWidget(size_hint_y=0.8))
        left_under_layout.add_widget(button_back)

        under_layout.add_widget(left_under_layout)
        under_layout.add_widget(EmptyWidget(size_hint_x=0.8))


        #общий layout
        general_layout = BoxLayout(orientation='vertical')
        general_layout.add_widget(EmptyWidget(size_hint_y=0.04))
        general_layout.add_widget(add_layout_2)
        general_layout.add_widget(under_layout)
        layout.add_widget(general_layout)

        self.add_widget(layout)

    def import_organizations(self):
        db = Database("safu", "users", "users")
        list_org = db.fetch_all("SELECT id, organization, wing_rus, abbreviation FROM list_organizations")
        db.close()
        return list_org

    def navigate_to_main_user(self, *args):
        if self.list_org.text != 'Выберите организацию':
            org = [x[1] for x in set(tuple(x) for x in [[org[1], org[3]] for org in self.list_organizations if org[1] == self.list_org.text])]
            constants.what_org = org[0]
            self.manager.current = 'MainUser'

    def back_to_entity_selector(self, *args):
        self.manager.current = 'EntitySelector'