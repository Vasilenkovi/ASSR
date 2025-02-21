FROM python:3.12.3 AS builder
LABEL authors="Vizor"
COPY requirements.txt .

RUN pip install --upgrade pip
RUN mkdir /source
COPY /AssrWeb /AssrWeb
RUN pip install --target /source -r requirements.txt


FROM python:3.12.3-slim AS working
COPY --from=builder /source/ /source/
COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /AssrWeb /AssrWeb
# For postgres
RUN apt update && apt install libpq5 -y

WORKDIR /AssrWeb

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /source
