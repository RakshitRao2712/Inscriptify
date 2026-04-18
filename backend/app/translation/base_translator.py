"""Abstract base classes for translation providers."""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseTranslator(ABC):
    """Define the interface implemented by translation providers."""

    @abstractmethod
    def supports_language_pair(self, source_lang: str, target_lang: str) -> bool:
        """Return whether the provider can translate the requested language pair."""

    @abstractmethod
    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text from the source language into the target language."""
