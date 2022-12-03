FROM miladaleali/dev_python:latest as base

WORKDIR /app/

ENV GIT_TOKEN_PEDESIS=${GIT_TOKEN_PEDESIS}

RUN pip install git+https://${GIT_TOKEN_PEDESIS}@github.com/miladaleali/pedesis.git

COPY ./app /app
# COPY ./pedesis/pedesis /app/pedesis/

ENV PYTHONPATH=/app

######################## START NEW IMAGE: DEBUGGER ############################
FROM base as debug
RUN pip install ptvsd

WORKDIR /app/

CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m manage run station
######################## START NEW IMAGE: PRODUCTION ##########################
FROM base as prod

COPY ./app/station-start.sh /station-start.sh

RUN chmod +x /station-start.sh

CMD bash /station-start.sh
