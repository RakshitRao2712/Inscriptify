"""Service layer for preparing text for downstream AI workflows."""

from __future__ import annotations

import logging
import re
from typing import Any

from app.processing.cleaner import TextCleaner
from app.processing.intent_detector import IntentDetector
from app.processing.language_detector import LanguageDetector

logger = logging.getLogger(__name__)


class Processor:
    """Coordinate text cleaning, segmentation, language detection, and intent extraction."""

    _SENTENCE_PATTERN = re.compile(r"(?<=[.!?।])\s+")

    def __init__(
        self,
        cleaner: TextCleaner | None = None,
        language_detector: LanguageDetector | None = None,
        intent_detector: IntentDetector | None = None,
    ) -> None:
        """Initialize the processor with injectable dependencies."""
        self.cleaner = cleaner or TextCleaner()
        self.language_detector = language_detector or LanguageDetector()
        self.intent_detector = intent_detector or IntentDetector()

    def process(self, text: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        """Process text and return a structured result for downstream services."""
        if text is None:
            logger.warning("Processor received None input.")
            text = ""

        logger.info("Processing text payload with original length %s.", len(text))
        cleaned_text = self.cleaner.clean(text)
        language = self.language_detector.detect(cleaned_text)
        sentences = self._segment_sentences(cleaned_text)
        intent = self.intent_detector.detect(cleaned_text)

        result_metadata = {
            "original_length": len(text),
            "clean_length": len(cleaned_text),
            "sentence_count": len(sentences),
            "is_empty": not bool(cleaned_text),
            "is_supported_language": language in {"en", "hi"},
            "pipeline": "rule_based_v1",
        }
        if metadata:
            result_metadata.update(metadata)

        result = {
            "clean_text": cleaned_text,
            "language": language,
            "sentences": sentences,
            "intent": intent,
            "metadata": result_metadata,
        }
        logger.debug("Processing result generated: %s", result)
        return result

    def _segment_sentences(self, text: str) -> list[str]:
        """Split normalized text into sentence-like chunks."""
        if not text:
            logger.info("Skipping sentence segmentation for empty text.")
            return []

        segments = self._SENTENCE_PATTERN.split(text)
        sentences = [segment.strip() for segment in segments if segment and segment.strip()]
        logger.debug("Segmented text into %s sentence(s).", len(sentences))
        return sentences
