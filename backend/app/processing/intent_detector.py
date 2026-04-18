"""Rule-based intent detection for processed text."""

from __future__ import annotations

import logging
import re
from typing import Pattern

logger = logging.getLogger(__name__)


class IntentDetector:
    """Infer a basic intent from text using rule-based patterns."""

    def __init__(self) -> None:
        """Initialize rule patterns used for intent inference."""
        self._patterns: list[tuple[str, Pattern[str]]] = [
            ("greeting", re.compile(r"\b(hi|hello|hey|namaste)\b", re.IGNORECASE)),
            (
                "translation_request",
                re.compile(r"\b(translate|translation|anuvad|अनुवाद)\b", re.IGNORECASE),
            ),
            (
                "help_request",
                re.compile(r"\b(help|support|assist|problem|issue)\b", re.IGNORECASE),
            ),
            (
                "question",
                re.compile(r"\b(what|why|how|when|where|who|can|could|should)\b|\?$", re.IGNORECASE),
            ),
            (
                "ocr_text",
                re.compile(r"\b(invoice|receipt|document|page|scan|form)\b", re.IGNORECASE),
            ),
        ]

    def detect(self, text: str) -> str:
        """Return the detected intent for the supplied text."""
        if not text:
            logger.info("Empty text received for intent detection.")
            return "empty_input"

        stripped_text = text.strip()
        for intent, pattern in self._patterns:
            if pattern.search(stripped_text):
                logger.debug("Detected intent '%s'.", intent)
                return intent

        if stripped_text.endswith("?"):
            logger.debug("Detected fallback question intent.")
            return "question"

        logger.debug("No specific intent matched. Falling back to 'statement'.")
        return "statement"
