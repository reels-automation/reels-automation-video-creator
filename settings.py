import os
from dotenv import load_dotenv

ROOT_DIR = os.getcwd()

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL")
print("API_GATEWAY_URL", API_GATEWAY_URL)
MINIO_URL = os.getenv("MINIO_URL")
SECURE = os.getenv("SECURE")

if ENVIRONMENT == "DEVELOPMENT":
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
else:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER_DOCKER")
