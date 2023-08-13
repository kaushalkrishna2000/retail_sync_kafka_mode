FROM python:latest

COPY requirements.txt /tmp/requirements.txt

RUN mkdir src

RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY src src

EXPOSE 8000

WORKDIR src

ENTRYPOINT ["sh", "entrypoint.sh"]