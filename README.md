# Image Captioning Server

This project provides a **containerized FastAPI server** for image captioning using the `Salesforce/blip-image-captioning-base` model from Hugging Face. It leverages **NGINX, Gunicorn, and Uvicorn** to handle multiple parallel requests efficiently. A **Jupyter notebook** demonstrates sending parallel POST requests to the server.

---

## 🗂️ Repository Structure

- **app/main.py**: FastAPI application for loading the model and serving the `/caption` endpoint.  
- **Dockerfile**: Multi-stage Dockerfile for building the container.  
- **nginx.conf**: NGINX configuration for reverse proxying to Gunicorn.  
- **requirements.txt**: Python dependencies.  
- **demo_notebook.ipynb**: Jupyter notebook for testing parallel requests.  
- **start.sh**: Entry script to start both NGINX and Gunicorn.

---

## ⚙️ Prerequisites

- Docker  
- Python 3.10+ (for running the notebook)  
- Jupyter (for running the notebook)  
- Sample images (JPEG/PNG format) for testing  

---

## 🚀 Setup

## ⚙️ Local Python Environment (Optional, for Notebook)
If you prefer to run the notebook in a local Python environment (rather than just Docker), you can create a virtual environment and install dependencies easily. 

### Option 1: Using uv (modern Python environment manager)

```bash
# Create a new virtual environment with uv
uv venv

# Activate it
source .venv/bin/activate

# Install dependencies from requirements.txt
uv pip install -r requirements.txt

# Install additional dependencies for the notebook
uv pip install aiohttp jupyter
```

### Option 2: Using python -m venv (standard)
```bash
# Create a virtual environment
python -m venv .venv

# Activate it
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Install additional dependencies for the notebook
pip install aiohttp jupyter
```

### Clone the Repository

```bash
git clone https://github.com/swaroski/image-captioning-server.git 
cd image-captioning-server
```

## Build the Docker Image
```bash
docker build -t image-captioning-server .
```

## Run the Container
```bash
docker run -p 80:80 image-captioning-server
```

The server will be available at http://localhost:80


## ⚙️ Local Python Environment (Optional, for Notebook)
### Using uv
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv pip install aiohttp jupyter ipykernel
```

### Or using venv
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install aiohttp jupyter
```

## 🧪 Testing with the Notebook
### Install Dependencies
```bash
pip install aiohttp jupyter 
Prepare Sample Images
Place JPEG/PNG images (e.g., dog.png, family.png, surf.jpg) in an images/ directory or alongside the notebook.
```

### Run the Notebook
```bash
jupyter notebook demo_notebook.ipynb
```

Execute the cell to send parallel POST requests to http://localhost:80/caption.
The notebook will print captions for each image, e.g.:

```bash
Image: images/elephant.jpg, Caption: the elephant is wet
Image: images/bananas.jpg, Caption: a bunch of bananas
Image: images/spoons.jpg, Caption: a wooden table with a bunch of wooden spoons
Image: images/cycling.jpg, Caption: a man riding a bike
Image: images/cherry_blossom.jpg, Caption: people are gathered around a blue table covered in pink flowers
Image: images/dog.png, Caption: a dog sitting in the grass with its tongue out
Image: images/surf.jpg, Caption: a man riding a wave on a surfboard
Image: images/bike.jpg, Caption: a motorcycle parked in the dirt
Image: images/family.png, Caption: a group of people are smiling and posing for a picture
Image: images/boy_eating_burger.jpg, Caption: a boy eating a piece of pizza
```


## 🖥️ API Endpoint

```bash
POST /caption
```
- Request: Form-data with key file and an image (JPEG/PNG).

- Response: JSON with a caption field, e.g.:

```bash
{"caption": "A dog sitting in the grass with its tongue out"}
```

## 📝 Notes
- The server uses 8 Gunicorn workers for concurrent request handling.

- The **Salesforce/blip-image-captioning-base** model runs on GPU if available, otherwise CPU.

- Logs are available in /var/log/nginx/ inside the container for debugging.

- NGINX config allows uploads up to 10 MB (client_max_body_size).

💡 Model Choice
I chose the **Salesforce/blip-image-captioning-base** model because:

✅ It’s lightweight (~350MB) — faster startup and efficient memory use.
✅ Provides accurate image captions for a wide range of images.
✅ Well-suited for a demonstration of containerized AI inference.


🔥 📝 Performance Notes
During testing, I observed that semaphore=2 in the notebook (max 2 concurrent client requests) consistently gave the best performance — even when the server had 6 Gunicorn workers.

This might seem surprising, but it reflects real-world performance factors:

Each image captioning request is CPU and memory intensive.

More than 2 simultaneous heavy requests cause CPU cache pressure and context-switching overhead, which slows down overall throughput.

This demonstrates that the fastest concurrency setting is often lower than the number of CPU cores for CPU-heavy workloads.

Takeaway:

More concurrency ≠ more speed.

The best concurrency is usually the sweet spot that matches your hardware and workload.