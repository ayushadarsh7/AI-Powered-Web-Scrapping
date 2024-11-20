# Use the official Python image from the Docker Hub
FROM python:3.10

# Install system dependencies required for Playwright
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file (assuming it is named requirements.txt)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its browsers
RUN pip install playwright && playwright install

# Copy the rest of your application code to the container
COPY . .

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
