import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


class Detector:
    def __init__(self, classifier=LinearSVC(dual="auto")):
        self.vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
        self.trained = False
        self.classifier = classifier
        self.text = np.array([])
        self.authenticity = np.array([])
        self.text_vec = None
        self.article = ""

    def read_training_data(self):
        data = pd.read_csv("./res/fake_or_real_news.csv")
        data["authenticity"] = data["label"].apply(
            lambda a: 0 if a == "REAL" else 1
        )
        data = data.drop("label", axis=1)
        self.text, self.authenticity = data["text"], data["authenticity"]

    def vectorize_training_data(self):
        self.text_vec = self.vectorizer.fit_transform(self.text)
        self.trained = True

    def getScore(self) -> float:
        if self.trained:
            return self.classifier.score(self.text_vec, self.authenticity)
        else:
            return 0.0

    def train_model(self):
        self.classifier.fit(self.text_vec, self.authenticity)

    def read_link(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            paragraphs = soup.find_all("p")

            self.article = "\n".join([p.get_text() for p in paragraphs])
        else:
            print(f"Error while reading article: {response.status_code}")

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
