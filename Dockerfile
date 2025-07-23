# Start with a slim Python image
FROM python:3.11-slim

# Set the home directory for our app
WORKDIR /app

# --- YEH HAI NAYA, SIMPLE TARIKA ---
# Copy all the files from our project folder into the container's /app directory
COPY . .
# ------------------------------------

# Install dependencies (CPU-only Torch first, then the rest)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Expose both ports that our services will use
EXPOSE 8000
EXPOSE 8501