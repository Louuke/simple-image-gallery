# Build stage
FROM python:3.11-alpine AS builder
WORKDIR /app

# Install git to get version of the package
RUN apk update && \
    apk add --no-cache git

# Copy pyproject.toml and .git directory to be able to install dependencies
COPY .git .git
COPY pyproject.toml .

# Install dependencies
RUN pip install --user --no-cache-dir .

# Copy the source code
COPY ./src .
# Install the package
RUN pip install --user --no-cache-dir --no-deps .

# Runtime stage
FROM python:3.11-alpine
ENV PYTHONUNBUFFERED=1

# Copy .local directory from the builder stage
COPY --from=builder /root/.local /home/appuser/.local
# Set up non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup \
    && chown -R appuser:appgroup /home/appuser/.local
USER appuser

# Set PATH to include the local bin directory
ENV PATH="/home/appuser/.local/bin:$PATH"
ENV HOME="/home/appuser"

EXPOSE 8080

ENTRYPOINT ["simple-image-gallery", "--gallery_host", "0.0.0.0", "--gallery_port", "8080"]