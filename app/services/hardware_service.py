import subprocess
from flask import jsonify

def get_cpu_temperature():
    try:
        result = subprocess.run(['bash', 'get_cpu_temp.sh'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode().strip()
        return jsonify({'status': 'success', 'temperature': output}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'error': e.stderr.decode()}), 500
