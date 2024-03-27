FROM python:slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn psycopg2-binary # production server

COPY app app
COPY fill_db_with_faker fill_db_with_faker
COPY migrations migrations
COPY main.py config.py boot.sh ./
RUN chmod a+x boot.sh # maakt bootscript uitvoerbaar

ENV FLASK_APP main.py


EXPOSE 5000
ENTRYPOINT ["./boot.sh"]