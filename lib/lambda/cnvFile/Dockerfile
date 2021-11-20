#FROM ubuntu:20.04
FROM amazon/aws-lambda-python:3.8.2021.11.08.18

COPY ./* /home/

RUN pip install poetry
RUN yum install -y zip


RUN cd /home; ls
RUN cd /home; ./build.sh
#RUN cd /home; touch AAA
RUN cd /home; ls


