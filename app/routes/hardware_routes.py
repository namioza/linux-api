from flask import Blueprint, jsonify
from app.services.hardware_service import get_cpu_temperature

hardware_bp = Blueprint('hardware', __name__)

@hardware_bp.route('/cpu-temp', methods=['GET'])
def cpu_temp():
    return get_cpu_temperature()
