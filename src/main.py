import tkinter as tk

import config as cf
from detector import Detector
from gui import UserInterface

# from sklearn.svm import LinearSVC


def main():
    window = tk.Tk()
    window.title(cf.TITLE)
    window.geometry(cf.DIAMETERS)
    window.resizable(False, False)

    detector = Detector()
    detector.read_training_data()
    detector.vectorize_training_data()
    detector.train_model()
    print(f"Score: {detector.getScore()}")
    # detector.read_link("ahoj")
    # detector.read_txt("C:/Dev/Python/FakeNewsDetector/res/fake_article.txt")
    print(f"Article is probably: {detector.identify()}")

    gui = UserInterface(window)
    gui.setUpUI()

    window.mainloop()


if __name__ == "__main__":
    main()
