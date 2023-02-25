from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import time
import os
import joblib
import glob

def vectorizer():
    # Creating  an instance of the CountVectorizer class
    vectorizer = TfidfVectorizer(min_df=0.001,max_df=0.5)
    # The fit() function is to learn a vocabulary from one or more documents.
    return vectorizer


def model_pro_perso():
    nb = MultinomialNB(alpha=0.4)
    return nb

def save_pipeline_pro_perso(pipeline, params, metrics):

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    # save params
    if params is not None:
        params_path = os.path.join("training_output", "pro_perso_params", timestamp + ".pickle")
        print(f"- params saved in : {params_path}")
        with open(params_path, "wb") as file:
            pickle.dump(params, file)

    # save metrics
    if metrics is not None:
        metrics_path = os.path.join("training_output", "pro_perso_metrics", timestamp + ".pickle")
        print(f"- metrics saved in : {metrics_path}")
        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)

    # save model
    if pipeline is not None:
        model_path = os.path.join("training_output", "pro_perso_models", timestamp)
        print(f"- model saved in : {model_path}")
        joblib.dump(pipeline, model_path)

def load_pipeline_pro_perso():

    model_directory = os.path.join("training_output", "pro_perso_models")

    results = glob.glob(f"{model_directory}/*")
    if not results:
        return None

    model_path = sorted(results)[-1]
    print(f"- pipeline loaded from : {model_path}")

    pipe = joblib.load(model_path)

    return pipe
