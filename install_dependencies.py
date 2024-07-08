import subprocess
import sys
import os

# Define the path to the wheel file
wheel_file = './TA_Lib-0.4.29-cp311-cp311-win_amd64.whl'

# Check if the wheel file exists
if os.path.isfile(wheel_file):
    # Install the wheel file
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', wheel_file])
else:
    raise FileNotFoundError(f"Wheel file not found: {wheel_file}")

# Install other dependencies from requirements.txt
subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
