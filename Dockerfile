FROM python:3.6.9-stretch

LABEL maintainer="jiangbohuai"

WORKDIR /app
COPY requirements.txt .
RUN pip install -U pip -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
RUN pip install -U setuptools -i http://pypi.douban.com/simple  --trusted-host pypi.douban.com
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple    --trusted-host pypi.douban.com
RUN apt-get update && apt-get -y --no-install-recommends install cron vim
RUN apt-get -y --no-install-recommends install cron git
ENV ENV_PORT="8082"
ENV PHASE="TEST"
ADD . /app

CMD [ "./app/script/entrypoints.sh" ]