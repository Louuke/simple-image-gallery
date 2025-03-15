FROM python:3.11.11-alpine

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies
RUN pip install -e .

# Run app.py when the container launches
EXPOSE 5000
ENTRYPOINT ["flask", "--app", "image_gallery", "run"]