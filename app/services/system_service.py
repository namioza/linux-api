import subprocess
import psutil
import os
from flask import jsonify
from app.utils.os_info import parse_os_info
from app.services.hardware_service import get_cpu_temperature

def shutdown_system():
    try:
        result = subprocess.run(['shutdown', '-h', 'now'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'status': 'success', 'output': result.stdout.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'error': e.stderr.decode()}), 500

def reboot_system():
    try:
        result = subprocess.run(['reboot'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return jsonify({'status': 'success', 'output': result.stdout.decode()}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'error': e.stderr.decode()}), 500

def get_system_info():
    # OS Info
    os_info = parse_os_info()

    # System Load and Uptime
    try:
        uptime_info = subprocess.check_output(['uptime', '-p']).decode().strip()
        load_avg = os.getloadavg()
        load_info = f"{load_avg[0] * 100:.1f}%"
    except subprocess.CalledProcessError:
        uptime_info = 'Unknown'
        load_info = 'Unknown'

    # Memory Usage
    mem_info = psutil.virtual_memory()
    mem_usage = {
        'total': mem_info.total / (1024 ** 3),
        'available': mem_info.available / (1024 ** 3),
        'used': mem_info.used / (1024 ** 3),
        'percent': mem_info.percent
    }

    # Disk Usage
    disk_info = psutil.disk_usage('/')
    disk_usage = {
        'total': disk_info.total / (1024 ** 3),
        'used': disk_info.used / (1024 ** 3),
        'free': disk_info.free / (1024 ** 3),
        'percent': disk_info.percent
    }

    # USB Storage Info
    usb_info = []
    for disk in psutil.disk_partitions():
        if 'rm' in disk.opts:
            usage = psutil.disk_usage(disk.mountpoint)
            usb_info.append({
                'device': disk.device,
                'total': usage.total / (1024 ** 3),
                'used': usage.used / (1024 ** 3),
                'free': usage.free / (1024 ** 3),
                'percent': usage.percent
            })

    # IP Addresses
    try:
        ip_info = subprocess.check_output(['hostname', '-I']).decode().strip()
    except subprocess.CalledProcessError:
        ip_info = 'Unknown'

    # CPU Temperature
    temp_info = '0' #get_cpu_temperature()  # Mendapatkan data sebagai string, bukan response

    return {
        'Armbian OS': os_info,
        'CPU Load': load_info,
        'Uptime': uptime_info,
        'RAM': mem_usage,
        'eMMC': disk_usage,
        'usb_storage': usb_info,
        'ip_addresses': ip_info,
        'cpu_temp': temp_info
    }
