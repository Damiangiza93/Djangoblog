FROM python:3.8

RUN mkdir /app
WORKDIR /app
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV PORT=8000
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# install environment dependencies
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv
RUN pip3 install Pillow

RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD gunicorn django_project.wsgi:application --bind 0.0.0.0:$PORT