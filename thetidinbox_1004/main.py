import numpy as np
import pandas as pd
from preprocessing import clean_email_spam,stopword_removal, preprocessing_pro_perso,preprocessing_spam
from model_spam import count_vectorizer, term_frequency,tfidf, model_spam, save_pipeline_spam, load_pipeline_spam
from model_pro_perso import vectorizer, model_pro_perso, save_pipeline_pro_perso,load_pipeline_pro_perso
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from math import sqrt
from data import pro_perso_dataset

def train_spam():
    """ Training and saving a model on spam/non-spam dataset"""

    # Pipeline definition
    pipe = Pipeline([('tfidf', tfidf()),
                 ('classify', model_spam())])

    # Picking the dataset to train on
    emails_df = preprocessing_spam()

    # X and y definition
    X = emails_df['message'].values
    y = emails_df['class'].values

    # Fit
    pipe.fit(X, y)

    # Metrics
    accuracy = pipe.score(X, y)
    y_pred = pipe.predict(X)
    rmse = sqrt(mean_squared_error(y, y_pred))
    metrics = {"accuracy" : round(accuracy,4),
            "rmse" : round(rmse,4)}

    # Parameters
    params = pipe.get_params()

    # Save pipeline
    save_pipeline_spam(pipe, params, metrics)

    print(f'- metrics of the model saved : {metrics}')

    return metrics

def pred_spam(X_pred: pd.DataFrame = None) -> np.ndarray:
    """
    Make a prediction of spam / ham given an X

    X must be a DataFrame with the body of the mail in a column named 'message'

    """
    # Preprocessing
    X_pred.dropna()
    X_pred.drop_duplicates(keep='first',inplace=True)

    # Translate bytes objects into strings.
    try:
        X_pred['message'] = X_pred['message'].apply(lambda x: x.decode('latin-1'))
    except (UnicodeDecodeError, AttributeError):
        pass

    # Reset pandas df index.
    X_pred = X_pred.reset_index(drop=True)

    # Applying preprocessing feature
    X_pred['message'] = X_pred['message'].apply(clean_email_spam)
    X_pred['message'] = X_pred['message'].apply(stopword_removal)

    # Loading the latest pipeline saved
    pipe = load_pipeline_spam()

    # Prediction
    y_pred = pipe.predict(X_pred['message'])
    y_pred_proba = pipe.predict_proba(X_pred['message'])

    return y_pred


def preprocessing_pro_perso_dataset():
    """ Preprocessing the email/message dataset"""

    df = pro_perso_dataset()
    df_preproc = preprocessing_pro_perso(df)
    return df_preproc

def train_pro_perso():
    """ Training and saving a model on the preprocessed email/message dataset"""

    # Pipeline definition
    pipe = Pipeline([('vectorize', vectorizer()),
                 ('classify', model_pro_perso())])

    # X and y definition
    emails_df = preprocessing_pro_perso_dataset()
    X = emails_df['body'].values
    y = emails_df['category'].values

    # Fit
    pipe.fit(X, y)

    # Metrics
    accuracy = pipe.score(X, y)
    metrics = {"accuracy" : round(accuracy,4)}

    # Parameters
    params = pipe.get_params()

    # Save pipeline
    save_pipeline_pro_perso(pipe, params, metrics)

    print(f'- metrics of the model saved : {metrics}')

    return metrics

def pred_pro_perso(X_pred: pd.DataFrame = None) -> np.ndarray:
    """
    Make a prediction of professional / personal given an X

    X must be a DataFrame with the body of the mail in a column named 'body'

    """
    # Preprocessing
    X_pred_proc = preprocessing_pro_perso(X_pred)

    # Loading the latest pipeline saved
    pipe = load_pipeline_pro_perso()

    # Prediction
    y_pred = pipe.predict(X_pred_proc['body'])

    return y_pred

if __name__ == '__main__':
    # train_spam()
    # train_pro_perso()

    test = input("Enter a message : ")

    spam = pred_spam(pd.DataFrame({"message": [test]}))
    # print(spam)
    pro_perso = pred_pro_perso(pd.DataFrame({"body": [test]}))
    d_spam = {0:"==>Not a spam", 1:"==>Spam"}
    d_pro_perso = {0:"==>Professional", 1:"==>Personal"}

    # # print("Test email:", "'"+test+"'")
    print (d_spam[spam[0]], d_pro_perso[pro_perso[0]])
