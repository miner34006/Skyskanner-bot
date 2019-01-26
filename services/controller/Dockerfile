FROM python:3.7.2-alpine

RUN mkdir -p /var/lib/skyscanner/logs/

COPY ./requirements.txt /home/skyenv/
RUN pip install --requirement /home/skyenv/requirements.txt

ENV SKYENV=/home/skyenv/

COPY ./services/controller /home/skyenv/controller
COPY ./services/modules /home/skyenv/modules
WORKDIR /home/skyenv/controller/

CMD ["python", "run.py"]