"""Skema awal Visit Flow.

Revision ID: 0001
Revises:
Create Date: 2026-11-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("username", sa.String(length=60), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("username", name="uq_users_username"),
    )

    op.create_table(
        "entities",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("type", sa.String(length=60), nullable=False),
        sa.Column("segment", sa.String(length=3), nullable=False),
        sa.Column("region", sa.String(length=80), nullable=False),
        sa.CheckConstraint(
            "segment IN ('B2G', 'B2B')", name="ck_entities_segment"
        ),
        sa.PrimaryKeyConstraint("id", name="pk_entities"),
    )

    op.create_table(
        "activities",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=True),
        sa.Column("entity_name", sa.String(length=160), nullable=False),
        sa.Column("entity_type", sa.String(length=60), nullable=False),
        sa.Column("entity_region", sa.String(length=80), nullable=False),
        sa.Column("segment", sa.String(length=3), nullable=False),
        sa.Column("visit_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("sales_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint(
            "segment IN ('B2G', 'B2B')", name="ck_activities_segment"
        ),
        sa.CheckConstraint(
            "status IN ('NOT_VISITED', 'VISITED')",
            name="ck_activities_status",
        ),
        sa.ForeignKeyConstraint(
            ["entity_id"],
            ["entities.id"],
            name="fk_activities_entity_id_entities",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["sales_id"],
            ["users.id"],
            name="fk_activities_sales_id_users",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_activities"),
    )
    op.create_index(
        "ix_activities_visit_date", "activities", ["visit_date"], unique=False
    )
    op.create_index(
        "ix_activities_sales_id", "activities", ["sales_id"], unique=False
    )
    op.create_index(
        "ix_activities_segment", "activities", ["segment"], unique=False
    )
    op.create_index(
        "ix_activities_status", "activities", ["status"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_activities_status", table_name="activities")
    op.drop_index("ix_activities_segment", table_name="activities")
    op.drop_index("ix_activities_sales_id", table_name="activities")
    op.drop_index("ix_activities_visit_date", table_name="activities")
    op.drop_table("activities")
    op.drop_table("entities")
    op.drop_table("users")
