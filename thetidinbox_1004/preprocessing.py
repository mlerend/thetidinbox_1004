import re
from string import punctuation

import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from thetidinbox_1004.data import (conversational_for_spam,
                                   ham_spam_extended_dataset, populate_df)


def clean_email_spam(email):

    # Remove mentions
    email = re.sub(r'@\w+', '', email)
    # Remove urls
    email = re.sub(r'http\S+', ' ', email)
    # Remove digits
    email = re.sub("\d+", " ", email)
    email = email.replace('\n', ' ')
    # Remove punctuations
    email = email.translate(str.maketrans("", "", punctuation))
    email = email.lower()

    return email


def stopword_removal(email):

    stop_words = set(stopwords.words('english'))

    email = email.split()
    filtered_sentence = ""

    for w in email:
        if w not in stop_words:
            filtered_sentence = filtered_sentence + w +" "

    return filtered_sentence

def preprocessing_spam():

    path_data = '../raw_data/enron1.tar.gz'

    # Picking the dataset to preprocess
        #Enron emails
    emails_df = populate_df(path_data)
    emails_df = emails_df.reset_index(drop=True)
    emails_df['class'] = emails_df['class'].map({'spam': 1, 'ham': 0})

        #Ham_Spam extended dataset
    ham_spam_temp_df = ham_spam_extended_dataset()

        #Sample of conversational messages
    conv_message_one_df = conversational_for_spam()

        #Concatenating the sample
    ham_spam_df = pd.concat([emails_df,ham_spam_temp_df,conv_message_one_df]).reset_index(drop=True)

    # Translate bytes objects into strings.
    try:
        ham_spam_df['message'] = ham_spam_df['message'].apply(lambda x: x.decode('latin-1'))
    except (UnicodeDecodeError, AttributeError):
        pass

    ham_spam_df["message"] = ham_spam_df["message"].astype(str)

    # Map 'spam' to 1 and 'ham' to 0

    ham_spam_df['message'] = ham_spam_df['message'].apply(clean_email_spam)
    ham_spam_df['message'] = ham_spam_df['message'].apply(stopword_removal)

    return ham_spam_df


def clean_email_pro_perso(email):

    # Remove mentions
    email = re.sub(r'@\w+', '', email)
    # Remove urls
    email = re.sub(r'http\S+', ' ', email)
    # Remove digits
    email = re.sub("\d+", " ", email)
    # Remove backline character
    email = email.replace('\n', ' ')
    # Remove digits between brackets
    email = re.sub(r'<.*>', '', email)
    # Remove punctuations
    email = email.translate(str.maketrans(" ", " ", punctuation))
    email = email.lower()
    # Remove some keyword
    elements_to_drop = ['Message-ID:', 'Date:', 'From:', 'To:', 'Subject:', 'Cc:', 'Mime-Version:',
     'Content-Type:', 'Content-Transfer-Encoding:', 'Bcc:', 'X-From:', 'X-To:', 'X-cc:', 'X-bcc:',
     'X-Folder:', 'X-Origin:', 'X-FileName:', 'cc', '\t', '--', 'Sent', ' --', '-', '/', '\n', 'Re:', 'FW:']
    for element in elements_to_drop:
        email = email.replace(element, ' ')

    return email

def tokenizing(email):
    email = word_tokenize(email)
    return email

def lemmatizing(email):

    # 1 - Lemmatizing the verbs
    verb_lemmatized = [
    WordNetLemmatizer().lemmatize(word, pos = "v") # v --> verbs
    for word in email
    ]

    # 2 - Lemmatizing the nouns
    noun_lemmatized = [
    WordNetLemmatizer().lemmatize(word, pos = "n") # n --> nouns
    for word in verb_lemmatized
    ]

    return noun_lemmatized

def preprocessing_pro_perso(df):
    df_cleaned = df.loc[df["body"].notna()]
    df_cleaned["body"] = df_cleaned["body"].apply(clean_email_pro_perso)
    df_cleaned["body"] = df_cleaned["body"].apply(stopword_removal)
    df_cleaned["body"] = df_cleaned["body"].apply(tokenizing)
    df_cleaned["body"] = df_cleaned["body"].apply(lemmatizing)
    df_cleaned = df_cleaned[df_cleaned["body"].map(lambda d: len(d)) > 0]
    df_cleaned["body"] = df_cleaned["body"].apply(lambda x: " ".join(x))
    return df_cleaned
