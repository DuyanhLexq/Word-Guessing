import zipfile
import json
from cryptography.fernet import Fernet
import pygame
import io
import consts
from core.logger import log
from typing import List
# Create logger for this module
logger = log(consts.LOAD_DATA_LOG_NAME)

def generate_key_from_string(string_key: str) -> bytes:
    """
    Generate a Fernet 32-byte key from any string.
    """
    import base64
    from hashlib import sha256
    hashed = sha256(string_key.encode()).digest()
    return base64.urlsafe_b64encode(hashed)


def load_zip_data(zip_path: str, key_string: str) -> List[dict]:
    """
    Read and decrypt data from a zip file.

    Returns:
      - data_json: dict (from data.json file)
      - images: dict {filename: pygame.Surface}
      - text_files: dict {filename: text content}
    """
    # Generate Fernet key from the string key
    key = generate_key_from_string(key_string)
    fernet = Fernet(key)

    data_json = {}
    images = {}
    text_files = {}

    # Initialize pygame (to load images)
    pygame.init()

    logger.info(f"Opening zip file: {zip_path}")
    with zipfile.ZipFile(zip_path, "r") as zip_file:
        for file_name in zip_file.namelist():
            logger.debug(f"Processing: {file_name}")

            # Decrypt the JSON data file
            if file_name == consts.DATA_FILE_NAME:
                with zip_file.open(file_name) as f:
                    encrypted_data = f.read()
                    decrypted_data = fernet.decrypt(encrypted_data).decode("utf-8")
                    data_json = json.loads(decrypted_data)
                    logger.info(f"Loaded {consts.DATA_FILE_NAME}")

            # Load images (not encrypted)
            elif file_name.startswith(consts.IMAGES_HINT_PATH) and not file_name.endswith("/"):
                with zip_file.open(file_name) as f:
                    image_data = f.read()
                    image_surface = pygame.image.load(io.BytesIO(image_data))
                    image_name = file_name.split("/")[-1]
                    images[image_name] = image_surface
                    logger.info(f"Loaded image: {image_name}")

            # Decrypt text files
            elif file_name.startswith(consts.TEXT_HINT_PATH) and not file_name.endswith("/"):
                with zip_file.open(file_name) as f:
                    encrypted_text = f.read()
                    decrypted_text = fernet.decrypt(encrypted_text).decode("utf-8")
                    text_name = file_name.split("/")[-1]
                    text_files[text_name] = decrypted_text
                    logger.info(f"Loaded text: {text_name}")

    logger.info("Finished loading all data from zip.")
    return data_json, images, text_files