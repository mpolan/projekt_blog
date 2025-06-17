import os
from supabase import create_client, Client
from django.core.files.uploadedfile import InMemoryUploadedFile

# Konfiguracja ogólna
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Osobne bucket’y
BUCKET_POSTS = os.getenv("SUPABASE_BUCKET_POSTS", "post-images")
BUCKET_PROFILES = os.getenv("SUPABASE_BUCKET_PROFILES", "profile-pics")

# Inicjalizacja klienta
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# -------------------------
#  ZDJĘCIA POSTÓW
# -------------------------

def upload_image_to_supabase(file: InMemoryUploadedFile, path: str) -> bool:
    """Upload zdjęcia posta do bucketu post-images"""
    try:
        file.file.seek(0)
        content = file.read()
        print(f"➡️ Uploading post image: {path}")
        res = supabase.storage.from_(BUCKET_POSTS).upload(
            path,
            content,
            file_options={"content-type": file.content_type}
        )
        print("✅ Upload success:", res)
        return True
    except Exception as e:
        print("❌ Upload failed:", e)
        return False

def get_signed_image_url(path: str, expires_in: int = 60) -> str:
    """Generowanie podpisanego URL-a do zdjęcia posta"""
    try:
        res = supabase.storage.from_(BUCKET_POSTS).create_signed_url(path, expires_in)
        return res.get("signedURL", "")
    except Exception as e:
        print("Signed URL generation failed:", e)
        return ""

# -------------------------
#  ZDJĘCIA PROFILOWE
# -------------------------

def upload_profile_image(file: InMemoryUploadedFile, path: str) -> bool:
    """Upload zdjęcia profilowego do bucketu profile-pics"""
    try:
        file.file.seek(0)
        content = file.read()
        print(f"➡️ Uploading profile image: {path}")
        res = supabase.storage.from_(BUCKET_PROFILES).upload(
            path,
            content,
            file_options={"content-type": file.content_type}
        )
        print("✅ Profile image upload success:", res)
        return True
    except Exception as e:
        print("❌ Profile image upload failed:", e)
        return False

def get_profile_image_url(path: str, expires_in: int = 300) -> str:
    """Generowanie podpisanego URL-a do zdjęcia profilowego"""
    try:
        res = supabase.storage.from_(BUCKET_PROFILES).create_signed_url(path, expires_in)
        return res.get("signedURL", "")
    except Exception as e:
        print("Signed profile image URL generation failed:", e)
        return ""
