FROM python:3.9

WORKDIR /ECE444-Flasky-lab

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=hello.py

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]