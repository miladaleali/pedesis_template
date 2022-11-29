FROM python:3.10.8-slim-buster
# FROM python:3.10.8

WORKDIR /app/

COPY requirements.txt .

ENV GIT_TOKEN_PEDESIS=${GIT_TOKEN_PEDESIS}

# COPY ./resolv.conf /etc/resolv.conf

RUN apt-get update &&\
    apt-get install -y --no-install-recommends\
    gcc\
    build-essential\
    wget\
    git

COPY ./ta-lib-0.4.0-src.tar.gz /app

# RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
RUN tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

RUN pip install -r requirements.txt

COPY ./app /app
# COPY ./pedesis/pedesis /app/pedesis/

ENV PYTHONPATH=/app

COPY ./app/station-start.sh /station-start.sh

RUN chmod +x /station-start.sh

CMD bash /station-start.sh
