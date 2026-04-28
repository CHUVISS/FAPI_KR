"""create products table

Revision ID: f81d1a7460f8
Revises: 9feb4a2bd0b0
Create Date: 2026-04-28 19:22:24.609606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f81d1a7460f8'
down_revision: Union[str, Sequence[str], None] = '9feb4a2bd0b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
