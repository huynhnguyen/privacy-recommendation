# Create common base stage
FROM python:3.6-slim as base
ENV VIRTUAL_ENV=/opt/venv
# Create virtualenv to isolate build
RUN python -m venv $VIRTUAL_ENV
COPY ./ /app/
WORKDIR /app
RUN pip install -U pip
# install git
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN pip install git+https://github.com/maciejkula/spotlight.git@master#egg=spotlight
RUN pip install -r requirements.txt
RUN echo "$(date)" > /tmp/buildtime.txt
CMD sh ./run_service.sh $PORT