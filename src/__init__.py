"""
LLM Prompt Injection Testing Platform

A comprehensive platform for testing and evaluating LLM security 
against various prompt injection attacks.
"""

__version__ = "1.0.0"
__author__ = "LLM Security Research Team"
__license__ = "MIT"

from .core.platform import PromptInjectionPlatform
from .providers.base import BaseProvider
from .attacks.base_attack import BaseAttack

__all__ = [
    "PromptInjectionPlatform",
    "BaseProvider", 
    "BaseAttack"
]