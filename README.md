# YOLOv8 Flask API & Analysis Project

## Overview
This project provides a RESTful API for object detection using YOLOv8 (Ultralytics) models, with resource usage reporting, benchmarking scripts, and Jupyter notebooks for result analysis. It is containerized with Docker and supports local and Kubernetes deployment.

---

## Features
- **Flask API** for image detection using YOLOv8 models
- **Resource usage reporting** (CPU, memory) in API responses
- **Client scripts** for benchmarking and logging results
- **Jupyter notebooks** for data analysis and visualization
- **Docker** support for easy deployment
- **Kubernetes**-ready

---

## Project Structure
```
├── app.py                  # Main Flask API
├── propagation_HALF.py     # Client benchmarking script
├── app8.py, app8_kube_stats.py # Additional API scripts
├── Dockerfile              # Docker build file
├── logs/                   # Benchmarking results (CSV)
├── results/, runs/         # Output images and predictions
├── images/                 # Test images
├── yolo_env/               # Python virtual environment
├── yolo5_8_analysis.ipynb  # Jupyter notebook for analysis
├── yolov8*.pt              # YOLOv8 model weights
└── ...
```

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd yolov8
```

### 2. Create & Activate Virtual Environment
```bash
python3 -m venv yolo_env
source yolo_env/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# Or manually:
pip install flask ultralytics psutil pandas numpy matplotlib notebook
```

### 4. Download YOLOv8 Weights
Place your YOLOv8 model weights (e.g., `yolov8n.pt`, `yolov8s.pt`, `yolov8m.pt`) in the project root.

---

## Running the Flask API
```bash
python app.py
```
- The API will be available at `http://localhost:5000/detect`.

---

## Running the Client Script
```bash
python propagation_HALF.py
```
- This will send images to the API and log results in the `logs/` directory.

---

## Running Jupyter Notebooks
1. Activate your virtual environment.
2. Start Jupyter:
   ```bash
   jupyter notebook
   ```
3. Open `yolo5_8_analysis.ipynb` in VS Code or your browser for analysis and visualization.

---

## Docker Usage
### Build Docker Image
```bash
docker build -t yolov8-api .
```
### Run Docker Container
```bash
docker run -p 5000:5000 yolov8-api
```

---

## Kubernetes Deployment
- See `app8_kube_stats.py` and your Kubernetes YAML files for deployment instructions.

---

## Resource Usage Reporting
- The API returns CPU and memory usage in each response using `psutil`.

---

## Project Analysis
- Use the Jupyter notebook to compare YOLOv5 and YOLOv8 results, visualize processing delays, and analyze benchmarking data.

---

## Troubleshooting
- **Port conflicts:** Change the port in `app.py` or stop other services using the required port. 
- **Missing dependencies:** Ensure your virtual environment is activated and all packages are installed.
- **Jupyter issues in VS Code:** Install the "Jupyter" and "Python" extensions and open `.ipynb` files with the Notebook Editor.

---

Based on public sources, with modifications
