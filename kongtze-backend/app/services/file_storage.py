"""File storage utilities for handling uploads"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile

from app.core.config import settings


class FileStorageService:
    """Service for handling file uploads and storage"""

    def __init__(self):
        self.storage_path = Path(settings.STORAGE_PATH)
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure storage directories exist"""
        (self.storage_path / "homework").mkdir(parents=True, exist_ok=True)
        (self.storage_path / "class_notes").mkdir(parents=True, exist_ok=True)
        (self.storage_path / "gifts").mkdir(parents=True, exist_ok=True)

    async def save_upload(
        self,
        file: UploadFile,
        category: str,
        user_id: int,
    ) -> Tuple[str, str]:
        """
        Save uploaded file to storage.

        Args:
            file: FastAPI UploadFile object
            category: Storage category (homework, class_notes, gifts)
            user_id: User ID for organizing files

        Returns:
            Tuple of (relative_path, absolute_path)
        """
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = Path(file.filename).suffix
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}{file_ext}"

        # Create user directory
        user_dir = self.storage_path / category / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)

        # Save file
        file_path = user_dir / filename
        content = await file.read()

        with open(file_path, "wb") as f:
            f.write(content)

        # Return relative path for database storage
        relative_path = f"{category}/{user_id}/{filename}"

        return relative_path, str(file_path)

    def get_absolute_path(self, relative_path: str) -> str:
        """Get absolute path from relative path"""
        return str(self.storage_path / relative_path)

    def delete_file(self, relative_path: str) -> bool:
        """
        Delete a file from storage.

        Args:
            relative_path: Relative path to the file

        Returns:
            True if deleted, False if file not found
        """
        try:
            file_path = self.storage_path / relative_path
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception:
            return False


# Singleton instance
file_storage = FileStorageService()
