"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-05-08
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "patient_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("nurse_id", sa.String(), nullable=False),
        sa.Column("patient_ref", sa.String(), nullable=True),
        sa.Column("status", sa.Enum("active", "closed", name="sessionstatus"), nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("raw_transcript", sa.Text(), nullable=True),
    )

    op.create_table(
        "soap_notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("session_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("patient_sessions.id"), nullable=False),
        sa.Column("subjective", sa.Text(), nullable=True),
        sa.Column("objective", sa.Text(), nullable=True),
        sa.Column("assessment", sa.Text(), nullable=True),
        sa.Column("plan", sa.Text(), nullable=True),
        sa.Column("generated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("reviewed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("submitted", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("nurse_edits", sa.Text(), nullable=True),
    )


def downgrade():
    op.drop_table("soap_notes")
    op.drop_table("patient_sessions")
    op.execute("DROP TYPE IF EXISTS sessionstatus")
