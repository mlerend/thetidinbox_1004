import tarfile
import pandas as pd
import requests
import mailparser
import re
import os
import email

def extract_emails(fname):
    """ Extract the zipped emails and load them into a pandas df """

    rows = []
    # tarfiles are used to read and write tar archives
    originalfile = tarfile.open(fname, 'r:gz')
    for member in originalfile.getmembers():
        if 'ham' in member.name:
            f = originalfile.extractfile(member)
            if f is not None:
                row = f.read()
                rows.append({'message': row, 'class': 'ham'})
        if 'spam' in member.name:
            f = originalfile.extractfile(member)
            if f is not None:
                row = f.read()
                rows.append({'message': row, 'class': 'spam'})
    originalfile.close()

    return pd.DataFrame(rows)

def populate_df(path: str):
    """ Populate the dataframe with all the emails """

    enron_files = path
    emails_df = pd.DataFrame({'message': [], 'class': []})

    unzipped_file = extract_emails(enron_files)
    emails_df = pd.concat([emails_df,unzipped_file])

    # Dropping all the rows with NA values
    emails_df.dropna()
    # Dropping all the duplicates but keeping the first instance
    emails_df.drop_duplicates(keep='first',inplace=True)

    return emails_df

def ham_spam_extended_dataset():

    ham_fnames = [name for name in sorted(os.listdir("../raw_data/main_ham"))]
    spam_fnames = [name for name in sorted(os.listdir("../raw_data/main_spam"))]

    def parse_email(fname, spam=False):
        directory = "../raw_data/main_spam" if spam else "../raw_data/main_ham"
        with open(os.path.join(directory, fname), "rb") as fp:
            return email.parser.BytesParser().parse(fp)

    ham_emails = [parse_email(name) for name in ham_fnames]
    spam_emails = [parse_email(name, spam=True) for name in spam_fnames]
    ham_emails_content = [email.get_payload() for email in ham_emails]
    spam_emails_content = [email.get_payload() for email in spam_emails]
    ham_df = pd.DataFrame({"message" : ham_emails_content, "class" : 0})
    spam_df = pd.DataFrame({"message" : spam_emails_content, "class" : 1})
    ham_spam_temp_df = pd.concat([ham_df, spam_df])

    return ham_spam_temp_df

def conversational_for_spam(sample=20000):
    r = requests.get('https://raw.githubusercontent.com/alexa/Topical-Chat/master/conversations/train.json').json()

    message_l = []
    for key in r.keys():
        for message in r[key]['content']:
            message_l.append(message["message"])
    conv_message_one_df = pd.DataFrame({"message":message_l, "class":0}).sample(sample)
    conv_message_one_df.head()

    return conv_message_one_df

def conversational_messages(n=20000):
    """ Import the conversational messages from Kaggle and Github
    Input :
    - n : number of messages to take from each dataset, format : int

     """

    # Importing first conversational messages dataset from github
    r = requests.get('https://raw.githubusercontent.com/alexa/Topical-Chat/master/conversations/train.json').json()
    message_l = []
    for key in r.keys():
        for message in r[key]['content']:
            message_l.append(message["message"])
    conv_message_one_df = pd.DataFrame({"body":message_l})

    # Importing second conversational messages dataset from kaggle
    path_train = '../raw_data/conv_messages_train.csv'
    path_test = '../raw_data/conv_messages_test.csv'
    conv_message_two_df_train = pd.read_csv(path_train)
    conv_message_two_df_test = pd.read_csv(path_test)
    conv_message_two_raw_df = pd.concat([conv_message_two_df_test, conv_message_two_df_train]).reset_index(drop=True)
    mess = []
    for i in range(0,len(conv_message_two_raw_df)):
        mess.append("".join(conv_message_two_raw_df.loc[i,"personas"]).replace("[","").replace("]","").replace("'",""))
        mess.append("".join(conv_message_two_raw_df.loc[i,"previous_utterance"]).replace("[","").replace("]","").replace("'",""))
        mess.append("".join(conv_message_two_raw_df.loc[i,"free_messages"]).replace("[","").replace("]","").replace("'",""))
        mess.append("".join(conv_message_two_raw_df.loc[i,"guided_messages"]).replace("[","").replace("]","").replace("'",""))
    conv_message_two_df = pd.DataFrame({"body":mess})

    # Concatenating conversational messages datasets
    conv_message_df = pd.concat([conv_message_one_df.sample(n), conv_message_two_df.sample(n)]).reset_index(drop=True)

    # Affecting category 1 to conversational messages
    conv_message_df["category"] = 1

    return conv_message_df

def originally_labeled_emails_dataset():
    """ Importing labeled emails from the Enron dataset already labeled in 8 categories """

    emails_df = pd.DataFrame({"message" : [],
                         "category" : []})
    for i in range(1,9):
        path_data = f'../raw_data/enron/emails/txt_files_categories/all_txt_files{i}.txt'
        with open(path_data) as f:
            contents = f.read()
            emails_cat = ["Message-ID: " + email for email in contents.split("Message-ID: ") if email]
            emails_df = pd.concat([emails_df, pd.DataFrame({"message" : emails_cat,
                            "category" : int(i)})]).reset_index(drop=True)

    return emails_df

################### Fonctions for parsing emails (i.e. identifying the date, sender, recipients etc)#################
def extract_date(email):
    mail = mailparser.parse_from_string(email)
    date = mail.date
    return date

def extract_sender(email):
    mail = mailparser.parse_from_string(email)
    if len(mail.from_) > 0:
        sender = mail.from_[0][1]
    else:
        sender = mail.from_
    return sender

def extract_recipients(email):
    mail = mailparser.parse_from_string(email)
    if len(mail.to) > 0:
        to = ",".join([rec[1] for rec in mail.to])
    else:
        to = mail.to
    return to

def extract_header(email):
    mail = mailparser.parse_from_string(email)
    header = mail.subject
    return header

def extract_body(email):
    mail = mailparser.parse_from_string(email)
    body = mail.body
    return body

def parsing(emails_df):
    """From a raw email in text format, separating each part of the email into a dataframe column :
    Id, date, from, to, header, body
    """
    emails_df_parsed = pd.DataFrame()
    emails_df_parsed["ID"] = emails_df["message"].apply(lambda x: re.search(r'\d+',x)[0])
    emails_df_parsed["date"] = emails_df["message"].apply(extract_date)
    emails_df_parsed["from"] = emails_df["message"].apply(extract_sender)
    emails_df_parsed["to"] = emails_df["message"].apply(extract_recipients)
    emails_df_parsed["header"] = emails_df["message"].apply(extract_header)
    emails_df_parsed["body"] = emails_df["message"].apply(extract_body)
    emails_df_parsed["category"] = emails_df["category"]
    return emails_df_parsed

################################ End parsing #############################################################################


def model_labeled_emails_dataset():
    """ Importing emails from the Enron dataset labeled by the baseline model """

    emails_model_df = pd.read_csv("../raw_data/new_emails_labeled.csv")
    emails_model_df["category"] = 0
    return emails_model_df

def business_emails_parsed():
    emails_df = originally_labeled_emails_dataset()
    emails_df_parsed = parsing(emails_df)
    emails_business_df = emails_df_parsed[emails_df_parsed["category"].isin([1,4,5,6])][["body","category"]]
    emails_business_df["category"] = 0
    return emails_business_df

def pro_perso_dataset():
    emails_business_df = business_emails_parsed()
    emails_model_df = model_labeled_emails_dataset()
    conv_message_df = conversational_messages()
    df = pd.concat([emails_business_df,emails_model_df[["body","category"]],conv_message_df], axis=0).reset_index(drop=True)
    return df
