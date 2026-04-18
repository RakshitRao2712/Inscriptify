"""Service layer for translating processed text into target languages."""

from __future__ import annotations

import logging
from typing import Any

from app.processing.language_detector import LanguageDetector
from app.translation.base_translator import BaseTranslator
from app.translation.implementations.simple_translator import SimpleTranslator

logger = logging.getLogger(__name__)


class Translator:
    """Coordinate translation providers and apply fallback behavior."""

    def __init__(
        self,
        translators: list[BaseTranslator] | None = None,
        language_detector: LanguageDetector | None = None,
    ) -> None:
        """Initialize the translation service with injectable dependencies."""
        self.translators = translators or [SimpleTranslator()]
        self.language_detector = language_detector or LanguageDetector()

    def translate(
        self,
        text: str | dict[str, Any],
        target_lang: str = "hi",
        source_lang: str | None = None,
    ) -> dict[str, Any]:
        """Translate raw or processed text into the requested target language."""
        original_text = self._extract_text(text)
        if not original_text:
            logger.info("Empty text received for translation.")
            return {
                "original_text": "",
                "translated_text": "",
                "source_lang": source_lang or "unknown",
                "target_lang": target_lang,
                "metadata": {
                    "fallback_used": True,
                    "reason": "empty_input",
                },
            }

        resolved_source_lang = source_lang or self._resolve_source_language(text, original_text)
        logger.info(
            "Attempting translation from '%s' to '%s'.",
            resolved_source_lang,
            target_lang,
        )

        if resolved_source_lang == target_lang:
            logger.info("Source and target languages are the same; skipping translation.")
            return {
                "original_text": original_text,
                "translated_text": original_text,
                "source_lang": resolved_source_lang,
                "target_lang": target_lang,
                "metadata": {
                    "fallback_used": False,
                    "reason": "same_language",
                },
            }

        provider = self._select_translator(resolved_source_lang, target_lang)
        if provider is None:
            logger.warning(
                "No translator found for language pair %s -> %s.",
                resolved_source_lang,
                target_lang,
            )
            return self._fallback_response(
                original_text=original_text,
                source_lang=resolved_source_lang,
                target_lang=target_lang,
                reason="unsupported_language_pair",
            )

        try:
            translated_text = provider.translate(
                text=original_text,
                source_lang=resolved_source_lang,
                target_lang=target_lang,
            )
        except Exception as exc:  # pragma: no cover - defensive fallback
            logger.exception("Translation provider failed: %s", exc)
            return self._fallback_response(
                original_text=original_text,
                source_lang=resolved_source_lang,
                target_lang=target_lang,
                reason="provider_error",
            )

        return {
            "original_text": original_text,
            "translated_text": translated_text,
            "source_lang": resolved_source_lang,
            "target_lang": target_lang,
            "metadata": {
                "fallback_used": False,
                "provider": provider.__class__.__name__,
            },
        }

    def _extract_text(self, payload: str | dict[str, Any]) -> str:
        """Return the most appropriate text field from raw or processed input."""
        if isinstance(payload, dict):
            extracted_text = payload.get("clean_text") or payload.get("text") or ""
            return str(extracted_text).strip()
        return str(payload).strip()

    def _resolve_source_language(self, payload: str | dict[str, Any], text: str) -> str:
        """Resolve the source language from processed payloads or detector heuristics."""
        if isinstance(payload, dict) and payload.get("language"):
            return str(payload["language"])
        return self.language_detector.detect(text)

    def _select_translator(self, source_lang: str, target_lang: str) -> BaseTranslator | None:
        """Select the first provider that supports the requested language pair."""
        for translator in self.translators:
            if translator.supports_language_pair(source_lang, target_lang):
                return translator
        return None

    def _fallback_response(
        self,
        original_text: str,
        source_lang: str,
        target_lang: str,
        reason: str,
    ) -> dict[str, Any]:
        """Return a safe fallback response when translation cannot be completed."""
        return {
            "original_text": original_text,
            "translated_text": original_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "metadata": {
                "fallback_used": True,
                "reason": reason,
            },
        }
