from __future__ import print_function

import numpy as np
import spacy
import time
import streamlit as st
import pandas as pd
import email
import re

import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import pandas as pd

# APP SETTINGS
## page config
st.set_page_config(
    page_title="Tidinbox demo",
    page_icon="📨",
    layout="wide",
    initial_sidebar_state="expanded",)

## sidebar config
st.sidebar.title("Navigation")

my_messy_inbox = st.sidebar.button("📨  My Messy Inbox")
my_tidy_inbox = st.sidebar.button("🦸‍♀️  My Tidy Inbox")
my_to_do_list = st.sidebar.button("✅  My To-Do List")

# MAIN PAGE CONTENT
## banner config
st.image("banner.png", width=None)

## call out config
st.markdown("""
<h1 style='padding-top: 20px; text-align: left; font-size: 30px;'>
    Welcome back, <i style='color: #67ff94;'>Very Busy Wagoner 👋</i>
</h1>
""", unsafe_allow_html=True)

st.markdown("""               """)
st.write("""
<div style="padding: 10px; background-color: #374E75;">
  📨  Transform your <strong>cluttered inbox</strong> into <strong>a productive hub</strong> with NLP-powered email pre-processing solution.
  <br> Extract key info and actions to generate a suggested to-do list, <strong>saving you time and boosting efficiency</strong>.</div>""", unsafe_allow_html=True)

## key insights config
st.markdown("""               """)
with st.spinner('Loading...'):
    time.sleep(1)

st.markdown("""               """)

with st.expander("""What happened since your last login **[2023-03-03 19:04:32]**"""):

    ## made up metrics config 😇
    col1, col2, col3 = st.columns(3)

    col1.write("##### 📩 Unread")
    col2.write("##### 📥 Action-required ")
    col3.write("##### ❗ Urgent ")

    col1.metric(label="#### 📩 Unread mails", value="202", delta="34",delta_color="inverse")
    col2.metric("#### 📥 Action-required emails", "12",  "4")
    col3.metric("#### ❗ Urgent emails", "6", "2")
    #st.metric(label="Unread mails", value="202", delta="34",delta_color="inverse")

st.markdown("""               """)
st.markdown("""               """)
st.markdown("""               """)

#tab1, tab2, tab3 = st.tabs(["📨  My Messy Inbox", "🦸‍♀️  My Tidy Inbox", "✅  My To-Do List"])

# MY MESSY INBOX CONTENT
if my_messy_inbox:
        #tab1.active = True
        st.subheader("📨 My Messy Inbox")
        st.write("""
    <div style="padding: 10px; background-color: #374E75;">
    Here are your <strong><red> ❌ 202 ❌ </red></strong>unread emails: My <strong>Messy</strong> Inbox </div>""", unsafe_allow_html=True)
        st.markdown("""               """)


        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


        def google_api():

            """Read the unread emails of verybusywagoner@gmail.com.
            Needs the file 'credentials.json' in the same folder as this script to work.
            At first utilisation, you need to click on the link displayed and confirm the access. Once done, re-execute the code.
            A token.json file is then automatically generated in the folder and the code should work just fine.
            """
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            try:
                # Call the Gmail API
                service = build('gmail', 'v1', credentials=creds)
                results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
                messages = results.get('messages', [])
                num_unread = len(messages)


                if not messages:
                    print('No labels found.')
                    return
                email_data = []
                for message in messages:
                    msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
                    msg_str = msg['raw'].encode('utf-8')
                    msg_str = base64.urlsafe_b64decode(msg_str).decode('utf-8')
                    msg = email.message_from_string(msg_str)
                    sender = msg['From']
                    sender = re.search(r'<(.*)>', sender).group(1)
                    date = msg['Date']
                    subject = msg['Subject']

                    # Check if the payload is a multipart message
                    if msg.is_multipart():
                        body = msg.get_payload()[0].get_payload()
                    else:
                        body = msg.get_payload()

                    email_data.append((date, sender, subject, body))

                return email_data


            except HttpError as error:
                # TODO(developer) - Handle errors from gmail API.
                print(f'An error occurred: {error}')

        if __name__ == '__main__':
            email_data = google_api()
            if email_data:
                df = pd.DataFrame(email_data, columns=["Date", "Sender", "Subject", "Body"])
                st.dataframe(df)
            else:
                st.write("No unread emails found.")


    # Display the number of unread messages in the Streamlit app
    #st.write("My Messy Inbox")
    #st.write("You have {} unread messages in your inbox.".format(unread_count))




### This is the code for the section "my tidy inbox"

elif my_tidy_inbox:
        #tab2.active = True
        st.subheader("🦸‍♀️ My Tidy Inbox")
        col4, col5 = st.columns(2)

        col4.write("""<div style="padding: 10px; background-color: #374E75;">  How to handle those overwhelming <strong><red> ❌ 202 ❌ </red></strong>unread emails ?  </div>""", unsafe_allow_html=True)
        col5.write("""<div style="padding: 10px; background-color: #374E75;"> Filter your way to laser-sharp focus thanks to <strong>Tidinbox</strong> !</div>""", unsafe_allow_html=True)

        st.markdown("""               """)
        st.write("""<div style="padding: 10px; background-color: #374E75;">  Select email filters that match your priorities and see what truly needs your attention : </div>""", unsafe_allow_html=True)

        st.markdown("""               """)
        st.markdown("""               """)
        # create a sample dataframe with messages and tags

        # define the available filter categories and their corresponding binary filters
        filter_categories = {
            'Spam/Not Spam': {'Not Spam': 'ham','Spam': 'spam'},
            'Personal/Professional': {'Professional': 'professional', 'Personal': 'personal'},
            'Urgent/Not Urgent': {'Urgent': 'do it now', 'Not Urgent': 'not urgent'},
            'Infos/Action-Required': {'Action-Required': 'action-required', 'Informative': 'informative'}
        }

        # create a container for the filters
        filters_container = st.container()

        # create a horizontal layout for the filter section
        filters_col1, filters_col2, filters_col3, filters_col4 = filters_container.columns(4)

        # create a radio widget for each binary filter
        # create a radio widget for each binary filter
        with filters_col1:
            selected_filter_1 = st.radio('Spam/Not Spam', options=list(filter_categories['Spam/Not Spam'].keys()))

        with filters_col2:
            selected_filter_2 = st.radio('Personal/Professional', options=list(filter_categories['Personal/Professional'].keys()))

        with filters_col3:
            selected_filter_3 = st.radio('Urgent/Not Urgent', options=list(filter_categories['Urgent/Not Urgent'].keys()))

        with filters_col4:
            selected_filter_4 = st.radio('Infos/Action-Required', options=list(filter_categories['Infos/Action-Required'].keys()))


        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

        st.markdown("""               """)
        st.markdown("""               """)

        st.markdown("""               """)
        def google_api():

            """Read the unread emails of verybusywagoner@gmail.com.
            Needs the file 'credentials.json' in the same folder as this script to work.
            At first utilisation, you need to click on the link displayed and confirm the access. Once done, re-execute the code.
            A token.json file is then automatically generated in the folder and the code should work just fine.
            """
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())

            try:
                # Call the Gmail API
                service = build('gmail', 'v1', credentials=creds)
                results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
                messages = results.get('messages', [])
                num_unread = len(messages)


                if not messages:
                    print('No labels found.')
                    return
                email_data = []
                for message in messages:
                    msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
                    msg_str = msg['raw'].encode('utf-8')
                    msg_str = base64.urlsafe_b64decode(msg_str).decode('utf-8')
                    msg = email.message_from_string(msg_str)
                    sender = msg['From']
                    sender = re.search(r'<(.*)>', sender).group(1)
                    date = msg['Date']
                    subject = msg['Subject']

                    # Check if the payload is a multipart message
                    if msg.is_multipart():
                        body = msg.get_payload()[0].get_payload()
                    else:
                        body = msg.get_payload()

                    email_data.append((date, sender, subject, body))

                return email_data


            except HttpError as error:
                # TODO(developer) - Handle errors from gmail API.
                print(f'An error occurred: {error}')

        if __name__ == '__main__':
            email_data = google_api()
            if email_data:
                df = pd.DataFrame(email_data, columns=["Date", "Sender", "Subject", "Body"])
            else:
                st.write("No unread emails found.")

        data1 = {
            'tags':
                ['ham, personal, not urgent, action-required',
                     'spam',
                     'spam',
                     'spam',
                     'spam',
                     'ham, professional, do it now, action-required',
                     'ham, professional, not urgent, action-required',
                     'ham, professional, not urgent, informative',
                     'ham, professional, not urgent, action-required',
                     'ham, professional, not urgent, action-required',
                     'ham, professional, not urgent, action-required',
                     'ham, professional, do it now, action-required',
                     'ham, professional, do it now, action-required',
                     'ham, professional, do it now, action-required',
                     'ham, professional, not urgent, action-required',
                     'ham, professional, not urgent, action-required',
                     'ham, professional, do it now, action-required',
                     'ham professional, not urgent, action-required',
                     'ham, professional, do it now, action-required',
                     'ham, professional, not urgent, action-required',
                     'ham, professional, do it now, action-required',
                     'ham, professional, not urgent, action-required',
                     'ham, professional, not urgent, action-required',
                     'ham, professional, do it now, action-required',
                     'ham, professional, do it now, action-required',
                     'spam',
                     'ham, personal, not urgent, action-required',
                     'spam',
                     'spam',
                     'spam',
                     'ham, personal, not urgent, informative']
        }

        df1 = pd.DataFrame(data1)
        df2 = pd.concat([df, df1], axis=1)
        df2 = df2.loc[df2["tags"] != "spam"]

        st.markdown("""               """)
        st.dataframe(df2)


### This is the code for the section "my to-do list"
elif my_to_do_list:
        #tab3.active = True
        st.subheader("✅  My To-Do List")
        options = st.multiselect(
    'Selected filters : ',
    ['not a spam', 'ham', 'professional', 'personal', 'do it now', 'not urgent', 'action-required', 'informative'],
    ['not a spam', 'professional','do it now', 'action-required'])

# If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

        def google_api1():

                    """Read the unread emails of verybusywagoner@gmail.com.
                    Needs the file 'credentials.json' in the same folder as this script to work.
                    At first utilisation, you need to click on the link displayed and confirm the access. Once done, re-execute the code.
                    A token.json file is then automatically generated in the folder and the code should work just fine.
                    """
                    creds = None
                    # The file token.json stores the user's access and refresh tokens, and is
                    # created automatically when the authorization flow completes for the first
                    # time.
                    if os.path.exists('token.json'):
                        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                    # If there are no (valid) credentials available, let the user log in.
                    if not creds or not creds.valid:
                        if creds and creds.expired and creds.refresh_token:
                            creds.refresh(Request())
                        else:
                            flow = InstalledAppFlow.from_client_secrets_file(
                                'credentials.json', SCOPES)
                            creds = flow.run_local_server(port=0)
                        # Save the credentials for the next run
                        with open('token.json', 'w') as token:
                            token.write(creds.to_json())

                    try:
                        # Call the Gmail API
                        service = build('gmail', 'v1', credentials=creds)
                        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
                        messages = results.get('messages', [])
                        num_unread = len(messages)


                        if not messages:
                            print('No labels found.')
                            return
                        text_input = []
                        for message in messages:
                            msg = service.users().messages().get(userId='me', id=message['id'], format='raw').execute()
                            msg_str = msg['raw'].encode('utf-8')
                            msg_str = base64.urlsafe_b64decode(msg_str).decode('utf-8')
                            msg = email.message_from_string(msg_str)
                            sender = msg['From']
                            sender = re.search(r'<(.*)>', sender).group(1)
                            date = msg['Date']
                            subject = msg['Subject']

                            # Check if the payload is a multipart message
                            if msg.is_multipart():
                                body = msg.get_payload()[0].get_payload()
                            else:
                                body = msg.get_payload()

                            text_input.append((body))

                        return text_input


                    except HttpError as error:
                    # TODO(developer) - Handle errors from gmail API.
                        print(f'An error occurred: {error}')

        if __name__ == '__main__':
            text_input = google_api1()


        def generate_to_do(text_input):
            # Load the pre-trained NER model
            nlp = spacy.load("en_core_web_sm")

            # Process the text input
            doc = nlp(text_input)

            # Extract named entities
            entities = [ent.text for ent in doc.ents]

            # Extract the person mentioned in the text
            person = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

            # Extract the action verb in the text
            action_verb = [token.text for token in doc if token.pos_ == "VERB"]

            # To Do Generation
            if any(verb in action_verb for verb in ["provide", "update"]):
                if any(word in text_input for word in ["tasks", "task", "current tasks"]):
                    to_do = "Provide updates on current tasks to {}".format(person[0]) if person else "Provide updates on current tasks"
                elif any(word in text_input for word in ["project", "current project"]):
                    to_do = "Provide updates on the current project to {}".format(person[0]) if person else "Provide updates on the current project"
                elif any(word in text_input for word in ["status", "project status"]):
                    to_do = "Update the project status"
                else:
                    to_do = "Provide informations"
            elif any(verb in action_verb for verb in ["request", "provide"]):
                if "feedback" in text_input:
                    to_do = "Provide feedback"
                elif any(word in text_input for word in ["approval", "approve"]):
                    if any(word in text_input for word in ["purchase", "software license"]):
                        to_do = "Approve a purchase requested by {}".format(person[0]) if person else "Approve purchases"
                    elif any(word in text_input for word in ["training request", "training"]):
                        to_do = "Approve {}'s training request".format(person[0]) if person else "Approve training requests"
                    elif any(word in text_input for word in ["PTO request", "PTO"]):
                        to_do = "Approve {}'s PTO request".format(person[0]) if person else "Approve PTO requests"
                    elif any(word in text_input for word in ["payment request", "payment"]):
                        to_do = "Approve {}'s payment request".format(person[0]) if person else "Approve payment requests"
                else:
                    to_do = "Approve {}'s inputs".format(person[0])
            elif any(verb in action_verb for verb in ["confirm"]):
                if "delivery" in text_input:
                    to_do = "Confirm a delivery from {}".format(person[0]) if person else "Confirm upcoming delivery"
                else:
                    to_do = "Confirm {}'s request".format(person[0])
            elif any(verb in action_verb for verb in ["respond"]):
                if "customer inquiry" in text_input:
                    to_do = "Respond to a customer inquiry submitted by {}".format(person[0]) if person else "Respond to a customer inquiry"
                else:
                    to_do = "Get back to {}".format(person[0])
            elif any(verb in action_verb for verb in ["schedule", "appoint", "arrange", "organize", "plan", "programme"]):
                if any(word in text_input for word in ["call", "discuss", "meeting"]):
                    to_do = "Schedule a meeting with {}".format(person[0]) if person else "Schedule upcoming meeting"
                elif "business trip" in text_input:
                    to_do = "Schedule a business trip with {}".format(person[0]) if person else "Schedule upcoming business trip"
                elif "training" in text_input:
                    to_do = "Schedule a training session for {}".format(person[0]) if person else "Schedule upcoming training session"
                elif any(word in text_input for word in ["business lunch", "lunch"]):
                    to_do = "Schedule a business lunch with {}".format(person[0]) if person else "Schedule upcoming business lunch"
                else:
                    to_do = "Schedule newt steps with {}".format(person[0])
            elif any(verb in action_verb for verb in ["accept"]):
                to_do = "Accept a meeting invitation from {}".format(person[0]) if person else "Accept meeting invitations"
            elif any(verb in action_verb for verb in ["prepare"]):
                to_do = "Prepare for the meeting with {}".format(person[0]) if person else "Prepare for the upcoming meeting"
            elif any(verb in action_verb for verb in ["postpone"]):
                to_do = "Postpone a meeting with {}".format(person[0]) if person else "Postpone the upcoming meeting"
            elif any(verb in action_verb for verb in ["send"]):
                if "reminder" in text_input:
                    to_do = "Send a reminder for the upcoming meeting to {}".format(person[0]) if person else "Send a reminder for the upcoming meeting"
                else:
                    to_do = "Double check {}'s meeting proposal".format(person[0])
            elif any(verb in action_verb for verb in ["join"]):
                if any(word in text_input for word in ["lunch"]):
                    to_do = "Join {} for lunch".format(person[0]) if person else "Book lunch time"
                else:
                    to_do = "Join {} for the upcoming meeting".format(person[0]) if person else "Attend upcoming meeting"

            elif any(verb in action_verb for verb in ["have", "discuss"]):
                to_do = "Set up a chat with {}".format(person[0]) if person else "Set up a chat about demo day"
            elif any(verb in action_verb for verb in ["provide"]):
                if "feedback" in text_input:
                    to_do = "Provide feedback on the latest project report to {}".format(person[0]) if person else "Provide feedback on the latest project report"
                else:
                    to_do = "Follow-up with {}"
            else:
                to_do = "No to do found"

            return to_do

        to_do_list = []
        for text in text_input:
            text = text.replace("\n", " ")
            to_do = "❗ " + generate_to_do(text)
            if to_do != '❗ No to do found':
                to_do_list.append([to_do,text,False])

        to_do_df = pd.DataFrame(to_do_list, columns=["To Do","email","done"])
        #to_do_df["done"] = st.checkbox(to_do_df['To Do'], to_do_df['done'])

        styled_df = (to_do_df.style
            .apply(lambda x: ['background-color: #374E75' if x.name == 'To Do' else '' for i in x], axis=0)
            .set_caption("To Do List")
        )
        st.markdown("""               """)
        st.markdown("""               """)

        st.dataframe(styled_df)
