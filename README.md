# workers-fastAPI

## Instructions

For using the app:

Configure `.env.example` in the root folder as `.env`

```
docker-compose build
```

```
docker-compose up
```

o

```
docker compose up --build
```

## Celery 

Celery is a usefull tool in python for implementing cronjobs with workers. You can specify it's broker in requirements.txt. The usual flow is shown in the image:

![](docs/celery-flow.png)

You can check all the configurations in the folder `./app/celery-config`.


### Links of interest
  - [Simple Celery App](https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html)
  - [Celery brokers](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html)
  - [User Guide](https://docs.celeryq.dev/en/stable/userguide/index.html)
  