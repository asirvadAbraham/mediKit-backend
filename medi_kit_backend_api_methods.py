import json
import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def is_doctor_name_present(request_doctor_name, doctor_name):
    request_doctor_name_trimmed=request_doctor_name.strip()
    if request_doctor_name_trimmed:
        request_name_split_array=request_doctor_name_trimmed.split()
        for element in request_name_split_array:
            if element.lower() in doctor_name.lower():
                return True
        return False
    else:
        return True

@app.route('/get_city_name', methods=['POST'])
def get_city_name():
    request_data = request.json
    postal_code = request_data['pin_code']

    if not postal_code:
        return jsonify({'error': 'Postal code parameter is required'}), 400
    url = f'https://api.postalpincode.in/pincode/{postal_code}'
    response = requests.get(url)
    response_data = response.json()

    if response_data and response_data[0]['Status'] == 'Success':
        city_name = response_data[0]['PostOffice'][0]['Name']
        return jsonify({'city_name': city_name}), 200
    else:
        return jsonify({'error': 'Postal code not found'}), 404
    
@app.route('/get_doctor_details', methods=['POST'])
def get_doctor_details():
    base_dir=os.path.abspath(os.path.dirname(__file__))
    json_data_file_path=os.path.join(base_dir,'data.json')
    with open(json_data_file_path) as dataFile:
        dataSet=json.load(dataFile)
    try:
        request_data = request.json
        print("Received data:", request_data)
        result =list(filter(lambda value: value['pin_code']==request_data['pin_code'] and is_doctor_name_present(request_data['doctor_name'],value['doctor_name']), dataSet['details']))
        print('Result:',(result))
      
        return {'data_set':result}, 200
    except Exception as error:
        return jsonify({'error': str(error)}), 500


if __name__ == '__main__':
    app.run()