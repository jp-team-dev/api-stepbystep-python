"""add guided learning models

Revision ID: 0002_add_guided_models
Revises: 0001_create_card_table
Create Date: 2026-02-25 00:00:00.000000
"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0002_add_guided_models'
down_revision = '0001_create_card_table'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'module',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('sensory_focus', sa.String(length=255), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'lesson',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('module_id', sa.Integer(), sa.ForeignKey('module.id'), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('level', sa.String(length=50), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.add_column('card', sa.Column('lesson_id', sa.Integer(), sa.ForeignKey('lesson.id'), nullable=True))
    op.add_column('card', sa.Column('sensory_cue', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('card', 'sensory_cue')
    op.drop_column('card', 'lesson_id')
    op.drop_table('lesson')
    op.drop_table('module')
