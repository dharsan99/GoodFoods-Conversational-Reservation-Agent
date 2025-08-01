FROM python:3.11-slim

WORKDIR /code

# Install system dependencies for Prisma and Google Cloud
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    wget -qO- https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    apt-get update && apt-get install -y google-cloud-cli

# Install Prisma CLI
RUN curl -fsSL https://get.prisma.io/install.sh | sh

# Copy requirements first for better caching
COPY requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy Prisma schema
COPY prisma /code/prisma

# Copy the application code
COPY app /code/app

# Copy initialization script
COPY init_prisma.py /code/init_prisma.py

# Copy seeding script
COPY seed_data.py /code/seed_data.py

# Copy test script
COPY test_prisma.py /code/test_prisma.py

# Expose the port
EXPOSE 8000

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🚀 Starting GoodFoods Backend..."\n\
\n\
# Authenticate with Google Cloud (if service account key is provided)\n\
if [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ]; then\n\
    echo "🔐 Authenticating with Google Cloud..."\n\
    gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS\n\
    gcloud config set project $GOOGLE_CLOUD_PROJECT_ID\n\
fi\n\
\n\
# Initialize Prisma\n\
echo "📦 Setting up Prisma..."\n\
python init_prisma.py\n\
\n\
# Generate Prisma client\n\
echo "🔧 Generating Prisma client..."\n\
prisma generate\n\
\n\
# Seed database with initial data (only if empty)\n\
echo "🌱 Checking if database needs seeding..."\n\
python seed_data.py\n\
\n\
# Start the FastAPI server\n\
echo "🌐 Starting FastAPI server..."\n\
uvicorn app.main:app --host 0.0.0.0 --port 8000\n\
' > /code/start.sh && chmod +x /code/start.sh

# The command to run the startup script
CMD ["/code/start.sh"] 