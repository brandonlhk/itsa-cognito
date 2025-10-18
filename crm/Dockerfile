FROM python:3.12-slim as base
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy --system
COPY ./app ./app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]