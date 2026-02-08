FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install nodejs for the frontend
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install frontend dependencies
COPY frontend/package*.json ./frontend/
RUN cd frontend && npm ci --only=production

# Copy the rest of the application
COPY . .

# Build the frontend
RUN cd frontend && npm run build

# Expose the port Hugging Face Spaces expects
EXPOSE 7860

# Set up environment for Hugging Face Spaces
ENV PYTHONUNBUFFERED=1
ENV NODE_ENV=production

# Start the application
# Install serve for frontend
RUN npm install -g serve

# Build frontend and copy to expected location
RUN cd frontend && npm install && npm run build
RUN mkdir -p /app && cp -r frontend/dist/* /app/ 2>/dev/null || echo "Copying frontend files"

# Start the application - serve both backend API and frontend
CMD ["sh", "-c", "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 7860"]