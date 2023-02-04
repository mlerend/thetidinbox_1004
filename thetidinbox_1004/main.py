from data import populate_df
<<<<<<< HEAD
import numpy as np
import pandas as pd
from email_preprocessing import clean_email, preproces_email,stopword_removal
from model import count_vectorizer, term_frequency, model, save_pipeline, load_pipeline
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from math import sqrt
=======
from email_preprocessing import clean_email, stopword_removal
>>>>>>> 05b26d8c035ca2b8b3d54d113b7768a803047361


def preprocessing():

    path_data = '../raw_data/enron1.tar.gz'

    emails_df = populate_df(path_data)
    # Translate bytes objects into strings.
    emails_df['message'] = emails_df['message'].apply(lambda x: x.decode('latin-1'))

    # Reset pandas df index.
    emails_df = emails_df.reset_index(drop=True)

    # Map 'spam' to 1 and 'ham' to 0
    emails_df['class'] = emails_df['class'].map({'spam': 1, 'ham': 0})

    emails_df['message'] = emails_df['message'].apply(clean_email)
    emails_df['message'] = emails_df['message'].apply(stopword_removal)

    return emails_df

def train():

    # Pipeline definition
    pipe = Pipeline([('vectorize', count_vectorizer()),
                 ('tfidf', term_frequency()),
                 ('classify', model())])

    # X and y definition
    emails_df = preprocessing()
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
    save_pipeline(pipe, params, metrics)

    print(f'- metrics of the model saved : {metrics}')

    return metrics

def pred(X_pred: pd.DataFrame = None) -> np.ndarray:
    """
    Make a prediction of spam / ham given an X

    X must be a DataFrame with the body of the mail in a column named 'message'

    """
    # Preprocessing
    X_pred.dropna()
    X_pred.drop_duplicates(keep='first',inplace=True)

    # Translate bytes objects into strings.
    X_pred['message'] = X_pred['message'].apply(lambda x: x.decode('latin-1'))

    # Reset pandas df index.
    X_pred = X_pred.reset_index(drop=True)

    # Applying preprocessing feature
    X_pred['message'] = X_pred['message'].apply(clean_email)
    X_pred['message'] = X_pred['message'].apply(preproces_email)
    X_pred['message'] = X_pred['message'].apply(stopword_removal)

    # Loading the latest pipeline saved
    pipe = load_pipeline()

    # Prediction
    y_pred = pipe.predict(X_pred['message'])

    return y_pred

if __name__ == '__main__':
    preprocessing()
    train()
    X_pred = populate_df('../raw_data/enron1.tar.gz').sample(1)
    print(pred(X_pred))
