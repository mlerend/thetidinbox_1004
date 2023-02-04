import re
from string import punctuation
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

def clean_email(email):

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

def preproces_email(email):

    words = ""
    # Create the stemmer.
    stemmer = SnowballStemmer("english")
    # Split text into words.
    email = email.split()
    for word in email:
        # Optional: remove unknown words.
        words = words + stemmer.stem(word) + " "

    return words

def stopword_removal(email):

    stop_words = set(stopwords.words('english'))

    email = email.split()
    filtered_sentence = ""

    for w in email:
        if w not in stop_words:
            filtered_sentence = filtered_sentence + w +" "

    return filtered_sentence
