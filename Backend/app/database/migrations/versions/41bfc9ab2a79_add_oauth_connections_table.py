"""add oauth connections table

Revision ID: 41bfc9ab2a79
Revises: 1400992b2411
Create Date: 2026-09-17 20:51:01.455194

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "41bfc9ab2a79"
down_revision: Union[str, Sequence[str], None] = "1400992b2411"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create OAuth connections table."""

    op.create_table(
        "oauth_connections",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True,
            nullable=False
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "provider",
            sa.String(length=100),
            nullable=False
        ),

        sa.Column(
            "connection_id",
            sa.String(length=255),
            nullable=False,
            unique=True
        ),

        sa.Column(
            "scopes",
            sa.Text(),
            nullable=False
        ),

        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        )
    )

    op.create_index(
        op.f("ix_oauth_connections_id"),
        "oauth_connections",
        ["id"],
        unique=False
    )

    op.create_index(
        op.f("ix_oauth_connections_user_id"),
        "oauth_connections",
        ["user_id"],
        unique=False
    )

    op.create_index(
        op.f("ix_oauth_connections_provider"),
        "oauth_connections",
        ["provider"],
        unique=False
    )

    op.create_index(
        op.f("ix_oauth_connections_connection_id"),
        "oauth_connections",
        ["connection_id"],
        unique=True
    )


def downgrade() -> None:
    """Remove OAuth connections table."""

    op.drop_index(
        op.f("ix_oauth_connections_connection_id"),
        table_name="oauth_connections"
    )

    op.drop_index(
        op.f("ix_oauth_connections_provider"),
        table_name="oauth_connections"
    )

    op.drop_index(
        op.f("ix_oauth_connections_user_id"),
        table_name="oauth_connections"
    )

    op.drop_index(
        op.f("ix_oauth_connections_id"),
        table_name="oauth_connections"
    )

    op.drop_table("oauth_connections")