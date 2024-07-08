import subprocess
import sys
import os

def install_package(package):
    print(f"Attempting to install {package}...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")
        sys.exit(1)

# Define the path to the wheel file
wheel_file = './TA_Lib-0.4.29-cp311-cp311-win_amd64.whl'

# Check if the wheel file exists and install it
if os.path.isfile(wheel_file):
    install_package(wheel_file)
else:
    print(f"Wheel file not found: {wheel_file}")
    sys.exit(1)

# Install other dependencies from requirements.txt
install_package('-r requirements.txt')
