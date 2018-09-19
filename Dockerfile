FROM python:3.6

ENV TZ 'Asia/Shanghai'
ENV PYTHONUNBUFFERED '0'

WORKDIR /app

RUN set -ex && pip install pipenv --upgrade -i https://mirrors.ustc.edu.cn/pypi/web/simple

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN set -ex && pipenv install --deploy --system

COPY . /app

CMD ["python", "main.py"]
