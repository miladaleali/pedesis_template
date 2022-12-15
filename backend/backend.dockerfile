FROM miladaleali/dev_python:latest as base

WORKDIR /app/

COPY ./app /app

ENV PYTHONPATH=/app

ENV GIT_TOKEN_PEDESIS=

RUN pip install git+https://${GIT_TOKEN_PEDESIS}@github.com/miladaleali/pedesis.git
######################## START NEW BASE IMAGE: PRE PRODUCTION ############################
# FROM base as prod_base

# ENV GIT_TOKEN_PEDESIS=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

# RUN pip install git+https://${GIT_TOKEN_PEDESIS}@github.com/miladaleali/pedesis.git

######################## START NEW BASE IMAGE: PRE DEBUGGER ############################
# FROM base as debug_base

# COPY ./pedesis /usr/local/lib/python3.10/site-packages/pedesis

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
