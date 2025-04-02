FROM python:3.13-alpine
ARG PORT

WORKDIR /code

COPY ./requirements.txt ./
RUN python -m pip install -r requirements.txt --no-cache-dir --require-hashes

COPY ./scripts ./api ./

RUN apk update && apk upgrade

EXPOSE ${PORT}/tcp

ENTRYPOINT ["/code/scripts/entrypoint.sh"]
