#
FROM python:3.10

WORKDIR /stream/proxy

# Install dependencies
RUN apt-get update && \
    apt-get install -y git ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container
COPY . .

# Upgrade pip and install Python dependencies from requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 1945

# Set the default command to run the app
ENTRYPOINT ["python"]
CMD ["__init__.py"]