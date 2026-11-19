"""initial empty schema

Revision ID: 40644b905f69
Revises:
Create Date: 2026-11-20 06:51:04.426863

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "40644b905f69"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
