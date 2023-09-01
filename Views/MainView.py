from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from ServiceLogic import SplitwiseService, DatabaseLogic


class LoginWindow(Screen):
    def loginSplitWise(self):
        sObj = SplitwiseService
        t = sObj.get()
        x = t.getCurrentUser()
        name = x.first_name
        print(name)


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("Views\sw.kv")

sm = WindowManager()

db = DatabaseLogic.DatabaseManager()

screens = [LoginWindow(name="login")]
for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


class SwCameraApp(App):
    def build(self):
        return sm
