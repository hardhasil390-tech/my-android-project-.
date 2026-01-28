from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from jnius import autoclass
import sys

class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        self.hacked_label = Label(
            text='[SYSTEM HACKED]\nUnauthorized Access Detected', 
            color=(0, 1, 0, 1), 
            font_size='25sp',
            halign='center'
        )
        self.layout.add_widget(self.hacked_label)
        self.show_permission_dialog()
        return self.layout

    def show_permission_dialog(self):
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        msg = Label(text="This app requires 'Display over other apps' \npermission to function properly.")
        btn_layout = BoxLayout(size_hint_y=None, height='50dp', spacing=10)
        acc_btn = Button(text='Access', background_color=(0, 1, 0, 1))
        dec_btn = Button(text='Decline', background_color=(1, 0, 0, 1))
        btn_layout.add_widget(acc_btn)
        btn_layout.add_widget(dec_btn)
        content.add_widget(msg)
        content.add_widget(btn_layout)
        self.popup = Popup(title='Permission Required', content=content, size_hint=(0.8, 0.4), auto_dismiss=False)
        acc_btn.bind(on_release=self.open_settings)
        dec_btn.bind(on_release=self.exit_app)
        self.popup.open()

    def open_settings(self, instance):
        try:
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Settings = autoclass('android.provider.Settings')
            Uri = autoclass('android.net.Uri')
            Intent = autoclass('android.content.Intent')
            context = PythonActivity.mActivity
            intent = Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION)
            intent.setData(Uri.parse("package:" + context.getPackageName()))
            context.startActivity(intent)
            self.popup.dismiss()
        except:
            pass

    def exit_app(self, instance):
        App.get_running_app().stop()
        sys.exit()

if __name__ == '__main__':
    MyApp().run()
