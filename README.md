# **Service**
## Environment
- docker
- docker-compose

### Notes
- Changes in docker-compose.yml: exposed port, image name, container name
- Changes in supervisord.conf: log files' location

### Use with docker, docker-compose
JUST RUN: `> docker-compose up -d --build`

### Run celery
```celery --app src.tasks worker -Q celery -l DEBUG -c 4```

## Health check
```curl -i http://localhost:5055/common/health_check```

## Container env config:
```/webapps/service/.env```

## Init table logs
```CREATE TABLE logs(id INT AUTO_INCREMENT PRIMARY KEY, info VARCHAR(500), created_time DATETIME)```