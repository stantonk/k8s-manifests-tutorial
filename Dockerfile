FROM python:latest

RUN mkdir -p /srv

WORKDIR /srv

COPY requirements.txt /srv/requirements.txt
COPY rest.py /srv/rest.py

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "rest.py"]
