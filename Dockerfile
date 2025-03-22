FROM python:3.11.11-alpine

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies and web server
RUN pip install --no-cache-dir -e . && \
    pip install --no-cache-dir gunicorn

# Run app.py when the container launches
EXPOSE 5000
ENTRYPOINT ["gunicorn", "-b", "127.0.0.1:5000", "image_gallery:app"]