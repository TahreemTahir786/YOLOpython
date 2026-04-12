import os
import time
import requests
import numpy as np
from PIL import Image

def process_query(dir_path: str, item: str, save_path: str):
    img = os.path.join(dir_path, item)
    s_time = time.time()
    headers = {'clientside': str(s_time)}
    try:
        with open(img, 'rb') as f:
            files = {'img': f}
            response = requests.post(
                'http://localhost:5001/detect',
                files=files,
                headers=headers,
                timeout=(10, 30)
            )
        print("Status code:", response.status_code)
        if response.status_code != 200:
            print("Response text:", response.text)
            raise Exception(f"Server returned status {response.status_code}: {response.text}")
        json_response = response.json()
        if 'image' not in json_response:
            raise KeyError(f"'image' missing in response JSON: {json_response}")
        img_list = json_response['image']
        img_np = np.array(img_list, dtype=np.uint8)
        image = Image.fromarray(img_np)
        os.makedirs(save_path, exist_ok=True)
        image.save(os.path.join(save_path, f"{item}.jpeg"))
        current_time = time.time()
        e2e_delay = current_time - s_time
        process_time = json_response.get('proc_time', 0) * 1000
        client_side_prop = json_response.get('clientsideprop', 0)
        server_client = json_response.get('serverclientprop', current_time)
        server_side_prop = current_time - server_client
        prop_time = client_side_prop + server_side_prop
        return {
            "e2e_delay": e2e_delay,
            "process_time_ms": process_time,
            "prop_time": prop_time
        }
    except Exception as e:
        print(f"Error in process_query: {e}")
        return None