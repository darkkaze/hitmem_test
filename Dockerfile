FROM python:3.9
ENV PYTHONUNBUFFERED=1

WORKDIR /project
COPY requirements.txt /project/
RUN pip install -r requirements.txt
COPY . /project/

RUN python manage.py migrate
RUN python manage.py loaddata apps/users/fixtures/users.json
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]