# Gunicorn configuration file for Render deployment
import os

# Port to bind (Render automatically sets the PORT environment variable)
port = os.environ.get("PORT", "5000")
bind = f"0.0.0.0:{port}"

# Timeout for worker processes (in seconds). Default is 30.
# Model loading and parsing PDFs on a free tier can take longer, so we increase it to 120s.
timeout = 120

# We use lightweight threads rather than multiple heavy processes to save memory.
# Render free tier has a strict 512MB RAM limit.
workers = 1
threads = 4

# Worker class: we use threads
worker_class = "gthread"
