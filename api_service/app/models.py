"""
Mapeamento SQLAlchemy das tabelas criadas pelas migrations do Django
(admin_service). O Django é o dono do schema (roda as migrations);
a API FastAPI apenas lê e escreve nessas mesmas tabelas.

Convenção de nomes do Django: <app_label>_<model_name_lower>
"""
from datetime import date, datetime

from sqlalchemy import (
    Column, Integer, String, Boolean, Date, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship

from .database import Base


class Departamento(Base):
    __tablename__ = "rh_departamento"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), unique=True, nullable=False)

    funcionarios = relationship("Funcionario", back_populates="departamento")


class Funcionario(Base):
    __tablename__ = "rh_funcionario"

    id = Column(Integer, primary_key=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    cargo = Column(String(100), nullable=False)
    departamento_id = Column(Integer, ForeignKey("rh_departamento.id"), nullable=True)
    gestor_id = Column(Integer, ForeignKey("rh_funcionario.id"), nullable=True)
    saldo_ferias_dias = Column(Integer, default=30)
    ativo = Column(Boolean, default=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    departamento = relationship("Departamento", back_populates="funcionarios")
    ausencias = relationship("Ausencia", back_populates="funcionario",
                              foreign_keys="Ausencia.funcionario_id")


class TipoAusencia(Base):
    __tablename__ = "rh_tipoausencia"

    id = Column(Integer, primary_key=True)
    nome = Column(String(80), unique=True, nullable=False)
    remunerada = Column(Boolean, default=True)
    exige_anexo = Column(Boolean, default=False)


class Ausencia(Base):
    __tablename__ = "rh_ausencia"

    id = Column(Integer, primary_key=True)
    funcionario_id = Column(Integer, ForeignKey("rh_funcionario.id"), nullable=False)
    tipo_id = Column(Integer, ForeignKey("rh_tipoausencia.id"), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    dias_solicitados = Column(Integer, nullable=False)
    status = Column(String(10), default="PENDENTE")
    aprovado_por_id = Column(Integer, ForeignKey("rh_funcionario.id"), nullable=True)
    observacao = Column(Text, default="")
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    funcionario = relationship("Funcionario", back_populates="ausencias",
                                foreign_keys=[funcionario_id])
    tipo = relationship("TipoAusencia")
