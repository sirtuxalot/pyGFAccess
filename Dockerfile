### base image
FROM python:3.13.5-alpine3.22

### set work directory
WORKDIR /pyGFAccess

### copy pyGFAccess files
COPY ./keys /pyGameFlix/keys/
COPY .env access.py models.py uwsgi.ini requirements.txt entrypoint.sh /pyGFAccess/

### install required packages
RUN apk add --no-cache gcc libc-dev linux-headers

### install pyGFAccess dependencies
RUN pip install --no-cache-dir -r /pyGFAccess/requirements.txt

### Expose port(s)
EXPOSE 5001

### execute pyGFAccess
CMD [ "/bin/sh", "/pyGFAccess/entrypoint.sh" ]
