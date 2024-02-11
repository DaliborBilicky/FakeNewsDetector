import time
import tkinter as tk
from tkinter import ttk

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

import config as cf
import ui
from detector import Detector


def main():
    loading = tk.Tk()
    loading.geometry("400x100")
    loading.resizable(False, False)

    label = tk.Label(loading, font=cf.FONT)
    label.pack()
    progressbar = ttk.Progressbar(
        loading, orient="horizontal", length=200, mode="determinate"
    )
    progressbar.pack()

    label.configure(text="Loading training data")
    progressbar["value"] = 20
    loading.update()
    time.sleep(1)
    data = pd.read_csv(cf.TRAIN_DATA)
    data["authenticity"] = data["authenticity"].apply(
        lambda a: 0 if a == "REAL" else 1
    )

    label.configure(text="Vectorizing data")
    progressbar["value"] = 60
    loading.update()
    time.sleep(1)
    vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
    text, authenticity = data["text"], data["authenticity"]
    text_vec = vectorizer.fit_transform(text)

    label.configure(text="Preparing classifiers")
    progressbar["value"] = 80
    loading.update()
    time.sleep(1)
    lsvc = Detector(LinearSVC(dual="auto"), vectorizer, text_vec, authenticity)
    lg = Detector(LogisticRegression(), vectorizer, text_vec, authenticity)
    dtc = Detector(DecisionTreeClassifier(), vectorizer, text_vec, authenticity)
    gbc = Detector(
        GradientBoostingClassifier(), vectorizer, text_vec, authenticity
    )
    rfc = Detector(RandomForestClassifier(), vectorizer, text_vec, authenticity)

    detectors = {
        str(lsvc): lsvc,
        str(lg): lg,
        str(dtc): dtc,
        str(gbc): gbc,
        str(rfc): rfc,
    }

    label.configure(text="Starting")
    progressbar["value"] = 100
    loading.update()
    time.sleep(2)

    loading.destroy()

    interface = ui.UserInterface(detectors)
    interface.detector_init(str(lsvc))
    interface.gui_init()

    interface.loop()


if __name__ == "__main__":
    main()
