FROM python:3-alpine

RUN apk update
RUN apk add --no-cache gcc libc-dev libxslt-dev libxslt\
     musl-dev linux-headers libc-dev pcre-dev mailcap 

RUN mkdir /execute
WORKDIR /execute
RUN adduser --disabled-password -h /execute execute

RUN chown -R execute:execute /execute && \
  chmod -R 600 /execute

COPY ./requirements.txt /execute/

RUN pip install --no-cache-dir -r /execute/requirements.txt

COPY ./start.sh /start.sh

USER execute

ENTRYPOINT ["/bin/sh", "/start.sh"]

EXPOSE 9999