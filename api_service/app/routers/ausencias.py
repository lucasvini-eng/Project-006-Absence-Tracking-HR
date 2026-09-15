from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..schemas.ausencia import AusenciaCreate, AusenciaOut, AusenciaAprovar

router = APIRouter(prefix="/ausencias", tags=["Ausências"])


@router.post("/", response_model=AusenciaOut, status_code=201)
def solicitar_ausencia(payload: AusenciaCreate, db: Session = Depends(get_db)):
    funcionario = db.get(models.Funcionario, payload.funcionario_id)
    if not funcionario:
        raise HTTPException(404, "Funcionário não encontrado")

    tipo = db.get(models.TipoAusencia, payload.tipo_id)
    if not tipo:
        raise HTTPException(404, "Tipo de ausência não encontrado")

    dias = (payload.data_fim - payload.data_inicio).days + 1
    if dias <= 0:
        raise HTTPException(400, "Data final deve ser posterior à data inicial")

    if tipo.nome.lower() == "férias" and dias > funcionario.saldo_ferias_dias:
        raise HTTPException(400, "Saldo de férias insuficiente")

    nova = models.Ausencia(
        funcionario_id=payload.funcionario_id,
        tipo_id=payload.tipo_id,
        data_inicio=payload.data_inicio,
        data_fim=payload.data_fim,
        dias_solicitados=dias,
        observacao=payload.observacao or "",
        status="PENDENTE",
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@router.get("/", response_model=list[AusenciaOut])
def listar_ausencias(
    status_filtro: str | None = None,
    funcionario_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Ausencia)
    if status_filtro:
        query = query.filter(models.Ausencia.status == status_filtro.upper())
    if funcionario_id:
        query = query.filter(models.Ausencia.funcionario_id == funcionario_id)
    return query.order_by(models.Ausencia.criado_em.desc()).all()


@router.get("/{ausencia_id}", response_model=AusenciaOut)
def obter_ausencia(ausencia_id: int, db: Session = Depends(get_db)):
    ausencia = db.get(models.Ausencia, ausencia_id)
    if not ausencia:
        raise HTTPException(404, "Ausência não encontrada")
    return ausencia


@router.post("/{ausencia_id}/aprovar", response_model=AusenciaOut)
def aprovar_ausencia(ausencia_id: int, payload: AusenciaAprovar, db: Session = Depends(get_db)):
    ausencia = db.get(models.Ausencia, ausencia_id)
    if not ausencia:
        raise HTTPException(404, "Ausência não encontrada")
    if ausencia.status != "PENDENTE":
        raise HTTPException(400, f"Ausência já está {ausencia.status}")

    ausencia.status = "APROVADA"
    ausencia.aprovado_por_id = payload.aprovado_por_id
    ausencia.observacao = payload.observacao or ausencia.observacao

    tipo = db.get(models.TipoAusencia, ausencia.tipo_id)
    if tipo and tipo.nome.lower() == "férias":
        funcionario = db.get(models.Funcionario, ausencia.funcionario_id)
        funcionario.saldo_ferias_dias -= ausencia.dias_solicitados

    db.commit()
    db.refresh(ausencia)
    return ausencia


@router.post("/{ausencia_id}/rejeitar", response_model=AusenciaOut)
def rejeitar_ausencia(ausencia_id: int, payload: AusenciaAprovar, db: Session = Depends(get_db)):
    ausencia = db.get(models.Ausencia, ausencia_id)
    if not ausencia:
        raise HTTPException(404, "Ausência não encontrada")
    if ausencia.status != "PENDENTE":
        raise HTTPException(400, f"Ausência já está {ausencia.status}")

    ausencia.status = "REJEITADA"
    ausencia.aprovado_por_id = payload.aprovado_por_id
    ausencia.observacao = payload.observacao or ausencia.observacao
    db.commit()
    db.refresh(ausencia)
    return ausencia
