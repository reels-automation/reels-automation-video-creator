import os
from dotenv import load_dotenv

ROOT_DIR = os.getcwd()
load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")

if ENVIRONMENT == "DEVELOPMENT":
    KAFKA_BROKER = os.getenv("KAFKA_BROKER")
else:
    KAFKA_BROKER = os.getenv("KAFKA_BROKER_DOCKER")
