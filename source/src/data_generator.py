"""
Gerador de Dados - COMPATIBILIDADE LEGADO.
Redireciona para nova arquitetura via adapter.
"""
from .legacy_adapters import LegacyDataGeneratorAdapter

# Alias para compatibilidade
DataGenerator = LegacyDataGeneratorAdapter
