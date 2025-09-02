FROM python:alpine3.22

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache bash && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "getVersOnOmnicomm.wsgi:application"]