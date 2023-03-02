FROM python:3.8.6-buster
COPY thetidinbox_1004 /thetidinbox_1004
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn thetidinbox_1004.api.fast:app --host 0.0.0.0
