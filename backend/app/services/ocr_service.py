from __future__ import annotations

import io
import re
from typing import List

from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
from pytesseract import TesseractNotFoundError


# Matches normal HTTP/HTTPS URLs.
URL_PATTERN = re.compile(
    r"https?://[^\s<>\"]+",
    re.IGNORECASE,
)

# Also catches common www.example.com-style URLs when OCR
# does not preserve the https:// prefix.
WWW_URL_PATTERN = re.compile(
    r"\bwww\.[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}"
    r"(?:/[^\s<>\"]*)?",
    re.IGNORECASE,
)


class OCRService:
    """
    OCR pipeline for ScamShield screenshot analysis.

    Pipeline:

        Image
          ↓
        Pre-processing
          ↓
        Tesseract OCR
          ↓
        Cleaned text
          ↓
        URL extraction
    """

    MAX_IMAGE_BYTES = 10 * 1024 * 1024
    MAX_IMAGE_SIZE = 12_000_000

    @classmethod
    def extract_text_from_bytes(
        cls,
        image_bytes: bytes,
    ) -> str:
        """
        Convert image bytes into OCR text.

        The image is:
        1. opened safely,
        2. converted to RGB,
        3. enlarged,
        4. converted to grayscale,
        5. contrast-enhanced,
        6. lightly sharpened,
        7. passed to Tesseract.

        A thresholded version is used as a fallback when
        the first OCR pass produces little or no text.
        """

        if not image_bytes:
            raise ValueError(
                "The uploaded screenshot is empty."
            )

        if len(image_bytes) > cls.MAX_IMAGE_BYTES:
            raise ValueError(
                "Screenshot is too large. Maximum size is 10 MB."
            )

        try:
            image = Image.open(
                io.BytesIO(image_bytes)
            )

            image.load()

        except Exception as exc:
            raise ValueError(
                "The uploaded file is not a valid image."
            ) from exc

        width, height = image.size

        if width <= 0 or height <= 0:
            raise ValueError(
                "The screenshot has invalid dimensions."
            )

        if width * height > cls.MAX_IMAGE_SIZE:
            # Resize very large screenshots before OCR so that the
            # low-memory Intel Mac demo environment remains stable.
            scale = (
                cls.MAX_IMAGE_SIZE
                / float(width * height)
            ) ** 0.5

            new_width = max(
                1,
                int(width * scale),
            )

            new_height = max(
                1,
                int(height * scale),
            )

            image = image.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS,
            )

        try:
            enhanced = cls._preprocess(image)

            text = cls._run_ocr(
                enhanced
            )

            cleaned = cls._clean_text(
                text
            )

            # OCR can struggle with screenshots containing
            # small dark text on bright backgrounds. In that
            # case, run a second OCR pass on a thresholded image.
            if len(cleaned) < 12:
                thresholded = cls._threshold(
                    enhanced
                )

                fallback_text = cls._run_ocr(
                    thresholded
                )

                fallback_cleaned = cls._clean_text(
                    fallback_text
                )

                if len(fallback_cleaned) > len(cleaned):
                    cleaned = fallback_cleaned

            if not cleaned:
                raise ValueError(
                    "No readable text was detected in the screenshot."
                )

            return cleaned

        except TesseractNotFoundError as exc:
            raise RuntimeError(
                "Tesseract OCR is not installed or is not available "
                "on the system PATH. Install it with "
                "'brew install tesseract' and try again."
            ) from exc

    @staticmethod
    def _preprocess(
        image: Image.Image,
    ) -> Image.Image:
        """
        Prepare a screenshot for OCR.
        """

        image = image.convert(
            "RGB"
        )

        # Enlarge screenshot text.
        width, height = image.size

        if width < 1800:
            scale = 2

            image = image.resize(
                (
                    width * scale,
                    height * scale,
                ),
                Image.Resampling.LANCZOS,
            )

        # Grayscale reduces visual noise.
        image = ImageOps.grayscale(
            image
        )

        # Improve dark/light separation.
        image = ImageOps.autocontrast(
            image,
            cutoff=1,
        )

        # Slight contrast enhancement.
        image = ImageEnhance.Contrast(
            image
        ).enhance(1.35)

        # Slight sharpening helps small chat text.
        image = image.filter(
            ImageFilter.SHARPEN
        )

        return image

    @staticmethod
    def _threshold(
        image: Image.Image,
    ) -> Image.Image:
        """
        Create a high-contrast black/white OCR image.
        """

        grayscale = ImageOps.grayscale(
            image
        )

        threshold = 175

        return grayscale.point(
            lambda pixel: (
                255
                if pixel > threshold
                else 0
            )
        )

    @staticmethod
    def _run_ocr(
        image: Image.Image,
    ) -> str:
        """
        Run Tesseract using a layout suitable for
        screenshot/chat text.
        """

        return pytesseract.image_to_string(
            image,
            config="--oem 3 --psm 6",
        )

    @staticmethod
    def _clean_text(
        text: str,
    ) -> str:
        """
        Normalize OCR output while preserving useful text.
        """

        if not text:
            return ""

        lines = []

        for raw_line in text.splitlines():
            line = raw_line.strip()

            if not line:
                continue

            # Collapse repeated whitespace.
            line = re.sub(
                r"[ \t]+",
                " ",
                line,
            )

            lines.append(line)

        return "\n".join(lines).strip()

    @classmethod
    def extract_urls(
        cls,
        text: str,
    ) -> List[str]:
        """
        Extract HTTP/HTTPS and www-style URLs from OCR text.
        """

        if not text:
            return []

        found = []

        for match in URL_PATTERN.findall(
            text
        ):
            found.append(
                cls._clean_url(
                    match
                )
            )

        for match in WWW_URL_PATTERN.findall(
            text
        ):
            cleaned = cls._clean_url(
                match
            )

            # Convert www.example.com into a URL that the
            # existing URL analyzer can process.
            if cleaned.lower().startswith(
                "www."
            ):
                cleaned = (
                    "https://"
                    + cleaned
                )

            found.append(
                cleaned
            )

        unique = []

        seen = set()

        for url in found:
            key = url.lower()

            if key in seen:
                continue

            seen.add(key)

            unique.append(
                url
            )

        return unique

    @staticmethod
    def _clean_url(
        url: str,
    ) -> str:
        """
        Remove punctuation accidentally captured at the
        end of an OCR-detected URL.
        """

        return url.rstrip(
            ".,;:!?)]}>\"'"
        )
