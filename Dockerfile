# Use an official Python runtime with CUDA 11.2 support as a parent image
FROM pytorch/pytorch:1.9.0-cuda11.2-cudnn8-runtime

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
# Note: we don't need to install torch separately as it's included in the base image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data
RUN python -c "import nltk; nltk.download('punkt')"

# Make port 8593 available to the world outside this container
EXPOSE 8593

# Run app.py when the container launches
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8593"]
