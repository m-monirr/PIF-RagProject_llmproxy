"""
Quick launcher for Streamlit app
"""

import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "app.py",
        "--server.port=8080",
        "--server.address=localhost"
    ])
