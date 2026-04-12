import requests
import pathlib
import os
import json
import numpy as np
from PIL import Image
import time
import csv
from tenacity import retry, wait_exponential, stop_after_attempt

fieldnames = ['Time', 'Model Name', 'File Name', 'Propagation Delay (s)', 'Processing Delay (ms)', 'E2E Delay (s)', 
              'location', 'core', 'model_acc', 'ram', 'cpu_request', 'cpu_usage', 'memory_request', 'memory_usage']
 
def generate_csv(path: str, fieldnames: list):
    """ 
    This function generates CSV file to log content if does not exist

    """
    base_name = 'dataset_yolo8m.csv'

    #timestamp = time.strftime("%Y%m%d_%H%M%S")
    csv_name = f"{base_name[:-4]}_b1.csv"
    csv_path = os.path.join(path, csv_name)

    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    print('CSV created...')
    return csv_path

@retry(wait=wait_exponential(multiplier=1, min=4, max=60), stop=stop_after_attempt(5))
def process_query(dir_path: str, item: str):
    img = os.path.join(dir_path, item)
    s_time = time.time()
    headers = {'clientside': str(s_time)}
    with open(img, 'rb') as f:
        files = {'img': f}
        response = requests.post('http://localhost:5001/detect', files=files, headers=headers, timeout=(10,30))
        
    if response.status_code == 200:
        current_time = time.time()
        json_response = json.loads(response.text)
        img_list = json_response['image']
        img_np = np.array(img_list, dtype=np.uint8)
        image = Image.fromarray(img_np)
  
        # Save the image
        image.save(os.path.join(save_path, f"{item}.jpeg"))
        e_time = time.time()
        e2e_delay = e_time - s_time
        process_time = json_response['proc_time'] * 1000
        #print(f'Processing Time: {process_time}')
        client_side_prop = json_response['clientsideprop']
        server_client = json_response['serverclientprop']
        server_side_prop = current_time - server_client
        prop_time = client_side_prop + server_side_prop
        
        return {
            'Time': time.time(),
            'Model Name': 'medium',
            'File Name': item,
            'Propagation Delay (s)': prop_time,
            'Processing Delay (ms)': process_time,
            'E2E Delay (s)': e2e_delay,
            'location': 'belgium',
            'core': 'two',
            'model_acc': 50.2,
            'ram': 1000,
            'cpu_request': json_response['cpu_request'],
            'cpu_usage': json_response['cpu_usage'],
            'memory_request': json_response['memory_request'], 
            'memory_usage': json_response['memory_usage']
        }
    else:
        print('Unsuccessful response!')
        return None 

def query(dir_path: str, save_path: str, csv_path: str):
    item = '6.jpg'
    for i in range(10):
        print(f'Iteration: {i}')
        result = process_query(dir_path, item)
        if result:
            with open(csv_path, 'a', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow(result)
    
    return None

if __name__ == '__main__':
    path = pathlib.Path(__file__).parent.resolve()
    dir_path = os.path.join(path, 'images')
    save_path = os.path.join(path, 'results/')
    logs_path = os.path.join(path, 'logs/')
    # generating CSV file
    csv_path = generate_csv(logs_path, fieldnames)
    query(dir_path, save_path, csv_path)
