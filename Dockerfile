FROM python:3.11-slim

# Install ffmpeg (buat yt-dlp)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file
COPY . .

# Expose port (Render butuh ini)
EXPOSE 10000

# Jalanin server FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "10000"]
