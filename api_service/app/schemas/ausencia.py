from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AusenciaCreate(BaseModel):
    funcionario_id: int
    tipo_id: int
    data_inicio: date
    data_fim: date
    observacao: Optional[str] = ""


class AusenciaAprovar(BaseModel):
    aprovado_por_id: int
    observacao: Optional[str] = ""


class AusenciaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    funcionario_id: int
    tipo_id: int
    data_inicio: date
    data_fim: date
    dias_solicitados: int
    status: str
    aprovado_por_id: Optional[int] = None
    observacao: str
    criado_em: datetime
    atualizado_em: datetime
