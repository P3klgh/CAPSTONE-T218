FROM python:3.11-slim

# Install dependencies for PyQt GUI support and X11 forwarding
RUN apt-get update && apt-get install -y \
    python3-pyqt5 \
    qtbase5-dev \
    qtchooser \
    qt5-qmake \
    qtbase5-dev-tools \
    xvfb \
    x11-utils \
    build-essential \
    libgeos-dev \
    libproj-dev \
    libnss3 \
    libasound2 \
    git \
    libx11-xcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements-dev.txt into the container and install Python dependencies
COPY requirements-dev.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install qtawesome if used separately
RUN pip install --no-cache-dir qtawesome

# Copy the whole project into the container
COPY . .

# Set environment variables for display and Python path
ENV DISPLAY=:99
ENV PYTHONPATH=/app

# Set the default command to run the main application with virtual framebuffer (Xvfb)
CMD ["xvfb-run", "-a", "--server-args='-screen 0 1024x768x24'", "python", "mainwindow.py"]
