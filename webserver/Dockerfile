FROM python:3-buster

RUN apt-get update && apt-get -y install supervisor

RUN mkdir /execute
WORKDIR /execute

ADD ./requirements.txt /execute/requirements.txt
RUN pip install --no-cache-dir -r /execute/requirements.txt

COPY . /execute/
COPY ./supervisord.conf /etc/supervisor/supervisord.conf

RUN usermod -a -G root nobody
RUN chown -R nobody:root /execute && \
  chmod -R 660 /execute && chmod -R u+X /execute

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]
