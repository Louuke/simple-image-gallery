# Build stage
FROM python:3.11-alpine AS builder

WORKDIR /app

# Copy pyproject.toml and .git directory to be able to install dependencies
COPY pyproject.toml .
COPY .git .git

# Install dependencies
RUN apk update && \
    apk add --no-cache git && \
    pip install --user --no-cache-dir .

# Copy the source code
COPY ./src .

# Install the package
RUN pip install --user --no-cache-dir .

# Runtime stage
FROM python:3.11-alpine
ENV PYTHONUNBUFFERED=1

# Copy .local directory from the builder stage
COPY --from=builder /root/.local /root/.local

# Set PATH to include the local bin directory
ENV PATH="/root/.local/bin:$PATH"

EXPOSE 80

ENTRYPOINT ["simple-image-gallery", "--gallery_host", "0.0.0.0", "--gallery_port", "80"]