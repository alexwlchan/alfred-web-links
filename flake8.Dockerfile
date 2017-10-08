FROM alpine

RUN apk update && apk add python3

RUN pip3 install flake8

VOLUME ["/src"]
WORKDIR /src

ENTRYPOINT ["flake8"]
