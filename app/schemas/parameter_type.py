from typing import Any, Optional

from pydantic import BaseModel, Json


class ParameterTypeCreate(BaseModel):
    name: str
    json: Json[Any]  # Usando Json do pydantic para lidar com JSON
    measure_unit: str
    qnt_decimals: int
    offset: Optional[float] = None
    factor: Optional[float] = None
    create_date: int
    last_update: int

    # Validação para garantir que offset e factor não são ambos nulos
    def validate_offset_factor(
        self,
    ) -> "ParameterTypeCreate":  # Adicionando a anotação de tipo para o retorno
        if self.offset is None and self.factor is None:
            raise ValueError("Offset e Factor não podem ser ambos nulos")
        return self

    class Config:
        orm_mode = True
