FROM python:3.7.2-alpine

RUN mkdir -p /var/lib/skyscanner/logs/

COPY ./requirements.txt /home/skyenv/
RUN pip install --requirement /home/skyenv/requirements.txt

ENV SKYENV=/home/skyenv/

COPY ./services/vkBot /home/skyenv/vkBot
COPY ./services/modules /home/skyenv/modules
WORKDIR /home/skyenv/vkBot/

EXPOSE 5000

CMD ["python", "run.py"]