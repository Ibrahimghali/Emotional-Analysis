FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install PyTorch with compatible version for Python 3.11
RUN pip install --upgrade pip && \
    pip install torch==2.1.0+cpu torchvision==0.16.0+cpu torchaudio==2.1.0 -f https://download.pytorch.org/whl/torch_stable.html

# Install other requirements
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change this line to use python -m to run uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
