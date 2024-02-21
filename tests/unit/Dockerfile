FROM python:3.12-slim

RUN mkdir /app
WORKDIR /app
COPY ./tests/unit/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY . .

CMD ["pytest", "-v", "."]
