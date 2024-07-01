from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import base64
import numpy as np
from io import BytesIO
from werkzeug.utils import secure_filename
from src.model_processing import *
from src.azure_blob import *
import requests
import json
import base64


app = Flask(__name__)

# Set a max image size
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Set up Azure Blob Storage connection
connect_str = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = "butterfly-recognition"

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # get filename
        filename = secure_filename(file.filename)

        encoded_image = base64.b64encode(file.read()).decode('utf-8')

        # Scoring URI
        scoring_uri = 'http://d50304f6-e750-4e55-aa86-e0dee48773fe.australiaeast.azurecontainer.io/score'

        # Header
        headers = {
            'Content-Type': 'application/json'
        }

        # Payload
        payload = json.dumps({
            'image': encoded_image  
        })

        # Send the request
        response = requests.post(scoring_uri, headers=headers, data=payload)

        # Store the image in the 'images' folder in blob storage
        #img_url = upload_image_to_blob(file.read(), filename, connect_str, container_name)

        return response.json()

    else:
        return jsonify({'error': 'File type not allowed'}), 400



if __name__ == '__main__':
    app.run(debug=True)
