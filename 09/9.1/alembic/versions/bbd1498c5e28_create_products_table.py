"""create products table

Revision ID: bbd1498c5e28
Revises: f81d1a7460f8
Create Date: 2026-04-28 19:23:02.621709

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbd1498c5e28'
down_revision: Union[str, Sequence[str], None] = 'f81d1a7460f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
