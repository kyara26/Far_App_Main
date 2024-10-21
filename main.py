import time
import cv2
from kivy.uix.popup import Popup
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.graphics.texture import Texture

Window.size = (310, 670)

class LoadingPage(Screen):
    def __init__(self, **kwargs):
        super(LoadingPage, self).__init__(**kwargs)
        Clock.schedule_once(self.change_screen, 2)  # change screen of the duration (seconds)

    def change_screen(self, dt):
        self.manager.current = 'homemenu'

class HomeMenu(Screen):
    def __init__(self, **kwargs):
        super(HomeMenu, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 1.0)

    def update_time(self, dt):
        current_time = time.strftime("%I:%M:%S %p") #Real-Time Clock
        self.ids.clock_label.text = current_time

class FirstAidMenu1(Screen):
    pass

class FirstAidMenu2(Screen):
    pass

class CameraMenu(Screen):
    def __init__(self, **kwargs):
        super(CameraMenu, self).__init__(**kwargs)
        self.capture = None

    def on_enter(self):
        self.capture = cv2.VideoCapture(0)  # Use the first camera
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Update at 30 FPS

    def on_leave(self):
        if self.capture:
            self.capture.release()
            Clock.unschedule(self.update)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 0)
            self.current_frame = frame  # Store the current frame for capturing
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.ids.camera_display.texture = texture

    def capture_image(self):
        if hasattr(self, 'current_frame'): # Save the current frame as an image
            filename = f"captured_image/captured_image_{int(time.time())}.png"
            cv2.imwrite(filename, cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR))
        else:
            self.timer.cancel() # stop the timer if the camera is not available
            
class BruisePage(Screen):
    pass

class AbrasionPage(Screen):
    pass

class BurnPage(Screen):
    pass

class MinorWoundPage(Screen):
    pass

class BleedingPage(Screen):
    pass

class SprainPage(Screen):
    pass

class AmbulanceMenu1(Screen):
    pass

class AmbulanceMenu2(Screen):
    pass

class ScreenManagement(ScreenManager):
    pass

class WindowManager(ScreenManager):
    pass

file=Builder.load_file('FirstAidResponder.kv')

class FirstAidApp(App):
   def build(self):
        return file
    
FirstAidApp().run()
