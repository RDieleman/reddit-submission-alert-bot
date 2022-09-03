FROM python:3.10-slim

WORKDIR /alert-bot

COPY . .

RUN pip install pipenv && \
  pipenv install --deploy --system && \
  pip uninstall pipenv -y

CMD ["python", "main.py"]