from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Rectangle
import webbrowser

class EmptyWidget(Widget):
    pass

class Registration(Screen):
    def __init__(self, **kwargs):
        super(Registration, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', size_hint_x=1)

        self.background_image = Image(source='images/upper.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(self.background_image)

        label = Label(text='НАХОДКА', font_size=50, font_name='OpenSans', size_hint_y=0.3)
        layout.add_widget(label)

        # блок с описанием
        layout_1 = BoxLayout(orientation='horizontal', size_hint_y=0.2)
        label_condition = Label(text='Чтобы зарегистрировать вашу организацию в нашем приложении вам нужно связаться с нами по почте, указанной ниже',
                                 font_size=25, size_hint_x=0.8, font_name='OpenSans',
                                 halign='center', color=(0, 0, 0, 1))
        label_condition.text_size = (350, None)

        with label_condition.canvas.before:
            Color(1, 1, 1, 1)  # set the color of the rectangle
            RoundedRectangle(pos=label_condition.pos, size=label_condition.size, radius=[5, 5, 5, 5])
        def update_rounded_rect(instance, value):
            with instance.canvas.before:
                instance.canvas.before.clear()
                RoundedRectangle(pos=[instance.pos[0], instance.pos[1] - 10],
                                  size=(instance.size[0], instance.size[1] + 20), radius=[5, 5, 5, 5])
        label_condition.bind(pos=update_rounded_rect, size=update_rounded_rect)

        layout_1.add_widget(EmptyWidget(size_hint_x=0.1))
        layout_1.add_widget(label_condition)
        layout_1.add_widget(EmptyWidget(size_hint_x=0.1))

        # блок с почтой
        layout_2 = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        label_email = Label(text='[u]naxodka@mail.com[/u]', font_size=30, size_hint_x=0.8,
                             font_name='OpenSans', markup=True, italic=True, color=(1, 1, 1, 1))
        label_email.bind(on_touch_down=self.open_email_client)

        with label_email.canvas.before:
            Color(0, 0, 0, 1)  # set the color of the rectangle
            le = RoundedRectangle(pos=label_email.pos, size=label_email.size, radius=[5, 5, 5, 5])
        def update_rounded_rect(instance, value):
            le.pos = instance.pos
            le.size = instance.size
        label_email.bind(pos=update_rounded_rect, size=update_rounded_rect)

        layout_2.add_widget(EmptyWidget(size_hint_x=0.1))
        layout_2.add_widget(label_email)
        layout_2.add_widget(EmptyWidget(size_hint_x=0.1))

        # блок с кнопкой
        layout_3 = BoxLayout(orientation='horizontal', size_hint_y=0.07)
        button_back = Button(text='<---', font_size=25, size_hint_x=0.2, background_color=(0, 0, 0, 0))
        button_back.bind(on_press=self.back_to_login)
        layout_3.add_widget(button_back)
        layout_3.add_widget(EmptyWidget())

        buttons_layout = BoxLayout(orientation='vertical')
        buttons_layout.add_widget(EmptyWidget(size_hint_y=0.14))
        buttons_layout.add_widget(layout_1)
        buttons_layout.add_widget(EmptyWidget(size_hint_y=0.03))
        buttons_layout.add_widget(layout_2)
        buttons_layout.add_widget(EmptyWidget(size_hint_y=0.19))
        buttons_layout.add_widget(layout_3)
        layout.add_widget(buttons_layout)

        self.add_widget(layout)

    def back_to_login(self, *args):
        self.manager.current = 'LoginSelector'

    def open_email_client(self, instance, touch):
        if instance.collide_point(touch.x, touch.y):
            email = 'naxodka@mail.com'
            subject = 'Тема письма'  # optional
            body = ''  # optional
            mailto_link = f'mailto:{email}?subject={subject}&body={body}'
            webbrowser.open(mailto_link)