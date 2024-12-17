FROM registry.levelup.cce.af.mil/cdso/containers/base-registry/ubuntu-cuda:22.04-12.1.0

# Set the working directory in the container
WORKDIR /app
COPY /app /app
COPY /helpers_af /app
COPY /services /app 
COPY /static /app
COPY /styles /app
COPY /main_file_upload.py /app
COPY /map.png /app


# Install necessary build tools and dependencies
# Update package index and install necessary packages without recommended ones
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends install -o Dpkg::Options::="--force-confnew" -y \
    build-essential cmake python3.10 python3.10-venv python3.10-dev python3-pip && \
    apt-get purge -y apt-transport-https cmake-data perl && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# Disable and stop nscd service
RUN systemctl disable nscd && systemctl stop nscd || true

# Copy requirements.txt to the container
COPY requirements.txt requirements.txt

# Create a virtual environment and install Python dependencies with --prefer-binary
RUN python3.10 -m venv venv && \
    . /app/venv/bin/activate && \
    pip install --no-cache-dir --prefer-binary setuptools==72.1.0 && \
    pip install --no-cache-dir --prefer-binary -r requirements.txt

# Set permissions for /usr/bin/wall
RUN chmod 750 /usr/bin/wall && chmod 750 /usr/share/bash-completion/completions/wall && \
    chmod o-x /usr/bin/wall && chmod o-x /usr/share/bash-completion/completions/wall

# Set the execution path
ENV PATH="/app/venv/bin:$PATH"

# Expose the port that Streamlit will run on
EXPOSE 8501


RUN apt-get purge -y \
    apt-transport-https \
    cuda-compat-12-1 \
    cuda-cudart-12-1 \
    cuda-keyring \
    cuda-toolkit-12-1-config-common \
    cuda-toolkit-12-config-common \
    cuda-toolkit-config-common \
    emacsen-common \
    gpg-agent \
    python3 \
    python3-pip \
    linux-libc-dev \
    libldap-2.5-0 \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*


# Uncomment and set up user permissions if needed
ARG APP_USER=burgundy
ARG APP_UID=1002
ARG APP_HOME=/home/${APP_USER}

RUN groupadd -g ${APP_UID} ${APP_USER} && \
    useradd -r -l -g ${APP_USER} -u ${APP_UID} ${APP_USER} && \
    mkdir -p /app/instance && \
    chown -R ${APP_USER}:${APP_USER} /app/instance

RUN chown -R ${APP_USER}:${APP_USER} /app && \
    chmod -R 755 /app

USER burgundy

# Run the Streamlit application
CMD ["streamlit", "run", "main_file_upload.py", "--server.port=8501"]

