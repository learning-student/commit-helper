FROM python:3.10.4-alpine3.15
COPY . /application
WORKDIR /application
RUN pip install -r requirements.txt
CMD python main.py --help
