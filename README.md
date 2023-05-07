# Data analysis
- Document here the project: thetidinbox_1004
- Description: Email classification and to-do list extraction using NLP
  - Emails classified into spam / ham
  - Ham emails classified into professional / personal
  - To-do list generation using Name Entity Recognition from Spacy package
  - Topic classification for personal emails using BerTopic
- Data Source:
  - Enron dataset (Kaggle)
  - Spam / ham dataset (Kaggle)
  - Conversational dataset (Kaggle)
- Type of analysis:
  - NLP
  - Transfer Learning
  - Name Entity Recognition (Spacy)

Please document the project the better you can.

# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for thetidinbox_1004 in github.com/mlerend. If your project is not set please add it:

Create a new project on github.com/mlerend/thetidinbox_1004
Then populate it:

```bash
git remote add origin git@github.com:mlerend/thetidinbox_1004.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
thetidinbox_1004-run
```

# Install

Go to `https://github.com/mlerend/thetidinbox_1004` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:mlerend/thetidinbox_1004.git
cd thetidinbox_1004
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
thetidinbox_1004-run
```

Connect to your Gmail inbox :
- Follow Google instructions : [Go the instructions ](https://developers.google.com/gmail/api/quickstart/python?hl=fr)
- Save the credentials.json in 'thetidinbox_1004/streamlitapp'

Launch the streamlit app:

```bash
streamlit run  streamlitapp/importst.py
```
