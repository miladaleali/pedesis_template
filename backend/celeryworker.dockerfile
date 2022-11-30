FROM pedesis_python_env:latest

WORKDIR /app/

ENV GIT_TOKEN_PEDESIS=${GIT_TOKEN_PEDESIS}

RUN pip install git+https://${GIT_TOKEN_PEDESIS}@github.com/miladaleali/pedesis.git

COPY ./app /app
# COPY ./pedesis/pedesis /app/pedesis/
WORKDIR /app

ENV PYTHONPATH=/app

COPY ./app/worker-start.sh /worker-start.sh

RUN chmod +x /worker-start.sh

CMD bash /worker-start.sh
