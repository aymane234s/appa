import os
import subprocess
import sys

def run_ai_agent():
    print("🤖 [AI Agent]: Starting Project Lambda System Diagnosis...")
    
    # 1. Check current directory
    current_dir = os.getcwd()
    print(f"📂 [AI Agent]: Target directory identified: {current_dir}")
    
    # 2. Find the correct Python executable (Prefer 64-bit and stable versions)
    # Checking if a virtual environment exists (.venv or venv)
    venv_paths = ['.venv', 'venv']
    python_exe = sys.executable # default fallback
    
    for venv in venv_paths:
        possible_py = os.path.join(current_dir, venv, 'Scripts', 'python.exe')
        if os.path.exists(possible_py):
            python_exe = possible_py
            print(f"🎯 [AI Agent]: Found dedicated Virtual Environment at: {venv}")
            break
            
    print(f"⚙️ [AI Agent]: Utilizing Python interpreter: {python_exe}")
    
    # 3. Auto-install core dependencies to ensure no "ModuleNotFound" errors
    print("📦 [AI Agent]: Verifying and installing system dependencies (Streamlit, Plotly, AeroSandbox)...")
    try:
        subprocess.run([python_exe, "-m", "pip", "install", "streamlit", "numpy", "pandas", "plotly", "aerosandbox"], check=True)
        print("✅ [AI Agent]: Dependencies successfully synchronized.")
    except subprocess.CalledProcessError:
        print("⚠️ [AI Agent]: Standard pip failed, attempting alternative installation wheel architecture...")
        # Fallback to prevent compilation errors on experimental Python versions
        subprocess.run([python_exe, "-m", "pip", "install", "streamlit", "plotly", "aerosandbox", "--only-binary=:all:"], check=True)

    # 4. Launch the Streamlit Server natively
    print("🚀 [AI Agent]: Booting EcoAero Designer Pro Framework...")
    try:
        subprocess.run([python_exe, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 [AI Agent]: Server stopped by user.")

if __name__ == "__main__":
    run_ai_agent()
