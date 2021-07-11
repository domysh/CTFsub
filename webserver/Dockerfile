FROM python:3-buster

RUN apt update && apt -y install cron supervisor

RUN mkdir /execute
WORKDIR /execute

#VOLUME /execute/data /execute/media
RUN echo "* * * * * root /usr/local/bin/python3 /execute/updater.py\n" > /etc/cron.d/task
RUN chmod 0644 /etc/cron.d/task
RUN crontab /etc/cron.d/task

ADD ./requirements.txt /execute/requirements.txt
RUN pip install --no-cache-dir -r /execute/requirements.txt

COPY . /execute/

RUN chmod -R 600 /execute && chmod -R u+X /execute

COPY ./supervisord.conf /etc/supervisor/supervisord.conf
ENTRYPOINT ["/usr/bin/supervisord"]

EXPOSE 9999
