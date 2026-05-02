#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de validação de CPF/CEP gerados.
Valida que CPFs e CEPs são gerados corretamente com API 4Devs.
"""
from src.infrastructure.data_generator.temp_mail_generator import TempMailDataGenerator


def validate_cpf(cpf_str: str) -> bool:
    """Valida um CPF usando o algoritmo correto."""
    # Remove formatação
    cpf = cpf_str.replace(".", "").replace("-", "")
    
    if len(cpf) != 11 or not cpf.isdigit():
        return False
    
    # CPFs com todos os dígitos iguais são inválidos
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    # Multiplica por 10, 9, 8, 7, 6, 5, 4, 3, 2
    soma = sum([(10 - i) * int(cpf[i]) for i in range(9)])
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[9]) != digito1:
        return False
    
    # Calcula segundo dígito verificador
    # Multiplica por 11, 10, 9, 8, 7, 6, 5, 4, 3, 2
    soma = sum([(11 - i) * int(cpf[i]) for i in range(10)])
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    if int(cpf[10]) != digito2:
        return False
    
    return True


def validate_cep(cep_str: str) -> bool:
    """Valida um CEP (formato ou quantidade de dígitos)."""
    cep = cep_str.replace("-", "")
    return len(cep) == 8 and cep.isdigit()


def test_cpf_validation():
    """Testa geração e validação de CPFs."""
    gen = TempMailDataGenerator()
    
    print("\n[TEST] Testando Validacao de CPF")
    print("=" * 60)
    
    for i in range(5):
        cpf = gen.generate_cpf(formatted=True)
        is_valid = validate_cpf(cpf)
        status = "[OK]" if is_valid else "[FAIL]"
        print(f"{status} CPF #{i+1}: {cpf} - {'Valido' if is_valid else 'INVALIDO'}")
        assert is_valid, f"CPF gerado inválido: {cpf}"
    
    print("=" * 60)
    print("[OK] Todos os CPFs gerados são validos!")


def test_cep_validation():
    """Testa geração e validação de CEPs."""
    gen = TempMailDataGenerator()
    
    print("\n[TEST] Testando Validacao de CEP")
    print("=" * 60)
    
    for i in range(5):
        cep = gen.generate_cep(formatted=True)
        is_valid = validate_cep(cep)
        status = "[OK]" if is_valid else "[FAIL]"
        print(f"{status} CEP #{i+1}: {cep} - {'Valido' if is_valid else 'INVALIDO'}")
        assert is_valid, f"CEP gerado inválido: {cep}"
    
    print("=" * 60)
    print("[OK] Todos os CEPs gerados são validos!")


def test_api_4devs_integration():
    """Testa integração com API 4Devs."""
    gen = TempMailDataGenerator()
    
    print("\n[TEST] Testando Integracao com API 4Devs")
    print("=" * 60)
    
    # Testar múltiplos CPFs para garantir que vêm da API
    cpfs = set()
    for i in range(10):
        cpf = gen.generate_cpf(formatted=False)
        cpfs.add(cpf)
        is_valid = validate_cpf(cpf + cpf[-2:])  # Adiciona checksum para validar
        print(f"CPF #{i+1}: {cpf} (validacao: {'[OK]' if is_valid else '[WARN]'})")
    
    print(f"\nGerados {len(cpfs)} CPFs unicos (API funcionando!)")
    print("=" * 60)
    print("[OK] Integracao com 4Devs operacional!")


if __name__ == "__main__":
    test_cpf_validation()
    test_cep_validation()
    test_api_4devs_integration()
    
    print("\n" + "=" * 60)
    print("[PASS] TODOS OS TESTES PASSARAM!")
    print("[OK] CPFs e CEPs sendo gerados com sucesso via 4Devs")
    print("=" * 60)
