from dotenv import load_dotenv
import os
from pathlib import Path
import logging
from datetime import datetime as dt

load_dotenv()

ROOT = Path(__file__).parent.parent
DATABASE_URL = os.getenv("DATABASE_URL")
RPA_CHALLENGE_API_KEY = os.getenv("RPA_CHALLENGE_API_KEY")
TEMP_DIR = os.path.join(ROOT, os.getenv("TEMP_DIR"))
OUTPUT_DIR = os.path.join(ROOT, os.getenv("OUTPUT_DIR"))
LOG_DIR = os.path.join(ROOT, os.getenv("LOG_DIR"))
directories = [TEMP_DIR, OUTPUT_DIR, LOG_DIR]

for dir in directories:
    os.makedirs(dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'{LOG_DIR}/rpa_{dt.now().strftime("%Y%m%d_%H%M%S")}.log')
    ]
)

logger = logging.getLogger(__name__)
