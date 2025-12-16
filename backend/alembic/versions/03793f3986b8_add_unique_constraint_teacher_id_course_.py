"""Add unique constraint teacher_id course_code

Revision ID: 03793f3986b8
Revises: 558ab25bc840
Create Date: 2025-12-15 22:23:37.566423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '03793f3986b8'
down_revision: Union[str, Sequence[str], None] = '558ab25bc840'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add unique constraint on (teacher_id, course_code)
    op.create_unique_constraint(
        'uq_courses_teacher_course_code',
        'courses',
        ['teacher_id', 'course_code']
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove unique constraint
    op.drop_constraint(
        'uq_courses_teacher_course_code',
        'courses',
        type_='unique'
    )
