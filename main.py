import os
from kivymd.app import MDApp
from kivy.graphics.texture import Texture
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
import validation
from kivy.clock import Clock
import cv2
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import requests
from kivy.core.window import Window
from bounding_boxes import params, recognition
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget, OneLineListItem
from kivymd.uix.filemanager import MDFileManager
import shutil
from statistics import get_statistics
#Window.size = (500, 650)


class RecognitionApp(MDApp):
    image_texture = ObjectProperty(None)
    dialog = None
    capture = None
    screen_manager = None
    video_folder = "./video"
    video_play = None
    user_id = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = ScreenManager()
        self.path = os.path.expanduser("~") or os.path.expanduser("/")
        self.filemanager = MDFileManager(
            select_path=self.select_path,
            exit_manager=self.close_filemanager
        )

    def build(self):
        self.screen_manager.add_widget(Builder.load_file("kv/start_f.kv"))
        self.screen_manager.add_widget(Builder.load_file("kv/start_s.kv"))
        self.screen_manager.add_widget(Builder.load_file("kv/login.kv"))
        self.screen_manager.add_widget(Builder.load_file("kv/reg.kv"))
        self.screen_manager.add_widget(Builder.load_file("kv/main.kv"))
        self.screen_manager.add_widget(Builder.load_file("kv/video.kv"))
        self.theme_cls.material_style = "M3"
        return self.screen_manager

    def on_start(self):
        Clock.schedule_once(self.start_window, 10)

    def start_window(self, *args):
        self.screen_manager.current = "start_sec"
        self.check_internet_conn()

    def login(self):
        if self.check_internet_conn():
            current_screen = self.root.current_screen
            login_denied = current_screen.ids.login_denied
            email = current_screen.ids.email
            password = current_screen.ids.password
            valid, user_id = validation.login_valid(email, password)
            if valid:
                self.screen_manager.current = "main"
                self.user_id = user_id
                #self.root.current_screen.ids.scroll_view.clear_widgets()
            elif valid is None:
                pass
            else:
                login_denied.opacity = 1
                print(f"main.py not valid {valid}")

    def signup(self):
        if self.check_internet_conn():
            current_screen = self.root.current_screen
            name = current_screen.ids.name
            surname = current_screen.ids.surname
            email = current_screen.ids.email
            password = current_screen.ids.password
            valid = validation.signup_valid(name, surname, email, password)
            if valid:
                self.screen_manager.current = "login"

    def catching_frames(self, *args):
        try:
            success, frames = self.capture.read()
            if success:
                recognition(frames, self.user_id)
                buffer = cv2.flip(frames, 0).tobytes()
                texture = Texture.create(size=(frames.shape[1], frames.shape[0]), colorfmt="bgr")
                texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
                self.root.current_screen.ids.image.texture = texture
        except Exception as e:
            print(e)

    def turn_on_camera(self):
        self.check_params()
        if self.root.current_screen.ids.image.opacity == 0:
            self.root.current_screen.ids.image.opacity = 1
        self.capture = cv2.VideoCapture(0)
        # self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.camera_play = Clock.schedule_interval(self.catching_frames, 1.0/30.0)

    def show_alert_dialog(self, title, text):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(
                    text="GERAI",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_release=self.close_dialog
                )
            ]
        )
        self.dialog.open()

    def check_internet_conn(self, *args):
        response = False
        url = "http://www.google.com"
        timeout = 1
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
        except Exception as e:
            text = "Nėra interneto ryšio :("
            title = "Patikrinkite, ar tikrai esate prisijungę prie interneto"
            self.show_alert_dialog(text, title)
        return response

    def close_dialog(self, *args):
        self.dialog.dismiss()
        Clock.schedule_once(self.check_internet_conn, 1)

    def update_video_list(self):
        md_list = self.root.current_screen.ids.md_list
        md_list.clear_widgets()
        video_files = [f for f in os.listdir(self.video_folder) if f.endswith((".mp4", ".MOV", ".avi", ".mkv"))]

        if video_files:
            for video_file in video_files:
                item = OneLineAvatarIconListItem(
                    IconLeftWidget(icon="file-video-outline"),
                          IconRightWidget(icon="delete", on_release=lambda x, file=video_file: self.delete_video(file)),
                          text=video_file, on_release=lambda x, file=video_file: self.play_video(file)
                )
                md_list.add_widget(item)
        else:
            item = OneLineListItem(text="Sąrašas tuščias")
            md_list.add_widget(item)

    def delete_video(self, file):
        os.remove(os.path.join(self.video_folder, file))
        self.update_video_list()

    def open_filemanager(self):
        self.filemanager.show(self.path)

    def select_path(self, path):
        title = "Netinkamas formatas :("
        text = "Pasirinkite vaizdo įrašą"
        if path.endswith((".mp4", ".MOV", ".avi", ".mkv")):
            self.close_filemanager(path)
        else:
            self.show_alert_dialog(title, text)

    def close_filemanager(self, path, *args):
        self.filemanager.close()
        self.add_video(path)

    def add_video(self, path):
        try:
            shutil.copy(path, self.video_folder)
            self.update_video_list()
        except Exception as e:
            print(e)

    def play_video(self, file):
        self.check_params()
        self.screen_manager.current = "video"
        self.screen_manager.transition.direction = "left"
        self.capture = cv2.VideoCapture(os.path.join(self.video_folder, file))
        self.video_play = Clock.schedule_interval(self.catching_frames, 1.0 / 30.0)

    def leave_video(self):
        self.capture = None
        if hasattr(self, 'video_play'):
            self.video_play.cancel()

    def camera_off(self):
        print("camera off")
        self.capture = None
        self.root.current_screen.ids.image.opacity = 0
        if hasattr(self, "camera_play"):
            self.camera_play.cancel()

    def statistics(self):
        anchor = self.root.current_screen.ids.anchor_layout
        get_statistics(anchor, self.user_id)

    def check_params(self):
        moment = self.root.current_screen.ids.sw_moment.active
        avg = self.root.current_screen.ids.sw_avg.active
        zone = self.root.current_screen.ids.sw_zone.active
        params(moment, avg, zone)

    def logout(self):
        self.screen_manager.current = "start_sec"


if __name__ == "__main__":
    RecognitionApp().run()
