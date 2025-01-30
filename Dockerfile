FROM python:3.11-slim

RUN apt-get update && apt-get install -y sudo

RUN useradd -r flask-user

WORKDIR /home/flask-user/app
COPY . /home/flask-user/app

RUN mkdir /home/flask-user/app/instance && sudo chown -R flask-user:flask-user /home/flask-user/app/instance

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["sudo", "-u", "flask-user", "flask", "run", "--host=0.0.0.0", "--port=5000"]
