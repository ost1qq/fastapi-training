# Dockerfile

FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the required packages
RUN pip install -r requirements.txt

# Add the current directory to PYTHONPATH
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Copy the source code
COPY . .

EXPOSE 8003
# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]