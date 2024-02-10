from tkinter import filedialog


def pick_file(entry):
    path = filedialog.askopenfilename(
        initialdir="C:/Dev/Python/FakeNewsDetection",
        title="Select text file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
    )
    entry.delete(0, "end")
    entry.insert(0, path)


def identify(detector, path):
    if path != "":
        if ".txt" in path:
            detector.read_txt(path)
        else:
            detector.read_link(path)
        print(f"Article is probably: {detector.identify()}")
    else:
        print("Error, provide path or url")

