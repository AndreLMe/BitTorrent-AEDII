FROM python

WORKDIR /usr/src/app

COPY ./src .

CMD python3 ./entryPoint.py "$PARAMS"