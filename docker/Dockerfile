# Dockerfile metadata for the first build
FROM registry.levelup.cce.af.mil/cdso/containers/base-registry/alpine:3.19 AS build

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python 3.11.9 and create a virtual environment
RUN apk upgrade --no-cache && \
    apk add --no-cache build-base cmake python3=3.11.9-r0 python3-dev=3.11.9-r0 py3-pip && \
    python3.11 -m venv venv && \
    . ./venv/bin/activate && \
    python3.11 -m pip install --no-cache-dir -r requirements.txt

# Dockerfile metadata for the second build
FROM registry.levelup.cce.af.mil/cdso/containers/base-registry/alpine:3.19

# Copy the virtual environment from the first build
COPY --from=build /app/venv /venv

# Install Python 3.11.9 and create a non-root user/group
RUN apk upgrade --no-cache --update && \
    apk add --no-cache python3=3.11.9-r0 && \
    adduser -D anchorman

# Set the working directory
WORKDIR /app

# Copy the rest of the application code into the container
# COPY app/ .

# Change to the non-root user
USER anchorman

# Set the execution path
ENV PATH="/venv/bin:$PATH"

# Expose the port that Streamlit will run on
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "main_upload_file.py"]