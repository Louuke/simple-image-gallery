FROM python:3.11.11-alpine

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container at /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Run app.py when the container launches
EXPOSE 5000
ENTRYPOINT ["flask", "--app", "image_gallery/app.py", "run"]