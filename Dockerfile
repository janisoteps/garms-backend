FROM python:3.6-stretch
COPY server/ /server/
WORKDIR /server
RUN pwd && ls -la
RUN pip3 install -r requirements.txt
CMD [ "uwsgi", "--socket", "0.0.0.0:8000", \
               "--protocol", "http", \
               "-w", "wsgi", \
               "--master", \
               "--processes", "4", \
               "--threads", "2"]
