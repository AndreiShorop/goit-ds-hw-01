FROM python:3.13.5
WORKDIR /app

RUN pip install pipenv


COPY Pipfile Pipfile.lock* ./


RUN pipenv install --system --deploy --ignore-pipfile || pipenv install --system --skip-lock


COPY . .


CMD ["python", "bot.py"]