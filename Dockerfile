FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn  # production server

COPY app app
COPY migrations migrations
COPY main.py config.py boot.sh ./
RUN chmod a+x boot.sh # maakt bootscript uitvoerbaar

ENV FLASK_APP main.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]