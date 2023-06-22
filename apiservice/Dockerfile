FROM python:3.11.3-slim-bullseye

WORKDIR /code

COPY ./ ./

RUN pip install --upgrade pip wheel setuptools && pip install --upgrade -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
