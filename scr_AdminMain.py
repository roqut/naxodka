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
            Color(0.3804, 0.3020, 0.8667, 1)
            self.active_color = Color(0.3804, 0.3020, 0.8667, 1)
            self.rounded_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[5, 5, 5, 5])
        self.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
        
    def update_rounded_rect(self, instance, value):
        self.rounded_rect.pos = instance.pos
        self.rounded_rect.size = instance.size
        self.active_color.rgb = (0.3804, 0.3020, 0.8667, 1)

class RoundedButtonDelete(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create a rounded rectangle for the button
        with self.canvas.before:
            Color(1, 0, 0.2, 1)
            self.active_color = Color(1, 0, 0.2, 1)
            self.rounded_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[5, 5, 5, 5])
        self.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
        
    def update_rounded_rect(self, instance, value):
        self.rounded_rect.pos = instance.pos
        self.rounded_rect.size = instance.size
        self.active_color.rgb = (1, 0, 0.2, 1)

# класс для создания popup, где происходит закрытие объявлений
class EditPopup(Popup):
    def __init__(self, item_id, **kwargs):
        super().__init__(**kwargs)
        self.item_id = item_id
        self.size_hint = (0.8, 0.5)

        self.all_content = BoxLayout(orientation='horizontal')
        
        center_content = BoxLayout(orientation='vertical', size_hint_x=0.8)

        main_label = Label(text="Введите ФИО забравшего вещь:", font_size=20, 
                           text_size=(270, None), font_name='OpenSans', size_hint_y=0.25, padding=(10, 0, 0, 0))
        self.who_input = TextInput(multiline=False, font_size=25, size_hint_y=0.15, padding=(10, 10, 0, 0))
        self.error_label = Label(text="", font_size=20, text_size=(270, None), font_name='OpenSans', 
                                 size_hint_y=0.1, color=(1, 0, 0, 1), padding=(10, 10, 0, 10))
        self.save_button = RoundedButtonDelete(text="Закрыть\nобъявление", size_hint_y=0.2, background_color=(0, 0, 0, 0),
                                          background_normal='', halign='center', font_name='OpenSans', on_press=self.save_changes)
        
        right_content = BoxLayout(orientation='vertical', size_hint_x=0.1)
        self.back_button = Button(text="X", size_hint_y=0.10, font_size=30, font_name='OpenSans', background_color=(0, 0, 0, 0),
                                          background_normal='', halign='center', on_press=self.back_to_main_admin)
        right_content.add_widget(self.back_button)
        right_content.add_widget(EmptyWidget(size_hint_y=0.8))

        center_content.add_widget(EmptyWidget(size_hint_y=0.15))
        center_content.add_widget(main_label)
        center_content.add_widget(self.who_input)
        center_content.add_widget(self.error_label)
        center_content.add_widget(self.save_button)
        center_content.add_widget(EmptyWidget(size_hint_y=0.15))

        self.all_content.add_widget(EmptyWidget(size_hint_x=0.1))
        self.all_content.add_widget(center_content)
        self.all_content.add_widget(right_content)

        self.add_widget(self.all_content)

    def save_changes(self, instance):
        if len(self.who_input.text) < 3:
            self.error_label.text = 'Введено мало символов!'
        
        else:
            db = Database("safu", "users", "users")
            abbr = db.fetch_all("SELECT abbreviation FROM list_organizations WHERE wing = %s", 
                                  (constants.what_admin, ))
            db.close()
            
            who = self.who_input.text
            db = Database("safu", "safu_main_admin", "sAr")
            db.execute(f"UPDATE {abbr[0][0]}_announcements SET who = '{who}' WHERE id = {int(self.item_id)}")
            db.execute(f"UPDATE {abbr[0][0]}_announcements SET status = 'закрыто' WHERE id = {int(self.item_id)}")
            db.commit()
            db.close()
            self.dismiss()

    def back_to_main_admin(self, *args):
        self.dismiss()


'''
Основной класс для просмотра, добавления и изменения объвлений администратором
'''
class AdminMain(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')

        self.center_layout = BoxLayout(size_hint_x=1)
        self.list_container = ScrollView(do_scroll_x=False, do_scroll_y=True, scroll_type=['content'])
        self.list_items = []

        self.background_image = Image(source='images/grad2.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background_image)
        self.add_widget(self.layout)

        self.create_header_bar()
        self.center()
        self.create_footer_bar()
     
    #Верхняя панель
    def create_header_bar(self):
        header_bar = BoxLayout(size_hint_y=ADMIN_MAIN_HEADER_BAR_HEIGHT)

        with header_bar.canvas:
            Color(1, 1, 1, 1)  # set the color of the rectangle
            footer_bar_2 = Rectangle(pos=header_bar.pos, size=header_bar.size)
            
        def update_rounded_rect(instance, value):
            footer_bar_2.pos = instance.pos
            footer_bar_2.size = instance.size
            
        header_bar.bind(pos=update_rounded_rect, size=update_rounded_rect)

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

    def create_list_items(self):
        self.center_layout.clear_widgets()
        self.list_container.clear_widgets()

        container = GridLayout(cols=1, size_hint_y=None, padding=10, size_hint_x=1)
        container.bind(minimum_height=container.setter('height'))

        self.db = Database("safu", "safu_admins", "SAFU")
        query = f"SELECT id, description, image FROM SAFU_announcements WHERE status = %s and high_school = %s"
        self.db.cur.execute(query, ('открыто',constants.what_admin)) #constants.what_admin
        self.list_items = self.db.cur.fetchall()
        self.db.close()

        for row in self.list_items:
                container.add_widget(create_list_item(row+("Х", "0"), self.db))

        self.list_container.add_widget(container)
        self.center_layout.add_widget(self.list_container)

    def search_list_items(self, search=''):
        self.center_layout.clear_widgets()
        self.list_container.clear_widgets()

        container = GridLayout(cols=1, size_hint_y=None, padding=10, size_hint_x=1)
        container.bind(minimum_height=container.setter('height'))
        print(search)

        for row in self.list_items:
                if search in row[1]:
                    container.add_widget(create_list_item(row+("Х", "0"), self.db))

        self.list_container.add_widget(container)
        self.center_layout.add_widget(self.list_container)

    def center(self):
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
        self.layout.add_widget(self.center_layout)
  
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
        back_button.bind(on_press=self.back_to_login)
        ew_u = EmptyWidget(size_hint_y=0.2)
        back_button_layout.add_widget(ew_u)
        back_button_layout.add_widget(back_button)
        ew_d = EmptyWidget(size_hint_y=0.2)
        back_button_layout.add_widget(ew_d)

        new_item_button_layout = BoxLayout(size_hint_x=0.5, orientation='vertical')
        new_item_button = RoundedButton(text='Новое объявление', background_color=(0, 0, 0, 0),
                                          background_normal='', size_hint_y=0.6)
        new_item_button.bind(on_press=self.navigate_to_new_thing)
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
        self.create_list_items()
    
    def items_search(self, *args):
        self.search_list_items(self.input_field.text)

    def back_to_login(self, *args):
        self.manager.current = 'LoginSelector'

    def navigate_to_new_thing(self, *args):
        self.manager.current = 'NewThing'
    


"""
Дополнительные обязательные функции
"""
# функция содания списка виджетов для scrollview
def create_list_item(item_info, db):
    list_item = BoxLayout(size_hint_y=None, height=ITEM_HEIGHT, size_hint_x=1)

    image_container = BoxLayout(size_hint_y=None, height=ITEM_HEIGHT, padding=(0, 7, 0, 7), size_hint_x=1)
    with image_container.canvas:
        Color(1, 1, 1, 1)  # set the color of the rectangle
        image_container_2 = Rectangle(pos=image_container.pos, size=image_container.size)
    def update_rounded_rect(instance, value):
        image_container_2.pos = [instance.pos[0]-100, instance.pos[1]+1]
        image_container_2.size = [instance.size[0]+200, instance.size[1]-2]
    image_container.bind(pos=update_rounded_rect, size=update_rounded_rect)

    list_item.add_widget(image_container)

    image = create_image(item_info[2], IMAGE_WIDTH_HINT)
    
    text = Label(text=item_info[1], font_size=18, size_hint_x=TEXT_WIDTH_HINT, color=(0, 0, 0, 1))
    text.text_size = (240, None)  # Set text_size to wrap text

    # Установка высоты image_container в зависимости от высоты текста
    def update_height(instance, value):
        instance.height = instance.texture_size[1] + 20  # добавляем 20 пикселей для padding
    text.bind(texture_size=update_height)

    button_delete = RoundedButtonDelete(text=item_info[3], background_color=(0, 0, 0, 0),
                                          background_normal='', size_hint_x=0.07)
    button_delete.bind(on_press=lambda btn: show_popup(item_info[0]))

    image_container.add_widget(image)
    image_container.add_widget(text)
    image_container.add_widget(button_delete)

    return list_item

# функция для преобразования фотографий
def create_image(image_data, width_hint):
    image = Image(source="data:image/jpeg;base64," + base64.b64encode(image_data).decode('utf-8'),
                   size_hint_x=width_hint, allow_stretch=True, keep_ratio=False)
    return image

# функция для создания popup, где происходит закрытие объявлений
def show_popup(item_text):
    popup = EditPopup(item_text, title='', title_align='center', title_size=0, 
                      separator_height=0, background='atlas://data/images/defaulttheme/bubble')
    popup.open()


    