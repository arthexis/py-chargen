FROM python:3.8.1-buster

COPY requirements.txt /tmp
RUN pip install /tmp/requirements.txt

COPY chargen /app

ENTRYPOINT ["uvicorn", "app:app"]
