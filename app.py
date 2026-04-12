from flask import Flask, request, jsonify
import time
import torch
from ultralytics import YOLO
import os
from PIL import Image
import io
import json
import psutil
import os

app = Flask(__name__)

model = YOLO("yolov8n.pt")

@app.route('/detect', methods=['POST'])
def detect():
    client_server = float(request.headers.get('clientside')) if 'clientside' in request.headers else 'Sender time not found'
    start_time = time.time()
    # calculating client to server propagation time
    client_side_prop = start_time - client_server 
    print(f'Client prop: {client_side_prop}')
    
    if 'img' not in request.files or request.files['img'].filename == '':
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['img']
    try:
        # start_time = time.time()
        # im_pil = Image.open(image)
        # print("Opened the image")
        # results = model(im_pil)
        # print(f"printing results: {results}")
        # nparr = results.render()[0]
        # nplist = nparr.tolist()
        # end_time = time.time()

        start_time = time.time()

        im_pil = Image.open(image)
        print("Opened the image")

        results = model(im_pil)
        print(f"printing results: {results}")

        annotated = results[0].plot()
        nplist = annotated.tolist()

        end_time = time.time()
        
        processing_time = end_time - start_time
        print(f"inference time: {processing_time}")

        process = psutil.Process(os.getpid())
        cpu_usage = process.cpu_percent(interval=0.1)
        memory_info = process.memory_info()
        memory_usage = memory_info.rss / (1024 * 1024)  # in MB
        cpu_count = os.cpu_count()
        memory_total = psutil.virtual_memory().total / (1024 * 1024)  # in MB
        # embedding current time for client to extract
        response = {
            'image': nplist,
            'proc_time': processing_time,
            'clientsideprop': client_side_prop,
            'serverclientprop': end_time,
            'cpu_request': cpu_count,
            'cpu_usage': cpu_usage,
            'memory_request': memory_total,
            'memory_usage': memory_usage
        }
        print(response)

        #response_json = json.dumps(response)

        return jsonify(response), 200
    
    except Exception as e:
        print(f"Error during detection: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)