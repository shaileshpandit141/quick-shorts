import subprocess
from pathlib import Path
from typing import Optional


def run_commands() -> None:
    backend_dir = Path("./backend").resolve()
    frontend_dir = Path("./frontend").resolve()

    print("\n🚀 Starting servers...")

    # Check if directories exist
    if not backend_dir.exists() or not frontend_dir.exists():
        print("❌ Backend or frontend directory not found!")
        return

    backend_process: Optional[subprocess.Popen[bytes]] = None
    frontend_process: Optional[subprocess.Popen[bytes]] = None

    try:
        # Run backend in new terminal tab
        backend_process = subprocess.Popen(
            [
                "gnome-terminal",
                "--tab",
                "--title=Backend Server",
                "--",
                "bash",
                "-c",
                f"source backend/.venv/bin/activate && cd {backend_dir} && python3 manage.py runserver; exec bash",
            ]
        )
        print("✅ Backend server started successfully")

        # Run frontend in new terminal tab
        frontend_process = subprocess.Popen(
            [
                "gnome-terminal",
                "--tab",
                "--title=Frontend Server",
                "--",
                "bash",
                "-c",
                f"cd {frontend_dir} && npm start; exec bash",
            ]
        )
        print("✅ Frontend server started successfully")
        print("💻 Development environment is ready!\n")

        # Wait for processes to complete
        backend_process.wait()
        frontend_process.wait()

    except KeyboardInterrupt:
        # Handle Ctrl+C
        print("\n⚠️  Shutting down servers...")
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()

        # Kill any remaining processes
        try:
            if backend_process:
                backend_process.kill()
            if frontend_process:
                frontend_process.kill()
        except:
            pass

        print("👋 Servers stopped successfully\n")

    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")


if __name__ == "__main__":
    run_commands()
