"""add language to blogs

Revision ID: 20260825_0003
Revises: 20260825_0002
Create Date: 2026-08-25
"""
from alembic import op
import sqlalchemy as sa

revision = "20260825_0003"
down_revision = "20260825_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("blogs", sa.Column("language", sa.String(length=10), nullable=True, server_default="en"))
    op.create_index(op.f("ix_blogs_language"), "blogs", ["language"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_blogs_language"), table_name="blogs")
    op.drop_column("blogs", "language")
