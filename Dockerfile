FROM python:latest

RUN mkdir -p /srv

WORKDIR /srv

COPY rest.py /srv/rest.py

RUN pip install flask

EXPOSE 5000

CMD ["python", "rest.py"]
