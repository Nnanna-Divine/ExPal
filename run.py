import subprocess
import time

def run_services():
    # 1. Start FastAPI Backend
    print("Starting FastAPI Backend...")
    fastapi_process = subprocess.Popen(["uvicorn", "server.main:app", "--reload", "--port", "8000"])

    # Give the backend a few seconds to initialize
    time.sleep(3)

    # 2. Start Streamlit Frontend
    print("Starting Streamlit Frontend...")
    streamlit_process = subprocess.Streamlit = subprocess.Popen(["Streamlit", "run", "client/app.py"])

    # Keep the runner script alive
    try:
        fastapi_process.wait()
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\nStopping services...")
        fastapi_process.terminate()
        streamlit_process.terminate()
        print("Services stopped.")

if __name__ == "__main__":
    run_services()