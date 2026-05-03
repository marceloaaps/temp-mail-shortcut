"""
Logger centralizado para toda a aplicação.
Implementa ILogger.
"""
import sys
from typing import Optional
from ...domain.interfaces.repositories import ILogger


class ConsoleLogger(ILogger):
    """Logger que escreve no console."""
    
    def __init__(self, debug_mode: bool = False):
        self.debug_mode = debug_mode
    
    def debug(self, message: str) -> None:
        if self.debug_mode:
            print(f"🔍 DEBUG: {message}", file=sys.stderr)
    
    def info(self, message: str) -> None:
        print(f"ℹ️  {message}")
    
    def warning(self, message: str) -> None:
        print(f"⚠️  {message}", file=sys.stderr)
    
    def error(self, message: str) -> None:
        print(f"❌ {message}", file=sys.stderr)
