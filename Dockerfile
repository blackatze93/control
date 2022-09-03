FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN apt update && apt install -y gdal-bin
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /app