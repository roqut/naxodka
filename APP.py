# my_app.py
from kivy.config import Config
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.text import LabelBase

# general
from scr_Loading import Loading
from scr_EntitySelector import EntitySelector

# for organizations
from scr_LoginSelector import LoginSelector
from scr_Registration import Registration
from scr_AdminMain import AdminMain #scr_AdminMain AM_test
from scr_NewThing import NewThing

# for users
from scr_ChooseOrg import ChooseOrg
from scr_MainUser import MainUser


class OrgApp(App):
    def build(self):
        self.sm = ScreenManager(transition=FadeTransition())
        
        # general
        self.scr_loading = Loading(name = 'Loading')
        self.sm.add_widget(self.scr_loading)
        self.scr_entity_selector = EntitySelector(name = 'EntitySelector')
        self.sm.add_widget(self.scr_entity_selector)

        # for organizations
        self.scr_login_selector = LoginSelector(name='LoginSelector')
        self.sm.add_widget(self.scr_login_selector)
        self.scr_register_screen = Registration(name='Registration')
        self.sm.add_widget(self.scr_register_screen)
        self.scr_AdminMain = AdminMain(name='AdminMain')
        self.sm.add_widget(self.scr_AdminMain)
        self.scr_NewThing = NewThing(name='NewThing')
        self.sm.add_widget(self.scr_NewThing)

        # for users
        self.scr_ChooseOrg = ChooseOrg(name='ChooseOrg')
        self.sm.add_widget(self.scr_ChooseOrg)
        self.scr_MainUser = MainUser(name='MainUser')
        self.sm.add_widget(self.scr_MainUser)

        self.sm.current = 'Loading'

        return self.sm

if __name__ == '__main__':
    LabelBase.register(name='OpenSans', fn_regular='OpenSans_SemiCondensed-BoldItalic.ttf')
    OrgApp().run()