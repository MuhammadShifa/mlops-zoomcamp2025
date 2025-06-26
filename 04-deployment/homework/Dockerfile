# Q6: Use the base image with model + vectorizer already included
FROM agrigorev/zoomcamp-model:mlops-2024-3.10.13-slim

# Upgrade pip, install pipenv
RUN pip install -U pip && pip install pipenv

# Set working directory
WORKDIR /app

# Copy Pipenv environment files
COPY ["Pipfile", "Pipfile.lock", "./"]

# Install dependencies into system Python (no virtualenv inside container)
RUN pipenv install --system --deploy

# Copy your batch scoring script
COPY ["starter.py", "./"]

# Run for May 2023
CMD ["python", "starter.py", "2023", "5"]
