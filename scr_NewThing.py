from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Rectangle
from PIL import Image as IMAGE
import os
import psycopg2
from db import Database
from kivy.core.window import Window
import constants

# функция для создания пустого виджета
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

class RoundedButtonPhoto(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create a rounded rectangle for the button
        with self.canvas.before:
            Color(0.9922, 1, 0.6235, 1)  # white color
            self.rounded_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=(10, 10, 10, 10))
        self.bind(pos=self.update_rounded_rect, size=self.update_rounded_rect)
        
    def update_rounded_rect(self, instance, value):
        self.rounded_rect.pos = instance.pos
        self.rounded_rect.size = instance.size


class NewThing(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database("safu", "safu_admins", "SAFU")
        self.layout = BoxLayout(orientation='vertical')
        self.space_image = BoxLayout(orientation='vertical')
        self.background_image = Image(source='images/grad2.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background_image)
        self.main_ui()
        self.add_widget(self.layout)

    def main_ui(self):
        self.layout.clear_widgets()

        #создание верхней панели (одна кнопка выхода)
        header_bar = BoxLayout(orientation='horizontal', size_hint_y=0.05)
        back_button = Button(text='X', font_size=30, font_name='OpenSans', 
                                  size_hint_x=0.1, background_color=(0, 0, 0, 0), background_normal='')
        back_button.bind(on_press=self.back_to_amdin_main)
        header_bar.add_widget(EmptyWidget(size_hint_x=0.9))
        header_bar.add_widget(back_button)
        
        #создание основного layout
        submit_layout = BoxLayout(orientation='horizontal', size_hint_y=0.95)
        submit_center_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)


        self.image_button_box_main = BoxLayout(orientation='horizontal', size_hint_y=0.25)
        self.image_button_box = BoxLayout(size_hint_x=0.8)

        image_button = RoundedButtonPhoto(text='ВЫБРАТЬ ФОТО', color=(0, 0, 0, 1), background_color=(0, 0, 0, 0),
                                          background_normal='', font_name='OpenSans', font_size=30, halign='center')
        image_button.text_size = (200, None)
        image_button.bind(on_release=self.show_file_chooser)
        self.image_button_box.add_widget(image_button)

        with self.image_button_box_main.canvas.before:
                Color(1, 1, 1, 1)  # set the color of the rectangle
                image_2 = RoundedRectangle(pos=self.image_button_box_main.pos, size=self.image_button_box_main.size, 
                                                     radius=(10, 10, 10, 10))
        def update_rounded_rect(instance, value):
                image_2.pos = [instance.pos[0]+20, instance.pos[1]-10]
                image_2.size = [instance.size[0]-40, instance.size[1]+20]
        self.image_button_box_main.bind(pos=update_rounded_rect, size=update_rounded_rect)
        
        self.image_button_box_main.add_widget(EmptyWidget(size_hint_x=0.1))
        self.image_button_box_main.add_widget(self.image_button_box)
        self.image_button_box_main.add_widget(EmptyWidget(size_hint_x=0.1))


        decription_label = Label(text="Введите краткое описание вещи:", font_size=20, 
                           text_size=(340, None), font_name='OpenSans', size_hint_y=0.08, padding=(20, 20, 0, 5))
        self.description_input = TextInput(multiline=False, font_size=20, size_hint_y=0.06, padding=(20, 10, 0, 0))

        location_label = Label(text="Введите место, где нашли:", font_size=20, 
                           text_size=(340, None), font_name='OpenSans', size_hint_y=0.08, padding=(20, 20, 0, 5))
        self.location_input = TextInput(multiline=False, font_size=20, size_hint_y=0.06, padding=(20, 10, 0, 0))

        self.error_label = Label(text="", font_size=20, color=(1, 0, 0, 1),
                           text_size=(350, None), font_name='OpenSans', size_hint_y=0.1, padding=(30, 0, 0, 0))
        self.submit_button = RoundedButton(text='Создать объявление', font_name='OpenSans', 
                                           font_size=25, size_hint_y=0.1, background_color=(0, 0, 0, 0),
                                          background_normal='')
        self.submit_button.bind(on_release=self.submit_data)

        submit_center_layout.add_widget(EmptyWidget(size_hint_y=0.05))
        submit_center_layout.add_widget(self.image_button_box_main)
        submit_center_layout.add_widget(EmptyWidget(size_hint_y=0.05))
        submit_center_layout.add_widget(decription_label)
        submit_center_layout.add_widget(self.description_input)
        submit_center_layout.add_widget(location_label)
        submit_center_layout.add_widget(self.location_input)
        submit_center_layout.add_widget(self.error_label)
        submit_center_layout.add_widget(self.submit_button)
        submit_center_layout.add_widget(EmptyWidget(size_hint_y=0.17))

        submit_layout.add_widget(EmptyWidget(size_hint_x=0.15))
        submit_layout.add_widget(submit_center_layout)
        submit_layout.add_widget(EmptyWidget(size_hint_x=0.15))

        self.layout.add_widget(header_bar)
        self.layout.add_widget(submit_layout)
        
        self.image_data = None
        self.image_path = None


    def show_file_chooser(self, instance):
        self.file_chooser = FileChooserIconView()
        self.file_chooser.path = os.path.join(os.path.expanduser('~'), 'Pictures')
        self.file_chooser.filters = ['*.*']
        self.file_chooser.bind(on_selection=self.on_selection)

        self.popup = Popup(title='Выберите фотографию', title_align='center',
                      separator_height=0, background='atlas://data/images/defaulttheme/bubble', content=self.file_chooser, size_hint=(0.8, 0.8))

        # Создаем кнопку "Выбрать"
        choose_button = RoundedButton(text='Выбрать фотографию', size_hint=(1, 0.1), background_color=(0, 0, 0, 0),
                                          background_normal='')
        choose_button.bind(on_release=self.on_choose)

        # Добавляем кнопку к файловому выборщику
        self.file_chooser.add_widget(choose_button)

        self.popup.open()

    def on_choose(self, instance):
        # Закрываем popup и обрабатываем выбранный файл
        self.popup.dismiss()
        # Обработка выбранного файла
        if self.file_chooser.selection:
            self.image_path = self.file_chooser.selection[0]
            with open(self.image_path, 'rb') as file:
                self.image_data = file.read()


            # Заменяем кнопку на изображение
            self.image_button_box.clear_widgets()
            self.image_button_box.add_widget(Image(source=self.image_path))
            

    def on_selection(self, chooser, selection):
        if selection and len(selection) > 0:
            try:
                self.image_path = selection[0]
                with open(self.image_path, 'rb') as file:
                    self.image_data = file.read()

                # Обновить виджет изображения
                if isinstance(self.image_widget, Button):
                    self.image_button_box.clear_widgets()
                    self.image_button_box.add_widget(Image(source=self.image_path, allow_stretch=True, 
                                                           size_hint=(1, 1), keep_ratio=False))

                # Затем закрыть popup
                self.popup.dismiss()
            except Exception as e:
                pass
        else:
            pass

    def submit_data(self, instance):
        description = self.description_input.text + '\n' + self.location_input.text
        
        if len(self.description_input.text) >=3 and len(self.location_input.text) >=3 and self.image_data:
            try:
                self.db.cur.execute("INSERT INTO SAFU_announcements (description, image, high_school) VALUES (%s, %s, %s)",
                                     (description, psycopg2.Binary(self.image_data), constants.what_admin))
                self.db.conn.commit()
                self.description_input.text = ''
                self.location_input.text = ''
                self.error_label.text = ''
                self.main_ui()
            except Exception as e:
                pass
        else:
            self.error_label.text = 'Ошибка! Введены не все данные!'

    def back_to_amdin_main(self, *args):
        self.error_label.text = ''
        self.manager.current = 'AdminMain'
