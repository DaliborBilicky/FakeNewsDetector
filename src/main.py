import customtkinter as ctk
from sklearn.svm import LinearSVC

import button_commands as bc

# import config as cf
from detector import Detector

# from CTkMessagebox import CTkMessagebox


TITLE = "Fake news detector"
FONT = ("Arial", 30)


def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")
    window = ctk.CTk()
    window.title(TITLE)
    window.resizable(False, False)

    detector = Detector(LinearSVC(dual="auto"))
    detector.read_training_data()
    detector.load_model()

    entry = ctk.CTkEntry(window, width=400, font=FONT)
    entry.grid(row=0, column=0, padx=10, pady=10)

    pick_button = ctk.CTkButton(
        window,
        text="Brows files",
        font=FONT,
        command=lambda: bc.pick_file(entry),
    )
    pick_button.grid(row=0, column=1, pady=10)

    identify_button = ctk.CTkButton(
        window,
        text="Identify",
        font=FONT,
        command=lambda: bc.identify(detector, entry.get()),
    )
    identify_button.grid(row=1, column=0, pady=10, columnspan=2)

    spacer = ctk.CTkLabel(window, text=" ", font=FONT)
    spacer.grid(row=2, column=0, pady=5)

    score_label = ctk.CTkLabel(
        window, text=f"Score: {detector.get_score()}%", font=FONT
    )
    score_label.grid(row=3, column=1, padx=10, pady=10)

    detectos = [detector, detector]

    def optionmenu_callback(choice):
        print(f"optionmenu dropdown clicked: {choice}")

    optionmenu_var = ctk.StringVar(value=str(detectos[0]))
    optionmenu = ctk.CTkOptionMenu(
        window,
        font=FONT,
        dropdown_font=FONT,
        width=350,
        values=[str(detectos[0]), str(detectos[1])],
        command=optionmenu_callback,
        variable=optionmenu_var,
    )
    optionmenu.grid(row=3, column=0, padx=10, pady=10)

    retrain_button = ctk.CTkButton(
        window,
        text="Retrain model",
        font=FONT,
        command=lambda: bc.identify(detector, entry.get()),
    )
    retrain_button.grid(row=4, column=0, pady=10, columnspan=2)

    window.mainloop()


if __name__ == "__main__":
    main()
