import tkinter as tk
from tkinter import filedialog


def main():
    def pick_file():
        path = filedialog.askopenfilename(
            initialdir="C:/Dev/Python/FakeNewsDetection",
            title="Select text file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
        )
        entry.delete(0, "end")
        entry.insert(0, path)

    window = tk.Tk()
    window.title("Fake news detector")
    window.geometry("750x750")
    window.resizable(False, False)

    frame1 = tk.Frame(window, borderwidth=5, relief="groove")
    frame1.pack(padx=5, pady=5)

    help = tk.Label(
        frame1, text="Put here link, path to .txt or pick .txt", font="Arial 20"
    )
    help.grid(row=0, column=0, sticky="w", padx=10)

    entry = tk.Entry(frame1, width=35, borderwidth=5, font="Arial 20")
    entry.grid(row=1, column=0, padx=10, pady=10)

    button = tk.Button(frame1, text="Brows files", font="Arial 20", command=pick_file)
    button.grid(row=1, column=1, padx=10, pady=10)

    frame2 = tk.Frame(window)
    frame2.pack()

    label2 = tk.Label(frame2, text="Hello there")
    label2.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
