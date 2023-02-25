import numpy as np
import pandas as pd
from preprocessing import clean_email_spam,stopword_removal, preprocessing_pro_perso,preprocessing_spam
from model_spam import count_vectorizer, term_frequency,tfidf, model_spam, save_pipeline_spam, load_pipeline_spam
from model_pro_perso import vectorizer, model_pro_perso, save_pipeline_pro_perso,load_pipeline_pro_perso
from model_action_word import action_dict, is_word_present, which_word_present, which_column_present, unique_values
from model_meeting_invit import classify_meeting_invit
from model_urgent_word import urgent_vocab_dict
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

def urgent_categories(df, urgent_df=urgent_vocab_dict()):
    df['body'] = df['body'].astype(str)
    df["present"] = df.body.apply(lambda x: is_word_present(urgent_df, x))
    df["wordspresent"] = df.body.apply(lambda x: which_word_present(urgent_df, x))
    df["columnspresent"] = df.body.apply(lambda x: which_column_present(urgent_df, x))
    #if not df["present"].any():
        #return 'non urgent'
    #if df["present"].any() == False:
        #return 'non urgent'
    return df

def action_categories(df, action_df=action_dict()):
    df['body'] = df['body'].astype(str)
    df["present"] = df.body.apply(lambda x: is_word_present(action_df, x))
    df["wordspresent"] = df.body.apply(lambda x: which_word_present(action_df, x))
    df["columnspresent"] = df.body.apply(lambda x: which_column_present(action_df, x))
    return df

def pred_meeting_invit(X_pred: pd.Series = None) -> int:
    y_pred = X_pred.apply(classify_meeting_invit)
    return y_pred

if __name__ == '__main__':
    # train_spam()
    # train_pro_perso()

    # Test string
    test = input("Enter a message : ")

    # Prediction
    spam = pred_spam(pd.DataFrame({"message": [test]}))
    pro_perso = pred_pro_perso(pd.DataFrame({"body": [test]}))
    urgent_class = urgent_categories(pd.DataFrame({"body": [test]}))['present']
    #unique_urgent_class = unique_values(urgent_class['columnspresent'])
#action_class = action_categories(pd.DataFrame({"body": [test]}))
    #unique_action_class = unique_values(action_class['columnspresent'])
    #meeting = pred_meeting_invit(pd.Series(test))

    # Return
    #d_spam = {0:"==>Not a spam", 1:"==>Spam"}
    #d_pro_perso = {0:"==>Professional", 1:"==>Personal"}
    #d_meeting_invit = {0:"==>Not a meeting invit", 1:"==>Meeting invitation"}


    #print (d_spam[spam[0]], d_pro_perso[pro_perso[0]],unique_urgent_class, unique_action_class, d_meeting_invit[meeting[0]])
    print(urgent_class)
