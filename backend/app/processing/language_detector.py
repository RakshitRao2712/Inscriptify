"""Lightweight language detection utilities."""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)


class LanguageDetector:
    """Detect supported languages using script and keyword heuristics."""

    _DEVANAGARI_PATTERN = re.compile(r"[\u0900-\u097F]")
    _ENGLISH_HINTS = {
        "the",
        "and",
        "is",
        "are",
        "please",
        "translate",
        "help",
        "document",
        "what",
        "how",
    }
    _HINDI_HINTS = {
        "है",
        "और",
        "क्या",
        "कृपया",
        "अनुवाद",
        "मदद",
        "दस्तावेज़",
        "यह",
    }

    def detect(self, text: str) -> str:
        """Return an ISO-style short language code for the supplied text."""
        if not text or not text.strip():
            logger.info("Empty text received for language detection.")
            return "unknown"

        normalized_text = text.strip()
        if self._contains_devanagari(normalized_text):
            logger.debug("Detected Hindi based on Devanagari characters.")
            return "hi"

        lowered_words = {word.lower() for word in re.findall(r"\b[\w']+\b", normalized_text)}
        if lowered_words & self._ENGLISH_HINTS:
            logger.debug("Detected English based on keyword hints.")
            return "en"

        if self._contains_hindi_keywords(normalized_text):
            logger.debug("Detected Hindi based on keyword hints.")
            return "hi"

        if re.search(r"[A-Za-z]", normalized_text):
            logger.debug("Detected English based on Latin characters fallback.")
            return "en"

        logger.warning("Unable to confidently detect language.")
        return "unknown"

    def _contains_devanagari(self, text: str) -> bool:
        """Return whether the text contains Devanagari script characters."""
        return bool(self._DEVANAGARI_PATTERN.search(text))

    def _contains_hindi_keywords(self, text: str) -> bool:
        """Return whether the text contains common Hindi tokens."""
        return any(token in text for token in self._HINDI_HINTS)
