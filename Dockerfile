FROM ubuntu:latest
COPY . /xptre
WORKDIR /xptre
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "run.py"]
