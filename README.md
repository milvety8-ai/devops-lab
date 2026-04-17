# DevOps Lab: Docker Compose + Kubernetes

Учебный проект с Flask-приложением, обратным прокси на Nginx и Kubernetes-манифестами для запуска в локальном кластере.

## Состав проекта

- `app/` - Flask-приложение и Dockerfile для сборки контейнера
- `nginx/` - конфигурация Nginx для проксирования запросов в приложение
- `k8s/` - Kubernetes-манифесты Deployment и Service
- `docker-compose.yml` - локальный запуск приложения и Nginx через Docker Compose

## Структура

```text
devops-lab/
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── k8s/
│   ├── deployment.yaml
│   └── service.yaml
├── nginx/
│   └── nginx.conf
└── docker-compose.yml
```

## Что делает приложение

Flask-сервис предоставляет два HTTP-эндпоинта:

- `GET /` - возвращает JSON с именем сервиса, hostname контейнера и версией приложения
- `GET /health` - возвращает JSON со статусом `"ok"` для health-check'ов

Пример ответа `GET /`:

```json
{
  "service": "devops-lab",
  "hostname": "container-id",
  "version": "1.0.0"
}
```

## Требования

- Docker
- Docker Compose
- Kubernetes или Minikube
- `kubectl`


### Как это работает

- сервис `app` собирается из каталога `app/`
- порт Flask-приложения наружу не публикуется
- сервис `nginx` слушает `80` порт и проксирует запросы в `app`
- оба сервиса находятся в сети `backend`

## Запуск в Kubernetes

### 1. Соберите Docker-образ

Если используется Minikube, удобно собирать образ прямо в его Docker-окружении:

```bash
eval $(minikube docker-env)
docker build -t devops-lab:v1 ./app
```

### 2. Примените манифесты

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### 3. Проверьте ресурсы

```bash
kubectl get pods
kubectl get services
```

### 4. Откройте сервис

Для Minikube:

```bash
minikube service devops-lab-service --url
```

Либо используйте `NodePort` вручную:

- порт сервиса: `80`
- `targetPort`: `5000`
- `nodePort`: `30080`

## Kubernetes-конфигурация

### Deployment

- имя Deployment: `devops-lab`
- количество реплик: `2`
- образ: `devops-lab:v1`
- `imagePullPolicy: Never` для использования локально собранного образа
- настроены `readinessProbe` и `livenessProbe` на `GET /health`
- заданы `requests` и `limits` по CPU и памяти

### Service

- тип сервиса: `NodePort`
- имя сервиса: `devops-lab-service`
- внешний порт: `80`
- порт приложения в контейнере: `5000`
- `nodePort`: `30080`

## Проверка работы

### Docker Compose

```bash
docker compose ps
docker compose logs
curl http://localhost/
curl http://localhost/health
```

### Kubernetes

```bash
kubectl describe deployment devops-lab
kubectl get pods -o wide
kubectl describe service devops-lab-service
curl http://$(minikube ip):30080/
curl http://$(minikube ip):30080/health
```

## Особенности проекта

- Nginx работает как reverse proxy перед Flask-приложением
- health-check в приложении используется и в Dockerfile, и в Kubernetes probes
- в `docker-compose.yml` доступ к приложению организован только через Nginx


