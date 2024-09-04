from flask import Blueprint, jsonify, request
import subprocess
from app.services.system_service import shutdown_system, reboot_system, get_system_info
from app.services.docker_service import get_docker_ps

system_bp = Blueprint('system', __name__)

@system_bp.route('/shutdown', methods=['POST'])
def shutdown():
    return shutdown_system()

@system_bp.route('/reboot', methods=['POST'])
def reboot():
    return reboot_system()

@system_bp.route('/welcome', methods=['GET'])
def welcome():
    try:
        system_info = get_system_info()
        return jsonify({'status': 'success', **system_info}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@system_bp.route('/docker', methods=['GET'])  # Tambahkan endpoint baru
def docker_ps():
    return get_docker_ps()

@system_bp.route('/execute', methods=['POST'])
def execute_command():
    global current_directory

    try:
        data = request.get_json()
        command = data.get('command')

        if not command:
            return jsonify({'status': 'error', 'error': 'No command provided'}), 400

        # Check if the command is 'cd'
        if command.startswith('cd '):
            new_directory = command[3:].strip()
            current_directory = new_directory
            return jsonify({'status': 'success', 'output': f'Changed directory to {current_directory}'}), 200

        # Run the command in the current directory
        full_command = f"cd {current_directory} && {command}"
        result = subprocess.run(full_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'status': 'success', 'output': result.stdout.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'error': e.stderr.decode()}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500