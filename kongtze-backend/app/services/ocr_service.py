"""OCR service for processing images using Google Gemini Vision"""

import os
from typing import Optional
import google.generativeai as genai
from PIL import Image
import io

from app.core.config import settings

# Configure Gemini API
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


class OCRService:
    """Service for optical character recognition using Google Gemini Vision"""

    def __init__(self):
        self.model = None
        if settings.GEMINI_API_KEY:
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def extract_text_from_image(self, image_path: str) -> Optional[str]:
        """
        Extract text from an image using Gemini Vision.

        Args:
            image_path: Path to the image file

        Returns:
            Extracted text or None if extraction fails
        """
        if not self.model:
            # Return placeholder text if Gemini is not configured
            return self._get_placeholder_text(image_path)

        try:
            # Open and prepare image
            image = Image.open(image_path)

            # Create prompt for OCR
            prompt = """Extract all text from this image.

Please transcribe exactly what you see, maintaining the structure and layout as much as possible.
If there are multiple sections, separate them clearly.
If the image contains handwriting, do your best to transcribe it accurately.

Return ONLY the extracted text, no additional commentary or formatting."""

            # Use Gemini vision to extract text
            response = self.model.generate_content([prompt, image])

            if response.text:
                return response.text.strip()

            return None

        except Exception as e:
            # Fallback to placeholder if OCR fails
            return self._get_placeholder_text(image_path)

    def _get_placeholder_text(self, image_path: str) -> str:
        """Generate placeholder text when OCR is not available"""
        filename = os.path.basename(image_path)
        return f"[OCR not configured - Image uploaded: {filename}]"

    async def validate_image(self, image_data: bytes) -> bool:
        """
        Validate that the uploaded file is a valid image.

        Args:
            image_data: Image file bytes

        Returns:
            True if valid image, False otherwise
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            # Check if it's a valid image format
            image.verify()
            return True
        except Exception:
            return False

    def get_supported_formats(self) -> list[str]:
        """Get list of supported image formats"""
        return [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]


# Singleton instance
ocr_service = OCRService()
