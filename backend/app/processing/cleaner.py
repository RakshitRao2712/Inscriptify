"""Utilities for cleaning and normalizing text input."""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)


class TextCleaner:
    """Clean raw OCR or user-provided text for downstream processing."""

    _CONTROL_CHAR_PATTERN = re.compile(r"[\x00-\x08\x0B-\x1F\x7F]")
    _SPACE_PATTERN = re.compile(r"\s+")
    _SYMBOL_NOISE_PATTERN = re.compile(r"[^\w\s.,!?;:'\"()\-/%@#&\u0900-\u097F]")
    _REPEATED_PUNCT_PATTERN = re.compile(r"([!?.,]){2,}")

    def clean(self, text: str) -> str:
        """Return a normalized representation of the supplied text."""
        if text is None:
            logger.warning("Received None while cleaning text.")
            return ""

        logger.debug("Cleaning text with length %s.", len(text))
        normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
        normalized_text = self._CONTROL_CHAR_PATTERN.sub(" ", normalized_text)
        normalized_text = self._SYMBOL_NOISE_PATTERN.sub(" ", normalized_text)
        normalized_text = self._REPEATED_PUNCT_PATTERN.sub(r"\1", normalized_text)
        normalized_text = re.sub(r"\s*\n\s*", " ", normalized_text)
        normalized_text = self._SPACE_PATTERN.sub(" ", normalized_text)
        cleaned_text = normalized_text.strip()
        logger.debug("Finished cleaning text. Result length: %s.", len(cleaned_text))
        return cleaned_text
