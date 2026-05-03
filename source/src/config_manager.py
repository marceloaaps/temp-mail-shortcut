"""
Gerenciador de configurações - COMPATIBILIDADE LEGADO.
Redireciona para nova arquitetura via adapter.
"""
from .legacy_adapters import LegacyConfigManagerAdapter

# Alias para compatibilidade
ConfigManager = LegacyConfigManagerAdapter
