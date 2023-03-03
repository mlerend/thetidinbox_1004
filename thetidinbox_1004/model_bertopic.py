import glob
import os
import time
from string import punctuation

import joblib
import pandas as pd
from bertopic import BERTopic


def bertopic_model():
    model = BERTopic(verbose=True,embedding_model='paraphrase-MiniLM-L3-v2', min_topic_size= 200)
    return model

def load_bertopic_model():
    model_directory = os.path.join("training_output", "bertopic_models")
    results = glob.glob(f"{model_directory}/*")
    if not results:
        return None

    model_path = sorted(results)[-1]
    print(f"- model loaded from : {model_path}")

    pipe = joblib.load(model_path)
    return pipe

def save_bertopic_model(model):
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    model_path = os.path.join("training_output", "bertopic_models", timestamp)#créer dossier bertopic model dans training output
    print(f"- model saved in : {model_path}")
    joblib.dump(model, model_path)

def dict_cat():
    dict_cat = {-1:"Other",
           0:"Other",
           1: "Cinema/Movies",
           2: "Sports",
           3: "Food & Drinks",
           4: "Music",
           5: "Animals",
           6: "Travels",
           7: "Politics",
           8: "Cars",
           9: "Other",
           10: "Nature/Planet",
           11: "Fashion",
           12: "Internet & Electronics",
           13: "Food & Drinks",
           14: "Cinema/Movies",
           15: "Art",
           16: "Music",
           17: "Sports",
           18: "Finances",
           19: "Art",
           20: "Social Media",
           21: "Social Media"}
    cat_df = pd.DataFrame(index=dict_cat.keys(), data=dict_cat.values(), columns=["Category"])
    return cat_df
