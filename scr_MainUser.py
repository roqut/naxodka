# scr_MainUser.py
# MainLayout.py
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import Color, RoundedRectangle, Rectangle
from db import Database
import base64
from constants import *
import constants

# функция для создания пустого виджета
class EmptyWidget(Widget):
    pass

# функция для закругленных кнопок
class RoundedButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create a rounded rectangle for the button
        with self.canvas.before:
            Color(0.3804, 0.3020, 0.8667, 1)  # white color
            self.active_color = Color(0.3804, 0.3020, 0.8667, 1)
            self.rounded_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[5, 5, 5, 5])
        self.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
        
    def update_rounded_rect(self, instance, value):
        self.rounded_rect.pos = instance.pos
        self.rounded_rect.size = instance.size
        self.active_color.rgb = (0.3804, 0.3020, 0.8667, 1)

class EditPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.95, 0.95)

        db = Database("safu", "users", "users")
        list_items = db.fetch_all("SELECT wing_rus, address FROM list_organizations WHERE abbreviation = %s OR abbreviation = %s", 
                                  (str(constants.what_org), ''))
        db.close()
        list_items = [[i[0], i[1]] for i in list_items]

        self.all_content = BoxLayout(orientation='horizontal')
        
        center_content = BoxLayout(orientation='vertical', size_hint_x=0.9)

        main_label = Label(text="Здесь вы можете ознакомиться с адресами корпусов, вами выбранной организации", font_size=24, 
                           text_size=(350, None), font_name='OpenSans', size_hint_y=0.2, padding=(0, 0, 0, 0), halign='center')

        header_layout = GridLayout(cols=2, size_hint_y=None, size_hint_x=1)
        header_layout.add_widget(Label(text="Корпус", font_name='OpenSans', font_size=24, halign='center'))
        header_layout.add_widget(Label(text="Адрес", font_name='OpenSans', font_size=24, halign='center'))

        # Создаем таблицу
        table_layout = GridLayout(cols=2, size_hint_y=None, padding=10, size_hint_x=1)
        table_layout.bind(minimum_height=table_layout.setter('height'))
        for wing, address in list_items:
            table_layout.add_widget(Label(text=wing, font_size=18, text_size=(180, None), 
                                          size_hint_x=0.5, size_hint_y=None))
            table_layout.add_widget(Label(text=address, font_size=18, text_size=(180, None),  
                                          halign='right', size_hint_x=0.5, size_hint_y=None))
        table_layout.height = table_layout.minimum_height

        # Создаем ScrollView для таблицы
        table_scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, scroll_type=['content'])
        table_scroll.add_widget(table_layout)

        self.save_button = RoundedButton(text="OK", size_hint_y=0.1, background_color=(0, 0, 0, 0),
                                          background_normal='', halign='center', font_name='OpenSans', on_press=self.close)
        
        center_content.add_widget(main_label)
        center_content.add_widget(header_layout)
        center_content.add_widget(table_scroll)
        center_content.add_widget(EmptyWidget(size_hint_y=0.05))
        center_content.add_widget(self.save_button)
        center_content.add_widget(EmptyWidget(size_hint_y=0.05))

        self.all_content.add_widget(EmptyWidget(size_hint_x=0.05))
        self.all_content.add_widget(center_content)
        self.all_content.add_widget(EmptyWidget(size_hint_x=0.05))

        self.add_widget(self.all_content)
        
    def close(self, *args):
         self.dismiss()

'''
Основной класс для просмотра, добавления и изменения объвлений администратором
'''
class MainUser(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.background_image = Image(source='images/grad1.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background_image)

        self.list_container = ScrollView(do_scroll_x=False, do_scroll_y=True, scroll_type=['content'])
        self.list_items = []
        self.list_wing = []

        self.center_layout = BoxLayout(size_hint_x=1)

        self.add_widget(self.layout)
        self.create_header_bar()
        self.center()
        self.layout.add_widget(self.center_layout)
        self.create_footer_bar()
    
    def create_header_bar(self):
        header_bar = BoxLayout(size_hint_y=ADMIN_MAIN_HEADER_BAR_HEIGHT)

        ew_l = EmptyWidget(size_hint_x=0.1)
        ew_r = EmptyWidget(size_hint_x=0.1)

        center_layout = BoxLayout(size_hint_x=0.8, orientation='vertical')
        ew_u = EmptyWidget(size_hint_y=0.2)
        ew_d = EmptyWidget(size_hint_y=0.2)
        text_input_layout = BoxLayout(size_hint_y=0.6)
        self.input_field = TextInput(size_hint_x=0.9, multiline=False)
        text_input_layout.add_widget(self.input_field)
        filter_button = RoundedButton(text='F', background_color=(0, 0, 0, 0),
                                        background_normal='', size_hint_x=0.1)
        filter_button.bind(on_press=self.items_search)
        text_input_layout.add_widget(filter_button)

        center_layout.add_widget(ew_u)
        center_layout.add_widget(text_input_layout)
        center_layout.add_widget(ew_d)

        header_bar.add_widget(ew_l)
        header_bar.add_widget(center_layout)
        header_bar.add_widget(ew_r)
        self.layout.add_widget(header_bar)
     
    #Верхняя панель
    def create_list_items(self):
        self.center_layout.clear_widgets()
        self.list_container.clear_widgets()

        container = GridLayout(cols=1, size_hint_y=None, padding=10, size_hint_x=1)
        container.bind(minimum_height=container.setter('height'))
        
        org = self.list_wing[0][1]
        self.db = Database("safu", "users", "users")
        query = f"SELECT id, description, image, high_school FROM {org}_announcements WHERE status = %s or status = %s"
        self.db.cur.execute(query, ('открыто', '')) #constants.what_admin
        self.list_items = self.db.cur.fetchall()
        self.db.close()
        i = 0
        for row in self.list_items:
                splt = row[1].split('\n')
                splt = [i for i in splt]
                db = Database("safu", "users", "users")
                query = f"SELECT wing_rus FROM list_organizations WHERE wing = '{row[3]}'"
                db.cur.execute(query) #constants.what_admin
                organiation = db.cur.fetchall()[0][0]
                db.close()
                polak = f'{splt[0]}\nГде нашли: {splt[1]}\nГде забрать: {organiation}'
                my_row = [i for i in row]
                my_row[1] = polak
                my_row.append("Х")
                self.list_items[i] = my_row
                container.add_widget(create_list_item(my_row, self.db, row[3]))
                i+=1

        self.list_container.add_widget(container)
        self.center_layout.add_widget(self.list_container)

    def search_list_items(self, search=''):
        self.center_layout.clear_widgets()
        self.list_container.clear_widgets()

        container = GridLayout(cols=1, size_hint_y=None, padding=10, size_hint_x=1)
        container.bind(minimum_height=container.setter('height'))

        for row in self.list_items:
                if search in row[1]:
                    container.add_widget(create_list_item(row, self.db, row[3]))

        self.list_container.add_widget(container)
        self.center_layout.add_widget(self.list_container)

    def center(self):
        self.center_layout.clear_widgets()
        mini_l = BoxLayout(orientation='horizontal')
        mini_l_label = BoxLayout(orientation='vertical', size_hint_x=0.96)
        lb = Label(text='Для появления вещей обновите страницу\n(кнопка справа снизу)\n\nЕсли же вещи не появляются, обратитесь к главному администратору',
                    color=(0, 0, 0, 1), valign='middle', halign='center', size_hint_y=0.3)
        lb.text_size = (400, None)
        with lb.canvas.before:
            Color(1, 1, 1, 1)  # set the color of the rectangle
            lb_2 = RoundedRectangle(pos=lb.pos, size=lb.size, radius=(5, 5, 5, 5))

        def update_rounded_rect(instance, value):
            lb_2.pos = instance.pos
            lb_2.size = instance.size
        lb.bind(pos=update_rounded_rect, size=update_rounded_rect)

        mini_l_label.add_widget(EmptyWidget(size_hint_y=0.35))
        mini_l_label.add_widget(lb)
        mini_l_label.add_widget(EmptyWidget(size_hint_y=0.35))
        mini_l.add_widget(EmptyWidget(size_hint_x=0.02))
        mini_l.add_widget(mini_l_label)
        mini_l.add_widget(EmptyWidget(size_hint_x=0.02))
        self.center_layout.add_widget(mini_l)
  
    def update_rect(self, instance, value):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size

    #Нижняя панель
    def create_footer_bar(self):
        footer_bar = BoxLayout(size_hint_y=ADMIN_MAIN_FOOTER_BAR_HEIGHT)

        with footer_bar.canvas:
            Color(1, 1, 1, 1)  # set the color of the rectangle
            footer_bar_2 = Rectangle(pos=footer_bar.pos, size=footer_bar.size)
        def update_rounded_rect(instance, value):
            footer_bar_2.pos = instance.pos
            footer_bar_2.size = instance.size
        footer_bar.bind(pos=update_rounded_rect, size=update_rounded_rect)

        back_button_layout = BoxLayout(size_hint_x=0.15, orientation='vertical')
        back_button = RoundedButton(text='<--', background_color=(0, 0, 0, 0),
                                          background_normal='', size_hint_y=0.6)
        back_button.bind(on_press=self.back_to_choose)
        ew_u = EmptyWidget(size_hint_y=0.2)
        back_button_layout.add_widget(ew_u)
        back_button_layout.add_widget(back_button)
        ew_d = EmptyWidget(size_hint_y=0.2)
        back_button_layout.add_widget(ew_d)

        new_item_button_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')
        new_item_button = RoundedButton(text='Доп. информация', background_color=(0, 0, 0, 0), font_size=20,
                                          background_normal='', size_hint_y=0.6, font_name='OpenSans')
        new_item_button.bind(on_press=self.dop_info)

        ew_u = EmptyWidget(size_hint_y=0.2)
        new_item_button_layout.add_widget(ew_u)
        new_item_button_layout.add_widget(new_item_button)
        ew_d = EmptyWidget(size_hint_y=0.2)
        new_item_button_layout.add_widget(ew_d)

        update_items_button_layout = BoxLayout(size_hint_x=0.15, orientation='vertical')
        update_items_button = RoundedButton(text='o', background_color=(0, 0, 0, 0),
                                          background_normal='', size_hint_y=0.6)
        update_items_button.bind(on_press=self.update_items)
        ew_u = EmptyWidget(size_hint_y=0.2)
        update_items_button_layout.add_widget(ew_u)
        update_items_button_layout.add_widget(update_items_button)
        ew_d = EmptyWidget(size_hint_y=0.2)
        update_items_button_layout.add_widget(ew_d)

        ew_l = EmptyWidget(size_hint_x=0.05)
        ew_r = EmptyWidget(size_hint_x=0.05)

        footer_bar.add_widget(EmptyWidget(size_hint_x=0.01))
        footer_bar.add_widget(back_button_layout)
        footer_bar.add_widget(EmptyWidget(size_hint_x=0.01))
        footer_bar.add_widget(new_item_button_layout)
        footer_bar.add_widget(EmptyWidget(size_hint_x=0.01))
        footer_bar.add_widget(update_items_button_layout)
        footer_bar.add_widget(EmptyWidget(size_hint_x=0.01))
        self.layout.add_widget(footer_bar)

    def update_items(self, *args):
        self.list_wing = self.create_list_wing()
        self.create_list_items()
    
    def items_search(self, *args):
        self.search_list_items(self.input_field.text)
    
    def create_list_wing(self):
        db = Database("safu", "users", "users")
        list_items = db.fetch_all("SELECT wing_rus, abbreviation FROM list_organizations WHERE abbreviation = %s OR abbreviation = %s", 
                                  (str(constants.what_org), ''))
        db.close()
        return list_items

    def back_to_choose(self, *args):
        self.input_field.text = ''
        self.center()
        self.manager.current = 'ChooseOrg'
        
    def dop_info(self, *args):
        popup = EditPopup(title='', title_align='center', title_size=0, 
                      separator_height=0, background='atlas://data/images/defaulttheme/bubble')
        popup.open()




"""
Дополнительные обязательные функции
"""
# функция содания списка виджетов для scrollview
def create_list_item(item_info, db, high_school):
    list_item = BoxLayout(size_hint_y=None, height=ITEM_HEIGHT)

    image_container = BoxLayout(size_hint_y=None, height=ITEM_HEIGHT, padding=(0, 3, 0, 3))
    list_item.add_widget(image_container)

    item_text = item_info[1]

    text = Label(text=item_text, size_hint_x=0.9, color=(0, 0, 0, 1), padding=(15, 0, 0, 0))

    text.text_size = (350, None)  # Set text_size to wrap text
    with text.canvas.before:
            Color(1, 1, 1, 1)  # set the color of the rectangle
            image_container_2 = RoundedRectangle(pos=text.pos, size=text.size, radius=(5, 5, 5, 5))
    def update_rounded_rect(instance, value):
            image_container_2.pos = [instance.pos[0], instance.pos[1]]
            image_container_2.size = [instance.size[0], instance.size[1]]
    text.bind(pos=update_rounded_rect, size=update_rounded_rect)

    image_container.add_widget(EmptyWidget(size_hint_x=0.05))
    image_container.add_widget(text)
    image_container.add_widget(EmptyWidget(size_hint_x=0.05))

    return list_item

