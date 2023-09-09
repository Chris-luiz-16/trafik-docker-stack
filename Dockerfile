FROM alpine:latest
    
RUN mkdir /var/flaskapp/

RUN adduser  -h /var/flaskapp/ -s /bin/sh -D  flaskapp

WORKDIR /var/flaskapp/

COPY  .   .

RUN  apk update && apk add python3 py3-pip --no-cache


RUN pip3 install -r requirements.txt 


RUN chown -R flaskapp:flaskapp  /var/flaskapp/

    
USER flaskapp


EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["app.py"]
