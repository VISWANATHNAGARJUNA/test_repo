#!/usr/bin/env python
"""
build_requests.py

Demonstrates installing Requests at runtime in a PyInstaller-frozen app:
1. Bootstraps pip with ensurepip if missing.
2. Installs a local Requests wheel into a target directory.
3. Verifies the installation by importing requests.
"""

import os
import sys
import subprocess
import logging
import glob

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def ensure_pip():
    """
    Checks if pip is available. If not, uses ensurepip to bootstrap pip,
    then upgrades pip to a recent version.
    """
    logging.info("Checking if pip is available...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        logging.info("pip is already available.")
    except subprocess.CalledProcessError:
        logging.info("pip not found; bootstrapping with ensurepip...")
        import ensurepip
        ensurepip.bootstrap()

        logging.info("Upgrading pip to the latest version...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True
        )
        logging.info("pip has been successfully bootstrapped and upgraded.")

def install_requests_from_wheel(wheels_dir, target_install_dir):
    """
    Searches for a Requests wheel in wheels_dir and installs it into target_install_dir
    using the interpreter at sys.executable.
    """
    # Find any file that starts with 'requests' and ends with .whl
    whl_files = glob.glob(os.path.join(wheels_dir, "requests*.whl"))
    if not whl_files:
        logging.error("No Requests wheel file found in the wheels directory.")
        sys.exit(1)

    requests_whl = whl_files[0]
    logging.info(f"Found Requests wheel file: {requests_whl}")

    # Make sure the target directory exists
    if not os.path.exists(target_install_dir):
        os.makedirs(target_install_dir)
        logging.info(f"Created target install directory at: {target_install_dir}")
    else:
        logging.info(f"Target install directory already exists: {target_install_dir}")

    # Construct and run the pip install command
    cmd = [
        sys.executable, "-m", "pip", "install",
        requests_whl, "--target", target_install_dir
    ]
    logging.info("Running pip install to install Requests into the target directory...")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        logging.info("Requests installation succeeded.")
        logging.info("Installation output:\n" + result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error("Requests installation failed with error:")
        logging.error(e.stderr)
        sys.exit(1)

def test_requests_installation(target_install_dir):
    """
    Adds target_install_dir to sys.path and attempts to import Requests.
    Logs the installed version if successful; exits on failure.
    """
    logging.info("Adding the installation directory to sys.path and importing Requests...")
    sys.path.insert(0, target_install_dir)
    try:
        import requests
        logging.info(f"Successfully imported Requests version: {requests.__version__}")
    except Exception as e:
        logging.error("Failed to import Requests. Error: " + str(e))
        sys.exit(1)

def main():
    # 1. Ensure pip is available inside the frozen environment
    ensure_pip()

    # 2. Define where your .whl files are located (e.g. a "wheels" folder)
    wheels_dir = os.path.join(os.getcwd(), "wheels")
    if not os.path.isdir(wheels_dir):
        logging.error(f"Wheels directory not found: {wheels_dir}")
        sys.exit(1)

    # 3. Define the local installation directory
    target_install_dir = os.path.join(os.getcwd(), "local_requests_install")

    # 4. Install Requests from the local wheel
    install_requests_from_wheel(wheels_dir, target_install_dir)

    # 5. Test the installation
    test_requests_installation(target_install_dir)

    logging.info("Successfully installed and tested Requests at runtime.")

if __name__ == "__main__":
    main()
