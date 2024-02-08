import tkinter as tk

import config as cf
from gui import UserInterface


def main():
    window = tk.Tk()
    window.title(cf.TITLE)
    window.geometry(cf.DIAMETERS)
    window.resizable(False, False)


    gui = UserInterface(window)
    gui.setUpFrames()

    window.mainloop()


if __name__ == "__main__":
    main()
