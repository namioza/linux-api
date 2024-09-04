import subprocess
import json
import re
import socket
from flask import jsonify

def get_device_ip():
    """
    Retrieve the IP address of the device.
    """
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.error:
        return 'Unknown'

def format_ports(ports, device_ip):
    """
    Replace 0.0.0.0 with the actual device IP and format ports correctly.
    """
    ports = ports.replace('\\u003e', '>')
    ports = ports.replace('0.0.0.0', device_ip)
    return ports

def format_output(output):
    """
    Format the raw docker ps output to make it more readable.
    """
    # Remove extra quotes around strings
    output = re.sub(r'^"|"$', '', output)
    return output

def get_docker_ps():
    try:
        # Run the docker ps command with the JSON format
        result = subprocess.run(['docker', 'ps', '-a', '--format', '{{json .}}'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        raw_output = result.stdout.decode().strip()
        
        # Split the output into individual lines
        lines = raw_output.splitlines()

        # Get device IP
        device_ip = get_device_ip()
        
        # Convert each line from JSON string to Python dict
        containers = [json.loads(line) for line in lines]
        
        # Format the output to make it more readable
        for container in containers:
            container['Command'] = format_output(container.get('Command', ''))
            container['Mounts'] = format_output(container.get('Mounts', ''))
            container['Ports'] = format_ports(container.get('Ports', ''), device_ip)
            # Add more fields if needed
        
        return jsonify({'status': 'success', 'containers': containers}), 200

    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'error': e.stderr.decode()}), 500
