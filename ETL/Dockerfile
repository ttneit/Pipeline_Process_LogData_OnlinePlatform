FROM apache/spark:3.4.2-scala2.12-java11-ubuntu
USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools --user

RUN rm -r /root/.cache && rm -rf /var/cache/apt/*

ENV PYSPARK_MAJOR_PYTHON_VERSION=3


WORKDIR /opt/application


COPY requirements.txt .
COPY ETL.py /opt/application/ETL.py
COPY MySQL_Connector/mysql-connector-java-8.0.30.jar /opt/spark/jars
COPY entrypoint.sh /entrypoint.sh

RUN pip3 install -r requirements.txt --user

ENTRYPOINT ["sh", "/entrypoint.sh"]
