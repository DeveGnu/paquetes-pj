# Download docker image
FROM debian

# Extra data
LABEL maintainer="| DGTIT - MOR - |"
LABEL version="0.1"
LABEL description="Docker image to work with flask"

# Install for image
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# Configuration of the app
COPY requirements.txt /rest-api/requirements.txt
WORKDIR /rest-api
RUN pip install -r requirements.txt
COPY . /rest-api

EXPOSE 3690

CMD [ "python3", "./app.py" ]