"""A lightweight in-process translator for English and Hindi."""

from __future__ import annotations

import logging
import re

from app.translation.base_translator import BaseTranslator

logger = logging.getLogger(__name__)


class SimpleTranslator(BaseTranslator):
    """Translate a limited English-Hindi vocabulary with safe fallbacks."""

    def __init__(self) -> None:
        """Initialize phrase and token dictionaries."""
        self._supported_pairs = {
            ("en", "hi"),
            ("hi", "en"),
        }
        self._phrase_map = {
            ("en", "hi"): {
                "hello": "नमस्ते",
                "how are you": "आप कैसे हैं",
                "thank you": "धन्यवाद",
                "please help": "कृपया मदद करें",
                "good morning": "शुभ प्रभात",
            },
            ("hi", "en"): {
                "नमस्ते": "hello",
                "आप कैसे हैं": "how are you",
                "धन्यवाद": "thank you",
                "कृपया मदद करें": "please help",
                "शुभ प्रभात": "good morning",
            },
        }
        self._token_map = {
            ("en", "hi"): {
                "hello": "नमस्ते",
                "hi": "नमस्ते",
                "thanks": "धन्यवाद",
                "thank": "धन्यवाद",
                "you": "आप",
                "please": "कृपया",
                "help": "मदद",
                "document": "दस्तावेज़",
                "text": "पाठ",
                "image": "छवि",
                "translate": "अनुवाद",
                "language": "भाषा",
                "question": "प्रश्न",
                "answer": "उत्तर",
            },
            ("hi", "en"): {
                "नमस्ते": "hello",
                "धन्यवाद": "thank you",
                "कृपया": "please",
                "मदद": "help",
                "दस्तावेज़": "document",
                "पाठ": "text",
                "छवि": "image",
                "अनुवाद": "translate",
                "भाषा": "language",
                "प्रश्न": "question",
                "उत्तर": "answer",
                "आप": "you",
            },
        }

    def supports_language_pair(self, source_lang: str, target_lang: str) -> bool:
        """Return whether this provider supports the requested language pair."""
        return (source_lang, target_lang) in self._supported_pairs

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text using phrase lookup with token-based fallback."""
        if not text:
            logger.info("SimpleTranslator received empty text.")
            return ""

        if not self.supports_language_pair(source_lang, target_lang):
            raise ValueError(f"Unsupported language pair: {source_lang} -> {target_lang}")

        normalized_text = text.strip()
        phrase_translation = self._translate_phrase(normalized_text, source_lang, target_lang)
        if phrase_translation is not None:
            logger.debug("Translated text using phrase mapping.")
            return phrase_translation

        translated_text = self._translate_tokens(normalized_text, source_lang, target_lang)
        logger.debug("Translated text using token mapping fallback.")
        return translated_text

    def _translate_phrase(self, text: str, source_lang: str, target_lang: str) -> str | None:
        """Return a phrase-level translation when an exact mapping exists."""
        phrase_map = self._phrase_map.get((source_lang, target_lang), {})
        return phrase_map.get(text.lower() if source_lang == "en" else text)

    def _translate_tokens(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text token by token while preserving punctuation when possible."""
        token_map = self._token_map.get((source_lang, target_lang), {})
        tokens = re.findall(r"\w+|[^\w\s]", text, flags=re.UNICODE)
        translated_tokens: list[str] = []

        for token in tokens:
            if re.fullmatch(r"[^\w\s]", token, flags=re.UNICODE):
                translated_tokens.append(token)
                continue

            key = token.lower() if source_lang == "en" else token
            translated_tokens.append(token_map.get(key, token))

        combined_text = " ".join(translated_tokens)
        combined_text = re.sub(r"\s+([,.!?।])", r"\1", combined_text)
        return combined_text
