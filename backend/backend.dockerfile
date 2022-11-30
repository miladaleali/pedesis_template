FROM pedesis_python_env:latest

WORKDIR /app/

ENV GIT_TOKEN_PEDESIS=${GIT_TOKEN_PEDESIS}

RUN pip install git+https://${GIT_TOKEN_PEDESIS}@github.com/miladaleali/pedesis.git

COPY ./app /app
# COPY ./pedesis/pedesis /app/pedesis/

ENV PYTHONPATH=/app

COPY ./app/station-start.sh /station-start.sh

RUN chmod +x /station-start.sh

CMD bash /station-start.sh
