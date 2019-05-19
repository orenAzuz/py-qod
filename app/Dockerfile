FROM python

RUN pip install pymongo

RUN mkdir /app
COPY . /app

WORKDIR /app
RUN chmod +x /app/entry-point.sh

ENTRYPOINT ["/app/entry-point.sh"]