FROM frolvlad/alpine-python3

WORKDIR /opt/workbench

COPY "./workbench" "./workbench"
COPY "./requirements.txt" "./"
COPY "./setup.py" "./"

RUN apk add --no-cache --virtual=build_dependencies musl-dev gcc python3-dev libffi-dev && \
    apk add --no-cache curl && \
    cd /opt/workbench && \
    touch README.md && \
    pip install -r requirements.txt && \
    pip install -e . && \
    rm -rf ~/.cache/pip && \
    apk del build_dependencies


WORKDIR /www

RUN chown -R nobody "."

USER nobody

VOLUME /www

EXPOSE 5000

ENTRYPOINT ["workbench"]
