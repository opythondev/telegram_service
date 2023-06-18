FROM python:3.11.3-slim-bullseye

WORKDIR /code

COPY ./ ./

RUN pip install --upgrade pip wheel setuptools && pip install --upgrade -r requirements.txt

CMD ["python", "main.py"]
