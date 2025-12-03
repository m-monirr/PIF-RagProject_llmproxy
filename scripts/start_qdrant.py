"""
Start Qdrant vector database using Docker
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def check_docker_installed():
    """Check if Docker is installed"""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✅ Docker installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker not found")
            return False
    except:
        print("❌ Docker not installed or not in PATH")
        return False

def check_qdrant_running():
    """Check if Qdrant is already running"""
    try:
        response = requests.get("http://localhost:6333/collections", timeout=2)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def start_qdrant():
    """Start Qdrant Docker container"""
    project_root = Path(__file__).parent.parent
    storage_path = project_root / "data" / "qdrant_storage"
    storage_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n📂 Qdrant storage: {storage_path}")
    
    # Remove old container if exists (suppress errors)
    print("\n🧹 Cleaning up old containers...")
    try:
        subprocess.run(
            ["docker", "rm", "-f", "pif-qdrant"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10
        )
    except:
        pass
    
    # Build Docker command
    docker_cmd = [
        "docker", "run",
        "-d",
        "--name", "pif-qdrant",
        "-p", "6333:6333",
        "-p", "6334:6334",
        "-v", f"{storage_path.absolute()}:/qdrant/storage",
        "qdrant/qdrant"
    ]
    
    print(f"\n🚀 Starting Qdrant container...")
    
    try:
        result = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"❌ Failed to start Qdrant:")
            print(result.stderr)
            return False
        
        container_id = result.stdout.strip()
        print(f"✅ Container started: {container_id[:12]}")
        
        # Wait for Qdrant to be ready
        print("\n⏳ Waiting for Qdrant to be ready...")
        for i in range(30):
            time.sleep(1)
            if check_qdrant_running():
                print(f"✅ Qdrant is ready! (took {i+1}s)")
                return True
            if i % 5 == 0 and i > 0:
                print(f"   Still waiting... ({i}s)")
        
        print("❌ Timeout waiting for Qdrant to start")
        return False
        
    except Exception as e:
        print(f"❌ Error starting Qdrant: {e}")
        return False

def main():
    print("\n" + "="*70)
    print("🗄️  QDRANT VECTOR DATABASE - STARTUP SCRIPT")
    print("="*70)
    
    # Check Docker
    if not check_docker_installed():
        print("\n❌ Please install Docker first:")
        print("   Windows/Mac: https://www.docker.com/products/docker-desktop")
        print("   Linux: https://docs.docker.com/engine/install/")
        sys.exit(1)
    
    # Check if already running
    if check_qdrant_running():
        print("\n✅ Qdrant is already running on http://localhost:6333")
        print("\n💡 To restart:")
        print("   docker restart pif-qdrant")
        print("\n💡 To stop:")
        print("   docker stop pif-qdrant")
        return
    
    # Start Qdrant
    if start_qdrant():
        print("\n" + "="*70)
        print("✅ QDRANT STARTED SUCCESSFULLY")
        print("="*70)
        print(f"\n📍 REST API: http://localhost:6333")
        print(f"📍 gRPC: http://localhost:6334")
        print(f"📊 Dashboard: http://localhost:6333/dashboard")
        print(f"\n💡 To view logs:")
        print(f"   docker logs -f pif-qdrant")
        print(f"\n💡 To stop:")
        print(f"   docker stop pif-qdrant")
        print("="*70 + "\n")
    else:
        print("\n❌ Failed to start Qdrant")
        sys.exit(1)

if __name__ == "__main__":
    main()
