
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer
import pickle
import time
import os
import joblib
import glob

def count_vectorizer():
    # Creating  an instance of the CountVectorizer class
    cv = CountVectorizer(stop_words='english', ngram_range=(1, 2))
    # The fit() function is to learn a vocabulary from one or more documents.
    return cv

def term_frequency():
    tfidf = TfidfTransformer(use_idf=True)
    return tfidf

def tfidf():
    tfidf = TfidfVectorizer(ngram_range=(1,2))
    return tfidf

def model_spam():
    nb = MultinomialNB(alpha=0.001)
    return nb

def save_pipeline_spam(pipeline, params, metrics):

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # save params
    if params is not None:
        params_path = os.path.join("training_output", "spam_params", timestamp + ".pickle")
        print(f"- params saved in : {params_path}")
        with open(params_path, "wb") as file:
            pickle.dump(params, file)

    # save metrics
    if metrics is not None:
        metrics_path = os.path.join("training_output", "spam_metrics", timestamp + ".pickle")
        print(f"- metrics saved in : {metrics_path}")
        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)

    # save model
    if pipeline is not None:
        model_path = os.path.join("training_output", "spam_models", timestamp)
        print(f"- model saved in : {model_path}")
        joblib.dump(pipeline, model_path)

def load_pipeline_spam():

    model_directory = os.path.join("training_output", "spam_models")

    results = glob.glob(f"{model_directory}/*")
    if not results:
        return None

    model_path = sorted(results)[-1]
    print(f"- pipeline loaded from : {model_path}")

    pipe = joblib.load(model_path)

    return pipe
