FROM python:3.8

# Install Java and Spark
RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    wget -q https://downloads.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz && \
    tar xf spark-3.2.1-bin-hadoop3.2.tgz && \
    rm spark-3.2.1-bin-hadoop3.2.tgz && \
    mv spark-3.2.1-bin-hadoop3.2 /spark

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV SPARK_HOME=/spark
ENV PATH=$PATH:$SPARK_HOME/bin

# Copy PySpark code
COPY spark_code.py /app/spark_code.py

# Set the entry point
ENTRYPOINT ["spark-submit", "--master", "local[*]", "/app/spark_code.py"]
