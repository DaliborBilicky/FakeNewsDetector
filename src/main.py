import customtkinter as ctk
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

import config as cf
import gui
from detector import Detector


def main():
    """Main function."""

    # Initialize main window
    ctk.set_appearance_mode(cf.MODE)
    ctk.set_default_color_theme(cf.THEME)
    window = ctk.CTk()
    window.title(cf.TITLE)
    window.resizable(False, False)

    # Initialize splash window
    splash = gui.SplashScreen()
    splash.update("", 0)

    # Reading data and setting authenticity to numbers
    splash.update("Reading data", 20)
    data = pd.read_csv(cf.TRAIN_DATA)
    data["authenticity"] = data["authenticity"].apply(
        lambda a: 0 if a == "REAL" else 1
    )

    # Vectorizing data because classifier can not work with text
    splash.update("Vectorizing data", 60)
    vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
    text, authenticity = data["text"], data["authenticity"]
    text_vec = vectorizer.fit_transform(text)

    # Setting classifier into Detectors
    splash.update("Preparing classifiers", 80)
    lsvc = Detector(LinearSVC(dual="auto"), vectorizer, text_vec, authenticity)
    lg = Detector(LogisticRegression(), vectorizer, text_vec, authenticity)
    dtc = Detector(DecisionTreeClassifier(), vectorizer, text_vec, authenticity)
    gbc = Detector(
        GradientBoostingClassifier(), vectorizer, text_vec, authenticity
    )

    detectors = {str(lsvc): lsvc, str(lg): lg, str(dtc): dtc, str(gbc): gbc}

    splash.update("Strating", 100)
    splash.kill()

    # Main gui
    interface = gui.UserInterface(detectors, window)
    interface.detector_init(str(lsvc))
    interface.gui_init()

    window.mainloop()


if __name__ == "__main__":
    main()
