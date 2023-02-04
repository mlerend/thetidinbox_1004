from data import populate_df
from email_preprocessing import clean_email, preproces_email,stopword_removal


def preprocessing(path_data):

    emails_df = populate_df(path_data)
    # Translate bytes objects into strings.
    emails_df['message'] = emails_df['message'].apply(lambda x: x.decode('latin-1'))

    # Reset pandas df index.
    emails_df = emails_df.reset_index(drop=True)

    # Map 'spam' to 1 and 'ham' to 0
    emails_df['class'] = emails_df['class'].map({'spam': 1, 'ham': 0})

    emails_df['message'] = emails_df['message'].apply(clean_email)
    emails_df['message'] = emails_df['message'].apply(preproces_email)
    emails_df['message'] = emails_df['message'].apply(stopword_removal)

    return emails_df

if __name__ == '__main__':
    preprocessing(path_data = '../raw_data/enron1.tar.gz')
