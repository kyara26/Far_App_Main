import time
import cv2
import numpy as np
import requests
from kivy.uix.popup import Popup
from kivy.app import App
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
        Clock.schedule_once(self.change_screen, 2)

    def change_screen(self, dt):
        self.manager.current = 'homemenu'

class HomeMenu(Screen):
    def __init__(self, **kwargs):
        super(HomeMenu, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 1.0)

    def update_time(self, dt):
        current_time = time.strftime("%I:%M:%S %p")
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
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_leave(self):
        if self.capture:
            self.capture.release()
            Clock.unschedule(self.update)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 0)
            self.current_frame = frame
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.ids.camera_display.texture = texture

    def capture_image(self):
        if hasattr(self, 'current_frame'):
            filename = f"captured_image/captured_image_{int(time.time())}.png"
            cv2.imwrite(filename, cv2.cvtColor(self.current_frame, cv2.COLOR_RGB2BGR))

            # Show processing page
            self.manager.current = 'processingpage'
            Clock.schedule_once(lambda dt: self.process_image(filename), 0)
        else:
            print("No current frame available.")

    def process_image(self, filename):
        # Send image to Roboflow API
        injury_type = self.detect_injury(filename)
        # Delay for processing effect
        Clock.schedule_once(lambda dt: self.navigate_to_page(injury_type), 2)

    def detect_injury(self, image_path):
        # Replace with your Roboflow API URL and API Key
        project_name = "wound-assessment"  # Use your project ID here in lowercase, with dashes instead of spaces
        model_version = "2"  # Specify your model version (e.g., "2" for version 2)
        api_key = "u20PAsYXkCCxa5vJtLEv"  # Replace with your actual API key

        # Formulate the correct API endpoint URL
        roboflow_api_url = f"https://outline.roboflow.com/{project_name}/{model_version}?api_key={api_key}"

        # Prepare the image for upload
        with open(image_path, 'rb') as img_file:
            response = requests.post(
                roboflow_api_url,
                files={"file": img_file}
            )

        # Check if the request was successful
        if response.status_code == 200:
            predictions = response.json()
            print(predictions)  # Print the entire response to see its structure
            # Process the predictions and return the wound type
            return self.process_predictions(predictions)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None



    def process_predictions(self, predictions):
        # Check if there are any predictions
        if not predictions['predictions']:
            print("No predictions found.")
            return None  # Handle the case where no predictions were made

        # Assuming the predictions contain a list of detected objects
        # Iterate through the predictions
        for prediction in predictions['predictions']:
            # Check if 'class' exists in the prediction
            if 'class' in prediction:
                if prediction['class'] == 'bruise':
                    return 'bruise'
                elif prediction['class'] == 'abrasion':
                    return 'abrasion'
                elif prediction['class'] == 'burn':
                    return 'burn'
                elif prediction['class'] == 'minor_wound':
                    return 'minor_wound'
        
        print("No recognized injury types in predictions.")
        return None

    def navigate_to_page(self, injury_type):
            if injury_type == 'bruise':
                self.manager.current = 'bruisepage'
            elif injury_type == 'abrasion':
                self.manager.current = 'abrasionpage'
            elif injury_type == 'burn':
                self.manager.current = 'burnpage'
            elif injury_type == 'minor_wound':
                self.manager.current = 'minorwoundpage'
            else:
                print("No injury detected or unhandled injury type.")
                
class ProcessingPage(Screen):
    def __init__(self, **kwargs):
        super(ProcessingPage, self).__init__(**kwargs)

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
