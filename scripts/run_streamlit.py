"""
Quick launcher for Streamlit app
"""

import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    # Change to project root directory
    project_root = Path(__file__).parent.parent
    
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        str(project_root / "app.py"),
        "--server.port=8080",
        "--server.address=localhost"
    ], cwd=str(project_root))