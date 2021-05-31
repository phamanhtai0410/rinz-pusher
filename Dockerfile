FROM python:3.8-alpine

# Todo check local timezone or remove?
RUN apk add --no-cache tzdata git && cp /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime \
    && echo "Asia/Ho_Chi_Minh" > /etc/timezone

RUN apk upgrade -U \
    && apk add --no-cache -u ca-certificates libffi-dev libva-intel-driver supervisor python3-dev mariadb-connector-c-dev build-base linux-headers pcre-dev curl busybox-extras \
    && apk add mariadb-dev build-base \
    && pip3 install mysqlclient==1.4.6 \
    && apk del mariadb-dev \
    && rm -rf /tmp/* /var/cache/*

COPY requirements.txt /
RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install -r requirements.txt && mkdir -p /var/log/apps

COPY conf/uwsgi.ini /etc/uwsgi/
COPY conf/supervisor/ /etc/supervisor.d/
COPY . /webapps/the-cua-tui-service

WORKDIR /webapps/the-cua-tui-service
