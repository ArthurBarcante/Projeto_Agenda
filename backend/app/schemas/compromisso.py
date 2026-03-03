from datetime import datetime
from uuid import UUID

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

from app.models.compromisso import StatusCompromisso


class CompromissoAtualizacao(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    titulo: str | None = Field(
        default=None,
        validation_alias=AliasChoices("titulo", "title"),
    )
    descricao: str | None = Field(
        default=None,
        validation_alias=AliasChoices("descricao", "description"),
    )
    inicio_em: datetime | None = Field(
        default=None,
        validation_alias=AliasChoices("inicio_em", "starts_at"),
    )
    fim_em: datetime | None = Field(
        default=None,
        validation_alias=AliasChoices("fim_em", "ends_at"),
    )
    status: StatusCompromisso | None = None


class CompromissoCriacao(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    titulo: str = Field(validation_alias=AliasChoices("titulo", "title"))
    descricao: str | None = Field(
        default=None,
        validation_alias=AliasChoices("descricao", "description"),
    )
    inicio_em: datetime = Field(
        validation_alias=AliasChoices("inicio_em", "starts_at")
    )
    fim_em: datetime = Field(
        validation_alias=AliasChoices("fim_em", "ends_at")
    )
    participantes_ids: list[UUID] = Field(
        default_factory=list,
        validation_alias=AliasChoices("participantes_ids", "participant_ids"),
    )


class CompromissoResposta(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    empresa_id: UUID = Field(
        validation_alias=AliasChoices("empresa_id", "company_id")
    )
    criador_id: UUID = Field(
        validation_alias=AliasChoices("criador_id", "creator_id")
    )
    titulo: str = Field(validation_alias=AliasChoices("titulo", "title"))
    descricao: str | None = Field(
        default=None,
        validation_alias=AliasChoices("descricao", "description"),
    )
    inicio_em: datetime = Field(
        validation_alias=AliasChoices("inicio_em", "starts_at")
    )
    fim_em: datetime = Field(
        validation_alias=AliasChoices("fim_em", "ends_at")
    )
    status: StatusCompromisso
    created_at: datetime
    updated_at: datetime


class AtualizacaoCompromissoLegado(CompromissoAtualizacao):
    pass


class CriacaoCompromissoLegado(CompromissoCriacao):
    pass


class RespostaCompromissoLegado(CompromissoResposta):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    company_id: UUID = Field(validation_alias=AliasChoices("company_id", "empresa_id"))
    creator_id: UUID = Field(validation_alias=AliasChoices("creator_id", "criador_id"))
    title: str = Field(validation_alias=AliasChoices("title", "titulo"))
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "descricao"),
    )
    starts_at: datetime = Field(validation_alias=AliasChoices("starts_at", "inicio_em"))
    ends_at: datetime = Field(validation_alias=AliasChoices("ends_at", "fim_em"))