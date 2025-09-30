"""
LLM Prompt Injection Testing Platform

A comprehensive platform for testing and evaluating LLM security 
against various prompt injection attacks.
"""

__version__ = "1.0.0"
__author__ = "LLM Security Research Team"
__license__ = "MIT"

from .providers.base import BaseProvider
from .core.attacks import BaseAttack, AttackManager
from .core.report_generator import AttackReportGenerator

__all__ = [
    "BaseProvider", 
    "BaseAttack",
    "AttackManager",
    "AttackReportGenerator"
]