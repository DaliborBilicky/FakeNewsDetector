import pickle

import requests
from bs4 import BeautifulSoup
from CTkMessagebox import CTkMessagebox

import config as cf


class Detector:
    """
    Class which wraps classifier and prepares
    it to predict on training data.
    """

    def __init__(self, classifier, vectorizer, vec_text, authenticity):
        """Some initialization."""

        self.vectorizer = vectorizer
        self.classifier = classifier
        self.vec_text = vec_text
        self.authenticity = authenticity
        self.article = ""

    def get_score(self) -> float:
        """Returns trained model score."""

        score = self.classifier.score(self.vec_text, self.authenticity)
        return round(score * 100, 3)

    def __str__(self) -> str:
        """
        Method which specifies how should be
        this class represented as string
        """

        return type(self.classifier).__name__

    def train_model(self):
        """Trains model and say it after in message box."""

        self.classifier.fit(self.vec_text, self.authenticity)

        CTkMessagebox(
            title="Model trained",
            message=f"{self} model is successfully trained.",
            icon="check",
            button_color=cf.GREEN,
            button_hover_color=cf.HOVER_GREEN,
            font=cf.MESSEAGE_FONT,
        )

    def read_link(self, url):
        """
        Method reads link from internet and sets article
        which is ready to be predicted.
        """

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            paragraphs = soup.find_all("p")

            self.article = "\n".join([p.get_text() for p in paragraphs])
        else:
            CTkMessagebox(
                title="Error",
                message=f"Failed to retrieve article. Status code: {response.status_code}",
                icon="cancel",
                button_color=cf.GREEN,
                button_hover_color=cf.HOVER_GREEN,
                font=cf.MESSEAGE_FONT,
            )

    def read_txt(self, path):
        """
        Method reads .txt file and sets article
        which is ready to be predicted.
        """

        try:
            with open(path, "r", encoding="utf-8") as my_file:
                self.article = my_file.read()
        except FileNotFoundError:
            CTkMessagebox(
                title="Error",
                message=f"{path} was not found.",
                icon="cancel",
                button_color=cf.GREEN,
                button_hover_color=cf.HOVER_GREEN,
                font=cf.MESSEAGE_FONT,
            )

    def identify(self) -> str:
        """Predicting article."""

        vec_article = self.vectorizer.transform([self.article])

        num = self.classifier.predict(vec_article)[0]

        if num == 1:
            return "FAKE"
        else:
            return "REAL"

    def save_model(self):
        """Saves model for better convenience."""

        with open(f"{cf.MODEL_PATH}{self}.pickle", "wb") as f:
            pickle.dump(self.classifier, f)
        CTkMessagebox(
            title="Model saved",
            message=f"Model {self} was successfully saved.",
            icon="check",
            button_color=cf.GREEN,
            button_hover_color=cf.HOVER_GREEN,
            font=cf.MESSEAGE_FONT,
        )

    def load_model(self):
        """
        Loads the model so that it does not
        have to be trained again.
        """

        try:
            with open(f"{cf.MODEL_PATH}{self}.pickle", "rb") as f:
                self.classifier = pickle.load(f)
            CTkMessagebox(
                title="Model loaded",
                message=f"Model {self} was successfully loaded.",
                icon="info",
                button_color=cf.GREEN,
                button_hover_color=cf.HOVER_GREEN,
                font=cf.MESSEAGE_FONT,
            )
        except FileNotFoundError:
            CTkMessagebox(
                title="Error",
                message=f"Model {self} was not found.",
                icon="cancel",
                button_color=cf.GREEN,
                button_hover_color=cf.HOVER_GREEN,
                font=cf.MESSEAGE_FONT,
            )
