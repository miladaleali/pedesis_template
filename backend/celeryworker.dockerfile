FROM miladaleali/dev_python:latest as base

WORKDIR /app/

ENV GIT_TOKEN_PEDESIS=${GIT_TOKEN_PEDESIS}

RUN pip install git+https://${GIT_TOKEN_PEDESIS}@github.com/miladaleali/pedesis.git

COPY ./app /app
# COPY ./pedesis/pedesis /app/pedesis/
WORKDIR /app

ENV PYTHONPATH=/app

######################## START NEW IMAGE: DEBUGGER ############################‍
FROM base as debug
RUN pip install ptvsd

WORKDIR /app/

CMD python -m ptvsd --host 0.0.0.0 --port 5679 --wait --multiprocess -m manage run celery
######################## START NEW IMAGE: PRODUCTION ##########################
FROM base as prod

COPY ./app/worker-start.sh /worker-start.sh

RUN chmod +x /worker-start.sh

CMD bash /worker-start.sh
