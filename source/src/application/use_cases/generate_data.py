"""
Casos de uso - Implementam a lógica de negócio da aplicação.
Dependem apenas de interfaces de domínio.
"""
from typing import Dict, Optional
from ...domain.interfaces.repositories import (
    IDataGenerator, IClipboardService, ILogger
)
from ...domain.entities.generated_data import GeneratedData


class GenerateCPFUseCase:
    """Caso de uso para gerar e copiar CPF."""
    
    def __init__(
        self,
        data_generator: IDataGenerator,
        clipboard_service: IClipboardService,
        logger: ILogger
    ):
        """
        Args:
            data_generator: Serviço de geração de dados
            clipboard_service: Serviço de clipboard
            logger: Serviço de logging
        """
        self.data_generator = data_generator
        self.clipboard_service = clipboard_service
        self.logger = logger
    
    def execute(self, formatted: bool = True) -> GeneratedData:
        """
        Executa o caso de uso.
        
        Returns:
            GeneratedData com CPF gerado
        """
        try:
            cpf = self.data_generator.generate_cpf(formatted)
            
            if self.clipboard_service.copy(cpf):
                self.logger.info(f"CPF copiado: {cpf}")
                return GeneratedData(
                    data_type="cpf",
                    value=cpf,
                    formatted=formatted
                )
            else:
                error_msg = "Erro ao copiar CPF para clipboard"
                self.logger.error(error_msg)
                return GeneratedData(
                    data_type="cpf",
                    value="",
                    error=error_msg
                )
        except Exception as e:
            error_msg = f"Erro ao gerar CPF: {str(e)}"
            self.logger.error(error_msg)
            return GeneratedData(
                data_type="cpf",
                value="",
                error=error_msg
            )


class GenerateCEPUseCase:
    """Caso de uso para gerar e copiar CEP."""
    
    def __init__(
        self,
        data_generator: IDataGenerator,
        clipboard_service: IClipboardService,
        logger: ILogger
    ):
        self.data_generator = data_generator
        self.clipboard_service = clipboard_service
        self.logger = logger
    
    def execute(self, formatted: bool = True) -> GeneratedData:
        """Executa o caso de uso."""
        try:
            cep = self.data_generator.generate_cep(formatted)
            
            if self.clipboard_service.copy(cep):
                self.logger.info(f"CEP copiado: {cep}")
                return GeneratedData(
                    data_type="cep",
                    value=cep,
                    formatted=formatted
                )
            else:
                error_msg = "Erro ao copiar CEP para clipboard"
                self.logger.error(error_msg)
                return GeneratedData(
                    data_type="cep",
                    value="",
                    error=error_msg
                )
        except Exception as e:
            error_msg = f"Erro ao gerar CEP: {str(e)}"
            self.logger.error(error_msg)
            return GeneratedData(
                data_type="cep",
                value="",
                error=error_msg
            )


class GenerateEmailUseCase:
    """Caso de uso para gerar e copiar email temporário."""
    
    def __init__(
        self,
        data_generator: IDataGenerator,
        clipboard_service: IClipboardService,
        logger: ILogger
    ):
        self.data_generator = data_generator
        self.clipboard_service = clipboard_service
        self.logger = logger
    
    def execute(self) -> GeneratedData:
        """Executa o caso de uso."""
        try:
            result = self.data_generator.generate_email()
            
            if result.get("error"):
                error_msg = result["error"]
                self.logger.warning(f"Email: {error_msg}")
                return GeneratedData(
                    data_type="email",
                    value="",
                    error=error_msg
                )
            
            email = result.get("email", "")
            
            if self.clipboard_service.copy(email):
                self.logger.info(f"Email copiado: {email}")
                return GeneratedData(
                    data_type="email",
                    value=email
                )
            else:
                error_msg = "Erro ao copiar email para clipboard"
                self.logger.error(error_msg)
                return GeneratedData(
                    data_type="email",
                    value="",
                    error=error_msg
                )
        except Exception as e:
            error_msg = f"Erro ao gerar email: {str(e)}"
            self.logger.error(error_msg)
            return GeneratedData(
                data_type="email",
                value="",
                error=error_msg
            )
