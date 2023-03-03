FROM python:3.8.6-buster
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY thetidinbox_1004 /thetidinbox_1004
COPY setup.py setup.py
RUN pip install .

# RUN python -c "import nltk ; nltk.download('all')"
RUN python -m nltk.downloader -d /usr/local/nltk_data all

CMD uvicorn thetidinbox_1004.api.fast:app --host 0.0.0.0 --port $PORT
