# 1. Base Image: Use Python 3.9 (matches your dev environment)
# "slim" version removes unnecessary tools to keep the file size down
FROM python:3.9-slim-bullseye

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Install System Dependencies
# OpenCV requires these Linux libraries to handle graphics, 
# even if we aren't displaying a window.
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    git \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy requirements first
# Docker caches layers. If you change your code but not your requirements,
# it won't have to re-install everything.
COPY requirements.txt .

# 5. Install PyTorch (CPU Version)
# We explicitly install the Linux CPU version of Torch. 
# This makes the image smaller (no massive CUDA drivers).
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 6. Install the rest of the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy your actual code
COPY . .

# 8. Expose the port Streamlit runs on
EXPOSE 8501

# 9. Healthcheck (Optional but "Pro" move)
# Tells Docker if the container is actually running properly
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 10. The Command to run your app
# "address=0.0.0.0" is CRITICAL. It lets the browser outside the container 
# talk to the app inside the container.
CMD ["streamlit", "run", "src/main.py", "--server.address=0.0.0.0"]