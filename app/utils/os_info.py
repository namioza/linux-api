import subprocess

def parse_os_info():
    try:
        os_info = subprocess.check_output(['cat', '/etc/os-release']).decode().strip().split('\n')
        os_info_dict = {}
        for line in os_info:
            key, value = line.split('=', 1)
            os_info_dict[key] = value.strip('"')
        pretty_name = os_info_dict.get('PRETTY_NAME', 'Unknown')
        version = os_info_dict.get('VERSION', 'Unknown')
        return f"{pretty_name} with {version}"
    except Exception as e:
        return f"Error retrieving OS info: {str(e)}"
