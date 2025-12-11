"""enable pgvector extension

Revision ID: 0001
Revises:
Create Date: 2025-12-11

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Enable pgvector extension."""
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')


def downgrade() -> None:
    """Disable pgvector extension."""
    op.execute('DROP EXTENSION IF EXISTS vector')
