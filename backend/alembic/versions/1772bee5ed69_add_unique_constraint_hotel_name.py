"""add_unique_constraint_hotel_name

Revision ID: 1772bee5ed69
Revises: d01133749479
Create Date: 2026-01-17 10:24:21.744564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1772bee5ed69'
down_revision: Union[str, Sequence[str], None] = 'd01133749479'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_index(op.f('ix_hotels_name'), table_name='hotels')
    op.create_index(op.f('ix_hotels_name'), 'hotels', ['name'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_hotels_name'), table_name='hotels')
    op.create_index(op.f('ix_hotels_name'), 'hotels', ['name'], unique=False)

