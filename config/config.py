import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    # Load environment variables from .env file
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    pass

BASE_DIR = Path(__file__).parent.parent
INPUT_DIR = BASE_DIR / "input_data"
OUTPUT_DIR = BASE_DIR / "output_demo"
LOGS_DIR = BASE_DIR / "logs"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "demo_mode")
