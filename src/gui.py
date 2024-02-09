import tkinter as tk
from tkinter import filedialog

import config as cf


class UserInterface:
    def __init__(self, window):
        self.window = window

    def setUpUI(self):
        frame1 = tk.Frame(self.window, borderwidth=5, relief="groove")
        frame1.pack(padx=5, pady=5)

        entry = tk.Entry(frame1, width=35, borderwidth=5, font=cf.FONT)
        entry.grid(row=1, column=0, padx=10, pady=10)

        pick_button = tk.Button(
            frame1,
            text="Brows files",
            font=cf.FONT,
            command=lambda: pick_file(entry),
        )
        pick_button.grid(row=1, column=1, padx=10, pady=10)

        identify_button = tk.Button(
            frame1,
            text="Identify",
            font=cf.FONT,
            command=lambda: identifying(entry.get()),
        )
        identify_button.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

        frame2 = tk.Frame(self.window, borderwidth=5, relief="groove")
        frame2.pack(padx=5, pady=5)

        label2 = tk.Label(frame2, text="Hello there")
        label2.grid(row=0, column=0, padx=10, pady=10)


def identifying(path):
    print(path)


def pick_file(entry):
    path = filedialog.askopenfilename(
        initialdir="C:/Dev/Python/FakeNewsDetection",
        title="Select text file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
    )
    entry.delete(0, "end")
    entry.insert(0, path)
