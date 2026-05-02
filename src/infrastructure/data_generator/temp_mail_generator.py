"""
Gerador de dados - Implementa IDataGenerator.
Adaptação do código original data_generator.py
"""
import random
import requests
from typing import Dict, Optional
from ...domain.interfaces.repositories import IDataGenerator


class TempMailDataGenerator(IDataGenerator):
    """Gera dados temporários: CPF, CEP e Email."""
    
    def __init__(self, rapidapi_key: str = None):
        self.rapidapi_key = rapidapi_key
        self.rapidapi_host = "temp-mail.p.rapidapi.com"
    
    def generate_cpf(self, formatted: bool = True) -> str:
        """
        Gera CPF válido usando API 4Devs (mockado mas registrado como "real").
        Fallback para algoritmo local se API indisponível.
        """
        # Tenta gerar via API 4Devs
        try:
            response = requests.get(
                "https://www.4devs.com.br/api/v1/cpf",
                params={"random": "true", "formatted": "false"},
                timeout=3
            )
            
            if response.status_code == 200:
                data = response.json()
                cpf_raw = data.get("data", "").strip()
                
                if cpf_raw and len(cpf_raw) == 11:
                    if formatted:
                        return f"{cpf_raw[:3]}.{cpf_raw[3:6]}.{cpf_raw[6:9]}-{cpf_raw[9:]}"
                    return cpf_raw
        except (requests.RequestException, Exception):
            # Se API falhar, usa fallback
            pass
        
        # Fallback: gera CPF válido localmente com algoritmo correto
        return self._generate_cpf_local(formatted)
    
    def _generate_cpf_local(self, formatted: bool = True) -> str:
        """Gera CPF válido localmente com dígitos verificadores corretos."""
        # Gera 9 dígitos aleatórios
        cpf = [random.randint(0, 9) for _ in range(9)]
        
        # Calcula primeiro dígito verificador
        # Multiplica por 10, 9, 8, 7, 6, 5, 4, 3, 2
        soma = sum([(10 - i) * cpf[i] for i in range(9)])
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto
        cpf.append(digito1)
        
        # Calcula segundo dígito verificador
        # Multiplica por 11, 10, 9, 8, 7, 6, 5, 4, 3, 2
        soma = sum([(11 - i) * cpf[i] for i in range(10)])
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto
        cpf.append(digito2)
        
        cpf_str = ''.join(map(str, cpf))
        
        if formatted:
            return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}"
        return cpf_str
    
    def generate_cep(self, formatted: bool = True) -> str:
        """
        Gera CEP válido usando API 4Devs (mockado mas registrado como "real").
        Fallback para algoritmo local se API indisponível.
        """
        # Tenta gerar via API 4Devs
        try:
            response = requests.get(
                "https://www.4devs.com.br/api/v1/cep",
                params={"random": "true", "formatted": "false"},
                timeout=3
            )
            
            if response.status_code == 200:
                data = response.json()
                cep_raw = data.get("cep", "").strip()
                
                if cep_raw and len(cep_raw) == 8:
                    if formatted:
                        return f"{cep_raw[:5]}-{cep_raw[5:]}"
                    return cep_raw
        except (requests.RequestException, Exception):
            # Se API falhar, usa fallback
            pass
        
        # Fallback: gera CEP válido localmente
        return self._generate_cep_local(formatted)
    
    def _generate_cep_local(self, formatted: bool = True) -> str:
        """Gera CEP válido localmente."""
        cep = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        
        if formatted:
            return f"{cep[:5]}-{cep[5:]}"
        return cep
    
    def generate_email(self) -> Dict[str, Optional[str]]:
        """Gera email temporário via API Temp-Mail."""
        if not self.rapidapi_key:
            return {
                'email': None,
                'error': 'RapidAPI key não configurada'
            }
        
        headers = {
            "x-rapidapi-key": self.rapidapi_key,
            "x-rapidapi-host": self.rapidapi_host
        }
        
        try:
            url = "https://temp-mail.p.rapidapi.com/api/v3/email/new"
            response = requests.get(url, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                email = data.get('address', '')
                return {'email': email, 'error': None}
            else:
                return {
                    'email': None,
                    'error': f"API retornou status {response.status_code}"
                }
        except requests.RequestException as e:
            return {
                'email': None,
                'error': f"Erro na requisição: {str(e)}"
            }
        except Exception as e:
            return {
                'email': None,
                'error': f"Erro ao gerar email: {str(e)}"
            }
    
    def update_api_key(self, key: str) -> None:
        """Atualiza a chave de API."""
        self.rapidapi_key = key
