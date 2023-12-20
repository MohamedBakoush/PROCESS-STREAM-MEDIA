#
FROM python:3.10

WORKDIR /stream/proxy

RUN apt install git
RUN apt-get -y update
RUN apt-get -y upgrade

COPY . . 

RUN pip install --upgrade pip  
RUN pip install -r requirements.txt 

ENTRYPOINT ["python"]

CMD ["__init__.py"]
