"""module sensory focus array

Revision ID: 0003_module_sensory_array
Revises: 0002_add_guided_models
Create Date: 2026-02-25 00:00:01.000000
"""
import sqlalchemy as sa
from alembic import op

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0003_module_sensory_array'
down_revision = '0002_add_guided_models'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'module',
        sa.Column(
            'sensory_focus_array',
            postgresql.ARRAY(sa.String(length=255)),
            nullable=False,
            server_default=sa.text("ARRAY[]::varchar[]"),
        ),
    )
    op.execute(
        """
        UPDATE module
        SET sensory_focus_array =
            CASE
                WHEN sensory_focus IS NULL THEN ARRAY[]::varchar[]
                ELSE ARRAY[sensory_focus]::varchar[]
            END
        """
    )
    op.drop_column('module', 'sensory_focus')
    op.alter_column(
        'module',
        'sensory_focus_array',
        new_column_name='sensory_focus',
        existing_type=postgresql.ARRAY(sa.String(length=255)),
    )


def downgrade():
    op.add_column(
        'module',
        sa.Column('sensory_focus_text', sa.String(length=255), nullable=True),
    )
    op.execute(
        """
        UPDATE module
        SET sensory_focus_text =
            CASE
                WHEN array_length(sensory_focus, 1) > 0 THEN sensory_focus[1]
                ELSE NULL
            END
        """
    )
    op.drop_column('module', 'sensory_focus')
    op.alter_column(
        'module',
        'sensory_focus_text',
        new_column_name='sensory_focus',
        existing_type=sa.String(length=255),
    )
