import os
import zipfile
from cryptography.fernet import Fernet

def encrypt_text(data: str, key: bytes) -> bytes:
    """
    Mã hóa 1 chuỗi text bằng Fernet.
    """
    fernet = Fernet(key)
    return fernet.encrypt(data.encode("utf-8"))

def generate_key_from_string(string_key: str) -> bytes:
    """
    Tạo khóa Fernet 32-byte từ chuỗi bất kỳ.
    """
    import base64
    from hashlib import sha256
    hashed = sha256(string_key.encode()).digest()
    return base64.urlsafe_b64encode(hashed)

def zip_folder_with_encryption(folderName: str, key_string: str):
    """
    Mã hóa file JSON và text rồi nén tất cả thành 1 file zip.
    """
    # Khóa mã hóa
    key = generate_key_from_string(key_string)
    fernet = Fernet(key)

    root = f"assets/{folderName}/"
    data_file = root + "data.json"
    image_folder = root + "datapacks/hint/images"
    text_folder = root + "datapacks/hint/text"
    output_zip = f"{folderName}.zip"

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 1️⃣ Mã hóa data.json (giữ nguyên tên file)
        with open(data_file, "r", encoding="utf-8") as f:
            plain = f.read()
            encrypted = fernet.encrypt(plain.encode("utf-8"))
            zipf.writestr("data.json", encrypted)

        # 2️⃣ Mã hóa tất cả file text (giữ nguyên tên file)
        for filename in os.listdir(text_folder):
            text_path = os.path.join(text_folder, filename)
            if os.path.isfile(text_path):
                with open(text_path, "r", encoding="utf-8") as f:
                    plain = f.read()
                    encrypted = fernet.encrypt(plain.encode("utf-8"))
                    zipf.writestr(f"hint/text/{filename}", encrypted)

        # 3️⃣ Thêm file ảnh (không mã hóa)
        for filename in os.listdir(image_folder):
            image_path = os.path.join(image_folder, filename)
            if os.path.isfile(image_path):
                zipf.write(image_path, arcname=f"hint/images/{filename}")

    print(f"✅ Đã tạo file {output_zip} với dữ liệu mã hóa.")

# 🧪 Example
zip_folder_with_encryption("surgeon", "duyanhle310")
