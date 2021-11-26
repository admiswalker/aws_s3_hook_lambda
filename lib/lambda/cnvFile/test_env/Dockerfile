FROM amazon/aws-lambda-python:3.8.2021.11.08.18

COPY ./* /home/

RUN pip install poetry
RUN cd /home; poetry install
RUN cd /home; poetry run python test.py

