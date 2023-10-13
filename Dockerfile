FROM tiangolo/uwsgi-nginx-flask:python3.9

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
