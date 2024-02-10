from tkinter import filedialog

from CTkMessagebox import CTkMessagebox


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

        icon = "info"
        result = detector.identify()

        if result == "REAL":
            icon = "check"
        else:
            icon = "cancel"

        CTkMessagebox(
            title="Result",
            message=f"Article is probably: {result}",
            icon=icon,
            button_color="#2fa572",
            button_hover_color="#106a43",
            font=("Arial", 20),
        )

    else:
        CTkMessagebox(
            title="Error",
            message="Error, provide path or url",
            icon="cancel",
            button_color="#2fa572",
            button_hover_color="#106a43",
            font=("Arial", 20),
        )
