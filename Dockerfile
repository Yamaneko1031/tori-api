FROM python:3.8

RUN apt update && \
    apt install -y mecab libmecab-dev libmecab2 swig sudo mecab-ipadic-utf8
    
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
    cd mecab-ipadic-neologd/ && \
    ./bin/install-mecab-ipadic-neologd -n -y

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./app/pyproject.toml ./app/poetry.lock* /app/
WORKDIR /app/
RUN poetry install --no-root
RUN poetry update reqests google-cloud-firestore

EXPOSE 8080

COPY ./app /app
COPY startup.sh /bin/startup.sh

RUN chmod 744 /bin/startup.sh
ENTRYPOINT ["startup.sh"]