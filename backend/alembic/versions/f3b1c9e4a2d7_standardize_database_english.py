"""standardize database naming to english

Revision ID: f3b1c9e4a2d7
Revises: e1a9d4b7c2f6
Create Date: 2026-03-06 20:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f3b1c9e4a2d7"
down_revision: Union[str, Sequence[str], None] = "e1a9d4b7c2f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _table_exists(table_name: str) -> bool:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    return table_name in set(inspector.get_table_names())


def _rename_table_if_exists(old_name: str, new_name: str) -> None:
    if _table_exists(old_name) and not _table_exists(new_name):
        op.rename_table(old_name, new_name)


def _rename_column_if_exists(table_name: str, old_name: str, new_name: str) -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if table_name not in set(inspector.get_table_names()):
        return

    columns = {column["name"] for column in inspector.get_columns(table_name)}
    if old_name in columns and new_name not in columns:
        op.alter_column(table_name, old_name, new_column_name=new_name)


def _rename_constraint_if_exists(table_name: str, old_name: str, new_name: str) -> None:
    if not _table_exists(table_name):
        return

    op.execute(
        sa.text(
            """
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM pg_constraint c
                    JOIN pg_class t ON t.oid = c.conrelid
                    JOIN pg_namespace n ON n.oid = t.relnamespace
                    WHERE c.conname = :old_name
                      AND t.relname = :table_name
                      AND n.nspname = current_schema()
                )
                AND NOT EXISTS (
                    SELECT 1
                    FROM pg_constraint
                    WHERE conname = :new_name
                ) THEN
                    EXECUTE format(
                        'ALTER TABLE %I RENAME CONSTRAINT %I TO %I',
                        :table_name,
                        :old_name,
                        :new_name
                    );
                END IF;
            END
            $$;
            """
        ).bindparams(table_name=table_name, old_name=old_name, new_name=new_name)
    )


def _rename_index_if_exists(old_name: str, new_name: str) -> None:
    op.execute(
        sa.text(
            """
            DO $$
            BEGIN
                IF to_regclass(:old_name) IS NOT NULL
                   AND to_regclass(:new_name) IS NULL THEN
                    EXECUTE format('ALTER INDEX %I RENAME TO %I', :old_name, :new_name);
                END IF;
            END
            $$;
            """
        ).bindparams(old_name=old_name, new_name=new_name)
    )


def upgrade() -> None:
    _rename_table_if_exists("empresas", "companies")
    _rename_table_if_exists("usuarios", "users")
    _rename_table_if_exists("compromissos", "appointments")
    _rename_table_if_exists("participantes_compromissos", "appointment_participants")

    _rename_column_if_exists("companies", "nome", "name")
    _rename_column_if_exists("companies", "identificador", "slug")
    _rename_column_if_exists("companies", "plano", "plan")
    _rename_column_if_exists("companies", "ativo", "is_active")

    _rename_column_if_exists("users", "empresa_id", "company_id")
    _rename_column_if_exists("users", "nome", "name")
    _rename_column_if_exists("users", "hash_senha", "password_hash")
    _rename_column_if_exists("users", "ativo", "is_active")

    _rename_column_if_exists("appointments", "empresa_id", "company_id")
    _rename_column_if_exists("appointments", "criador_id", "creator_id")
    _rename_column_if_exists("appointments", "titulo", "title")
    _rename_column_if_exists("appointments", "descricao", "description")
    _rename_column_if_exists("appointments", "inicio_em", "start_time")
    _rename_column_if_exists("appointments", "fim_em", "end_time")
    _rename_column_if_exists("appointments", "estado", "status")

    _rename_column_if_exists("appointment_participants", "empresa_id", "company_id")
    _rename_column_if_exists("appointment_participants", "compromisso_id", "appointment_id")
    _rename_column_if_exists("appointment_participants", "usuario_id", "user_id")

    _rename_column_if_exists("audit_logs", "empresa_id", "company_id")
    _rename_column_if_exists("audit_logs", "usuario_id", "user_id")
    _rename_column_if_exists("audit_logs", "acao", "action")
    _rename_column_if_exists("audit_logs", "entidade", "entity")
    _rename_column_if_exists("audit_logs", "entidade_id", "entity_id")
    _rename_column_if_exists("audit_logs", "dados_antes", "before_data")
    _rename_column_if_exists("audit_logs", "dados_depois", "after_data")
    _rename_column_if_exists("audit_logs", "criado_em", "created_at")

    _rename_column_if_exists("idempotency_keys", "empresa_id", "company_id")
    _rename_column_if_exists("idempotency_keys", "chave", "key")
    _rename_column_if_exists("idempotency_keys", "metodo", "method")
    _rename_column_if_exists("idempotency_keys", "criado_em", "created_at")

    _rename_column_if_exists("roles", "empresa_id", "company_id")
    _rename_column_if_exists("roles", "nome", "name")
    _rename_column_if_exists("roles", "descricao", "description")
    _rename_column_if_exists("roles", "criado_em", "created_at")

    _rename_column_if_exists("permissions", "codigo", "code")
    _rename_column_if_exists("permissions", "descricao", "description")

    _rename_column_if_exists("user_roles", "usuario_id", "user_id")

    _rename_column_if_exists("outbox_events", "empresa_id", "company_id")
    _rename_column_if_exists("outbox_events", "tipo_evento", "event_type")
    _rename_column_if_exists("outbox_events", "tentativas", "attempts")
    _rename_column_if_exists("outbox_events", "criado_em", "created_at")
    _rename_column_if_exists("outbox_events", "processar_em", "process_at")

    _rename_column_if_exists("webhook_subscriptions", "empresa_id", "company_id")
    _rename_column_if_exists("webhook_subscriptions", "ativo", "is_active")
    _rename_column_if_exists("webhook_subscriptions", "criado_em", "created_at")

    _rename_constraint_if_exists("users", "uq_usuario_empresa_email", "uq_user_company_email")
    _rename_constraint_if_exists(
        "appointment_participants",
        "uq_participante_compromisso_usuario",
        "uq_appointment_participant_user",
    )
    _rename_constraint_if_exists(
        "idempotency_keys",
        "uq_idempotency_keys_empresa_chave",
        "uq_idempotency_keys_company_key",
    )
    _rename_constraint_if_exists(
        "appointments",
        "ex_compromissos_tenant_periodo_sem_sobreposicao",
        "ex_appointments_tenant_period_no_overlap",
    )

    _rename_index_if_exists(
        "ix_compromissos_empresa_inicio_fim_status",
        "ix_appointments_company_start_end_status",
    )
    _rename_index_if_exists(
        "ix_participantes_compromissos_usuario_compromisso",
        "ix_appointment_participants_user_appointment",
    )
    _rename_index_if_exists("ix_audit_logs_usuario_id", "ix_audit_logs_user_id")
    _rename_index_if_exists(
        "ix_audit_logs_empresa_entidade_criado",
        "ix_audit_logs_company_entity_created",
    )
    _rename_index_if_exists("ix_roles_empresa_id", "ix_roles_company_id")
    _rename_index_if_exists("ix_permissions_codigo", "ix_permissions_code")
    _rename_index_if_exists("ix_user_roles_usuario_id", "ix_user_roles_user_id")
    _rename_index_if_exists("ix_outbox_events_empresa_id", "ix_outbox_events_company_id")
    _rename_index_if_exists("ix_outbox_events_processar_em", "ix_outbox_events_process_at")
    _rename_index_if_exists(
        "ix_webhook_subscriptions_empresa_evento_ativo",
        "ix_webhook_subscriptions_company_event_active",
    )


def downgrade() -> None:
    _rename_index_if_exists(
        "ix_appointments_company_start_end_status",
        "ix_compromissos_empresa_inicio_fim_status",
    )
    _rename_index_if_exists(
        "ix_appointment_participants_user_appointment",
        "ix_participantes_compromissos_usuario_compromisso",
    )
    _rename_index_if_exists("ix_audit_logs_user_id", "ix_audit_logs_usuario_id")
    _rename_index_if_exists(
        "ix_audit_logs_company_entity_created",
        "ix_audit_logs_empresa_entidade_criado",
    )
    _rename_index_if_exists("ix_roles_company_id", "ix_roles_empresa_id")
    _rename_index_if_exists("ix_permissions_code", "ix_permissions_codigo")
    _rename_index_if_exists("ix_user_roles_user_id", "ix_user_roles_usuario_id")
    _rename_index_if_exists("ix_outbox_events_company_id", "ix_outbox_events_empresa_id")
    _rename_index_if_exists("ix_outbox_events_process_at", "ix_outbox_events_processar_em")
    _rename_index_if_exists(
        "ix_webhook_subscriptions_company_event_active",
        "ix_webhook_subscriptions_empresa_evento_ativo",
    )

    _rename_constraint_if_exists("users", "uq_user_company_email", "uq_usuario_empresa_email")
    _rename_constraint_if_exists(
        "appointment_participants",
        "uq_appointment_participant_user",
        "uq_participante_compromisso_usuario",
    )
    _rename_constraint_if_exists(
        "idempotency_keys",
        "uq_idempotency_keys_company_key",
        "uq_idempotency_keys_empresa_chave",
    )
    _rename_constraint_if_exists(
        "appointments",
        "ex_appointments_tenant_period_no_overlap",
        "ex_compromissos_tenant_periodo_sem_sobreposicao",
    )

    _rename_column_if_exists("companies", "name", "nome")
    _rename_column_if_exists("companies", "slug", "identificador")
    _rename_column_if_exists("companies", "plan", "plano")
    _rename_column_if_exists("companies", "is_active", "ativo")

    _rename_column_if_exists("users", "company_id", "empresa_id")
    _rename_column_if_exists("users", "name", "nome")
    _rename_column_if_exists("users", "password_hash", "hash_senha")
    _rename_column_if_exists("users", "is_active", "ativo")

    _rename_column_if_exists("appointments", "company_id", "empresa_id")
    _rename_column_if_exists("appointments", "creator_id", "criador_id")
    _rename_column_if_exists("appointments", "title", "titulo")
    _rename_column_if_exists("appointments", "description", "descricao")
    _rename_column_if_exists("appointments", "start_time", "inicio_em")
    _rename_column_if_exists("appointments", "end_time", "fim_em")
    _rename_column_if_exists("appointments", "status", "estado")

    _rename_column_if_exists("appointment_participants", "company_id", "empresa_id")
    _rename_column_if_exists("appointment_participants", "appointment_id", "compromisso_id")
    _rename_column_if_exists("appointment_participants", "user_id", "usuario_id")

    _rename_column_if_exists("audit_logs", "company_id", "empresa_id")
    _rename_column_if_exists("audit_logs", "user_id", "usuario_id")
    _rename_column_if_exists("audit_logs", "action", "acao")
    _rename_column_if_exists("audit_logs", "entity", "entidade")
    _rename_column_if_exists("audit_logs", "entity_id", "entidade_id")
    _rename_column_if_exists("audit_logs", "before_data", "dados_antes")
    _rename_column_if_exists("audit_logs", "after_data", "dados_depois")
    _rename_column_if_exists("audit_logs", "created_at", "criado_em")

    _rename_column_if_exists("idempotency_keys", "company_id", "empresa_id")
    _rename_column_if_exists("idempotency_keys", "key", "chave")
    _rename_column_if_exists("idempotency_keys", "method", "metodo")
    _rename_column_if_exists("idempotency_keys", "created_at", "criado_em")

    _rename_column_if_exists("roles", "company_id", "empresa_id")
    _rename_column_if_exists("roles", "name", "nome")
    _rename_column_if_exists("roles", "description", "descricao")
    _rename_column_if_exists("roles", "created_at", "criado_em")

    _rename_column_if_exists("permissions", "code", "codigo")
    _rename_column_if_exists("permissions", "description", "descricao")

    _rename_column_if_exists("user_roles", "user_id", "usuario_id")

    _rename_column_if_exists("outbox_events", "company_id", "empresa_id")
    _rename_column_if_exists("outbox_events", "event_type", "tipo_evento")
    _rename_column_if_exists("outbox_events", "attempts", "tentativas")
    _rename_column_if_exists("outbox_events", "created_at", "criado_em")
    _rename_column_if_exists("outbox_events", "process_at", "processar_em")

    _rename_column_if_exists("webhook_subscriptions", "company_id", "empresa_id")
    _rename_column_if_exists("webhook_subscriptions", "is_active", "ativo")
    _rename_column_if_exists("webhook_subscriptions", "created_at", "criado_em")

    _rename_table_if_exists("appointment_participants", "participantes_compromissos")
    _rename_table_if_exists("appointments", "compromissos")
    _rename_table_if_exists("users", "usuarios")
    _rename_table_if_exists("companies", "empresas")
