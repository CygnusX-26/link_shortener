FROM python:3.11-slim

RUN useradd -r flask
USER flask


COPY . /$HOME/app

WORKDIR /$HOME/app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
