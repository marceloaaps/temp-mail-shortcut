"""
Clipboard Manager - COMPATIBILIDADE LEGADO.
Redireciona para nova arquitetura via adapter.
"""
from .legacy_adapters import LegacyClipboardManagerAdapter

# Alias para compatibilidade
ClipboardManager = LegacyClipboardManagerAdapter
