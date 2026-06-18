FROM apache/airflow:2.5.1

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-dev \
        wget \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make sure 'python' points to 'python3'
RUN ln -sf /usr/bin/python3 /usr/bin/python

# Switch to airflow user before pip install
USER airflow

# Install Python packages as airflow user
RUN pip install --no-cache-dir \
    kafka-python \
    psycopg2-binary

# Switch back to root to copy scripts
USER root

# Copy your producer/consumer scripts
COPY ./scripts /opt/airflow/scripts
RUN chmod +x /opt/airflow/scripts/*.py

# Back to airflow user for safety
USER airflow
