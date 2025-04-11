FROM python:3.10.12

ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

# # CMD python manage.py runserver
# CMD ["python","manage.py","runserver", "0.0.0.0:8000"]
