"""Services for Kongtze backend"""

from app.services.ai_service import ai_service
from app.services.ocr_service import ocr_service
from app.services.file_storage import file_storage

__all__ = ["ai_service", "ocr_service", "file_storage"]
