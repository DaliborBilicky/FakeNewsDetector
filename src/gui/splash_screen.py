import time

import customtkinter as ctk

import config as cf


class SplashScreen:
    """Pop up window showing info on start of app to tell user what is happening."""

    def __init__(self):
        """Setting up Top level window, label and progress bar."""

        self.window = ctk.CTkToplevel()
        self.window.title("")
        self.window.geometry("400x100")
        self.window.resizable(False, False)

        self.label = ctk.CTkLabel(self.window, font=cf.FONT)
        self.label.pack(pady=10)
        self.progressbar = ctk.CTkProgressBar(self.window, width=300, height=20)
        self.progressbar.pack()

    def update(self, text, progress):
        """Update Splash screen to show current info."""

        self.label.configure(text=text)
        self.progressbar.set(progress / 100)
        self.window.update()
        time.sleep(1)

    def kill(self):
        """Kill Splash screen."""

        self.window.destroy()
