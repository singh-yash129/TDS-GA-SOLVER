
import PIL.Image as Image
import io
import docker
import requests
import fastapi
from fastapi import FastAPI
import uvicorn
import os
import subprocess
from Prebuilt import gunc
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from starlette.responses import Response
import pandas as pd
def generate_markdown():
    md_content = gunc('q-markdown')
    return md_content
from fastapi.responses import StreamingResponse
import base64
def compress_image(file_name):
    file = os.path.join(os.getcwd(), 'tmp', file_name)

    with Image.open(file) as img:
        if img.mode == "RGBA":
            img = img.convert("RGB")

        img_buffer = io.BytesIO()
        img.save(img_buffer, format="WEBP", quality=85, optimize=True)
        img_buffer.seek(0)

        # Convert to Base64
        image_base64 = base64.b64encode(img_buffer.getvalue()).decode("utf-8")

    return image_base64 

def deploy_github_pages(repo_name, github_username,email):
    os.system(f"git clone https://github.com/{github_username}/{repo_name}.git")
    os.chdir(repo_name)
    
    index_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>My Work</title>
</head>
<body>
    <h1>Welcome to My Work Showcase</h1>
    <p>Contact me at: <!--email_off-->{email}<!--/email_off--></p>
</body>
</html>"""
    
    with open("index.html", "w") as file:
        file.write(index_content)
    
    os.system("git add index.html")
    os.system("git commit -m 'Add GitHub Pages index.html'")
    os.system("git push origin main")
    os.system("git branch -M main")
    os.system("git checkout -b gh-pages")
    os.system("git push origin gh-pages")
    
    return(f"GitHub Pages deployed at: https://{github_username}.github.io/{repo_name}/")

def google_colab_test():
    return gunc('q-use-colab')
from PIL import Image
import numpy as np
import colorsys
def image_library_colab(file_name):
    file_path=os.path.join(os.getcwd(),'tmp',file_name)
    image = Image.open(file_path)

    # Normalize RGB values
    rgb = np.array(image) / 255.0
    
    # Convert to lightness channel
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x[:3])[1], 2, rgb)

    
    # Count pixels with lightness > 0.849
    light_pixels = np.sum(lightness > 0.849)
    return int(light_pixels)


def deploy_vercel(repo_name, github_username, file_name):
    port=5050
    os.system(f"git clone https://github.com/{github_username}/{repo_name}.git")
    os.chdir(repo_name)
    
    # Create Flask app
    app_content = f"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

with open('marks.json', 'r') as f:
    marks_data = json.load(f)

@app.route('/api', methods=['GET'])
def get_marks():
    names = request.args.getlist('name')
    result = {"marks": [marks_data.get(name, None) for name in names]}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port={port})
    """
    
    with open("api.py", "w") as file:
        file.write(app_content)
    marks_file=os.path.join(os.getcwd(),'tmp',file_name)
    # Copy marks file
    os.system(f"cp {marks_file} marks.json")
    
    # Setup Vercel deployment
    vercel_config = """
{
  "version": 2,
  "builds": [{ "src": "api.py", "use": "@vercel/python" }],
  "routes": [{ "src": "/api", "dest": "api.py" }]
}
    """
    
    with open("vercel.json", "w") as file:
        file.write(vercel_config)
    
    os.system("git add .")
    os.system("git commit -m 'Deploy Flask API to Vercel'")
    os.system("git push origin main")
    os.system("vercel deploy --prod")
    
    return (f"Vercel API deployed at: https://{github_username}.vercel.app/api")

def create_github_action(repo_name, github_username,email):
    os.system(f"git clone https://github.com/{github_username}/{repo_name}.git")
    os.chdir(repo_name)
    
    os.makedirs(".github/workflows", exist_ok=True)
    action_content = f"""
name: CI Pipeline

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2
      - name: {email}
        run: echo "Hello, world!"
    """
    
    with open(".github/workflows/main.yml", "w") as file:
        file.write(action_content)
    
    os.system("git add .github/workflows/main.yml")
    os.system("git commit -m 'Add GitHub Action' ")
    os.system("git push origin main")
    
    return (f"GitHub Action added at: https://github.com/{github_username}/{repo_name}/actions")

def push_docker_image(docker_username, repo_name):
    os.system("docker build -t {docker_username}/{repo_name}:23f2004644 .")
    os.system("docker login")
    os.system("docker push {docker_username}/{repo_name}:23f2004644")
    return(f"Docker image pushed to: https://hub.docker.com/repository/docker/{docker_username}/{repo_name}/general")


def serve_students_data(file_name):
    csv_file=os.path.join(os.getcwd(),'tmp',file_name)
    app = FastAPI()
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    df = pd.read_csv(csv_file)
    
    @app.get("/api")
    def get_students(class_param: list[str] = None):
        if class_param:
            filtered_df = df[df['class'].isin(class_param)]
        else:
            filtered_df = df
        
        return {"students": filtered_df.to_dict(orient="records")}
    
    return app

def run_fastapi_server(file_name):
    csv_file=os.path.join(os.getcwd(),'tmp',file_name)

    app = serve_students_data(csv_file)

    uvicorn.run(app, host="0.0.0.0", port=4000)



import os
import subprocess
import time
import requests

def run_llamafile(file_name):
    llamafile_path = os.path.join(os.getcwd(), 'tmp', file_name)

    # Run llamafile (assuming it's an executable; remove `shell=True` if not needed)
    llamafile_process = subprocess.Popen([llamafile_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Start ngrok
    ngrok_process = subprocess.Popen(["ngrok", "http", "8081"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Wait for ngrok to start
    time.sleep(3)  # Small delay to ensure ngrok is up

    # Get ngrok URL
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        response.raise_for_status()
        public_url = response.json()['tunnels'][0]['public_url']
        return f"Llamafile server started and exposed via ngrok: {public_url}"
    except requests.RequestException as e:
        return f"Error retrieving ngrok URL: {str(e)}"


