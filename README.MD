# Интеллектуальный ассистент методиста

## Необходимые зависимости:
``
python3
cuda118+
``

## Стек
```
DS: Pytorch, Transformers, Spacy, nltk, KeyBert, torchaudio, sklearn
Backend: Python3.10, FastAPI, Celery, PostgeSQL, SQLAlchemy, redis, docker
Frontend: Angular
```

## Использованные модели
```
whisper-large-v3
Mistral-7B-OpenOrca
```

## Установка
**ONLY *LINUX* SUPPORTED or *WSL* (not tested on Windows)**
```
python3 prepare_models_for_docker.py

cd ./backend

docker-compose up
```

## Использование
- Перейдите на http://127.0.0.1:4200
- Наслаждайтесь)))))


