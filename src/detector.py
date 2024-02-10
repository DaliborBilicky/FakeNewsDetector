import pickle

import pandas as pd
import requests
from bs4 import BeautifulSoup
from CTkMessagebox import CTkMessagebox
from sklearn.feature_extraction.text import TfidfVectorizer


class Detector:
    def __init__(self, classifier):
        self.vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
        self.classifier = classifier
        self.text = None
        self.authenticity = None
        self.text_vec = None
        self.article = ""

    def get_score(self) -> float:
        return round(
            self.classifier.score(self.text_vec, self.authenticity) * 100, 3
        )

    def __str__(self) -> str:
        return type(self.classifier).__name__

    def read_training_data(self):
        data = pd.read_csv("./res/fake_or_real_news.csv")
        data["authenticity"] = data["label"].apply(
            lambda a: 0 if a == "REAL" else 1
        )
        data = data.drop("label", axis=1)
        self.text, self.authenticity = data["text"], data["authenticity"]
        self.text_vec = self.vectorizer.fit_transform(self.text)

    def train_model(self):
        self.classifier.fit(self.text_vec, self.authenticity)

        CTkMessagebox(
            title="Model trained",
            message=f"{self} model is successfully trained.",
            icon="check",
            button_color="#2fa572",
            button_hover_color="#106a43",
            font=("Arial", 20),
        )

    def read_link(self, url):
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
                button_color="#2fa572",
                button_hover_color="#106a43",
                font=("Arial", 20),
            )

    def read_txt(self, path):
        with open(path, "r", encoding="utf-8") as my_file:
            self.article = my_file.read()

    def identify(self) -> str:
        vec_article = self.vectorizer.transform([self.article])

        num = self.classifier.predict(vec_article)[0]

        if num == 1:
            return "FAKE"
        else:
            return "REAL"

    def save_model(self):
        with open(f"res/models/{self}.pickle", "wb") as f:
            pickle.dump(self.classifier, f)
        CTkMessagebox(
            title="Model saved",
            message=f"Model {self} was successfully saved.",
            icon="check",
            button_color="#2fa572",
            button_hover_color="#106a43",
            font=("Arial", 20),
        )

    def load_model(self):
        with open(f"res/models/{self}.pickle", "rb") as f:
            self.classifier = pickle.load(f)
        CTkMessagebox(
            title="Model loaded",
            message=f"Model {self} was successfully loaded.",
            icon="info",
            button_color="#2fa572",
            button_hover_color="#106a43",
            font=("Arial", 20),
        )
