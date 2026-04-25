"""change lab instance info columns to jsonb

Revision ID: ca4c03fe8e21
Revises: 2d60669d3652
Create Date: 2026-04-25 12:02:21.637254

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "ca4c03fe8e21"
down_revision: Union[str, Sequence[str], None] = "2d60669d3652"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "lab_instances",
        "containers_info",
        existing_type=sa.Text(),
        type_=postgresql.JSONB(astext_type=sa.Text()),
        postgresql_using="containers_info::jsonb",
        existing_nullable=True,
    )

    op.alter_column(
        "lab_instances",
        "networks_info",
        existing_type=sa.Text(),
        type_=postgresql.JSONB(astext_type=sa.Text()),
        postgresql_using="networks_info::jsonb",
        existing_nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "lab_instances",
        "networks_info",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        type_=sa.Text(),
        postgresql_using="networks_info::text",
        existing_nullable=True,
    )

    op.alter_column(
        "lab_instances",
        "containers_info",
        existing_type=postgresql.JSONB(astext_type=sa.Text()),
        type_=sa.Text(),
        postgresql_using="containers_info::text",
        existing_nullable=True,
    )
