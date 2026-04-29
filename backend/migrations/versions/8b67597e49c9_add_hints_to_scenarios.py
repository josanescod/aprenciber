"""add hints to scenarios

Revision ID: 8b67597e49c9
Revises: f22a58ed7805
Create Date: 2026-04-29 14:36:16.447586

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "8b67597e49c9"
down_revision: Union[str, Sequence[str], None] = "f22a58ed7805"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "scenarios",
        sa.Column(
            "hints",
            sa.JSON(),
            nullable=False,
            server_default="[]",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("scenarios", "hints")
