from tkinter import filedialog

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

import config as cf


class UserInterface:
    def __init__(self, detectors):
        self.start = True
        self.detectors = detectors

        ctk.set_appearance_mode(cf.MODE)
        ctk.set_default_color_theme(cf.THEME)
        self.window = ctk.CTk()
        self.window.title(cf.TITLE)
        self.window.resizable(False, False)

    def detector_init(self, choice):
        self.detector = self.detectors[choice]
        self.detector.load_model()

        if self.start:
            self.start = False
        else:
            self._reload_label()

    def gui_init(self):
        entry = ctk.CTkEntry(self.window, width=400, font=cf.FONT)
        entry.grid(row=0, column=0, padx=10, pady=10)

        pick_button = ctk.CTkButton(
            self.window,
            text="Brows files",
            font=cf.FONT,
            command=lambda: self._pick_file(entry),
        )
        pick_button.grid(row=0, column=1, pady=10)

        identify_button = ctk.CTkButton(
            self.window,
            text="Identify",
            font=cf.FONT,
            command=lambda: self._identify(entry.get()),
        )
        identify_button.grid(row=1, column=0, pady=10, columnspan=2)

        spacer = ctk.CTkLabel(self.window, text=" ", font=cf.FONT)
        spacer.grid(row=2, column=0, pady=5)

        self.score_label = ctk.CTkLabel(
            self.window,
            font=cf.FONT,
        )
        self.score_label.grid(row=3, column=1, padx=10, pady=10)

        self._reload_label()

        optionmenu_var = ctk.StringVar(value=str(self.detector))
        optionmenu = ctk.CTkOptionMenu(
            self.window,
            font=cf.FONT,
            dropdown_font=cf.FONT,
            width=400,
            values=list(self.detectors.keys()),
            command=self.detector_init,
            variable=optionmenu_var,
        )
        optionmenu.grid(row=3, column=0, padx=10, pady=10)

        retrain_button = ctk.CTkButton(
            self.window,
            text="Retrain model",
            font=cf.FONT,
            command=lambda: self._retrain(),
        )
        retrain_button.grid(row=4, column=0, pady=10, columnspan=2)

    def _reload_label(self):
        self.score_label.configure(text=f"Score: {self.detector.get_score()}%")

    def _pick_file(self, entry):
        path = filedialog.askopenfilename(
            initialdir=cf.INIT_DIR,
            title="Select text file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        )
        entry.delete(0, "end")
        entry.insert(0, path)

    def _identify(self, path):
        if path != "":
            if ".txt" in path:
                self.detector.read_txt(path)
            else:
                self.detector.read_link(path)

            icon = "info"
            result = self.detector.identify()

            if result == "REAL":
                icon = "check"
            else:
                icon = "cancel"

            CTkMessagebox(
                title="Result",
                message=f"Article is probably: {result}",
                icon=icon,
                button_color=cf.GREEN,
                button_hover_color=cf.HOVER_GREEN,
                font=cf.MESSEAGE_FONT,
            )

        else:
            CTkMessagebox(
                title="Error",
                message="Error, provide path or url",
                icon="cancel",
                button_color=cf.GREEN,
                button_hover_color=cf.HOVER_GREEN,
                font=cf.MESSEAGE_FONT,
            )

    def _retrain(self):
        self.detector.train_model()
        self.detector.save_model()

    def loop(self):
        self.window.mainloop()
