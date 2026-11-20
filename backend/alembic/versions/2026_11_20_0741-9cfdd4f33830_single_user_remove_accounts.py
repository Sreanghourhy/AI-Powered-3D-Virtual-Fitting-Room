"""single user remove accounts

Revision ID: 9cfdd4f33830
Revises: a6c9f7f0b941
Create Date: 2026-11-20 07:41:35.977881

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9cfdd4f33830"
down_revision: str | Sequence[str] | None = "a6c9f7f0b941"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Remove accounts, sessions and consents (CR-02: single-user prototype).

    Order matters: drop the foreign-key columns first, so dropping `users` can't
    cascade-delete jobs or audit rows.
    """
    with op.batch_alter_table("audit_log", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_audit_log_user_id"))
        batch_op.drop_constraint(batch_op.f("fk_audit_log_user_id_users"), type_="foreignkey")
        batch_op.drop_column("user_id")

    with op.batch_alter_table("jobs", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_jobs_user_id"))
        batch_op.drop_constraint(batch_op.f("fk_jobs_user_id_users"), type_="foreignkey")
        batch_op.drop_column("user_id")

    with op.batch_alter_table("sessions", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_sessions_token_hash"))
        batch_op.drop_index(batch_op.f("ix_sessions_user_id"))
    op.drop_table("sessions")

    with op.batch_alter_table("consents", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_consents_user_id"))
    op.drop_table("consents")

    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_users_email"))
    op.drop_table("users")


def downgrade() -> None:
    """Recreate the old tables/columns. Does NOT restore deleted accounts; only works when
    `jobs` is empty (the old `jobs.user_id` was NOT NULL)."""
    op.create_table(
        "users",
        sa.Column("email", sa.VARCHAR(length=320), nullable=False),
        sa.Column("password_hash", sa.VARCHAR(length=255), nullable=False),
        sa.Column("created_at", sa.DATETIME(), nullable=False),
        sa.Column("deleted_at", sa.DATETIME(), nullable=True),
        sa.Column("id", sa.CHAR(length=32), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
    )
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_users_email"), ["email"], unique=1)

    op.create_table(
        "consents",
        sa.Column("user_id", sa.CHAR(length=32), nullable=False),
        sa.Column("version", sa.VARCHAR(length=32), nullable=False),
        sa.Column("scope", sa.VARCHAR(length=64), nullable=False),
        sa.Column("granted_at", sa.DATETIME(), nullable=False),
        sa.Column("withdrawn_at", sa.DATETIME(), nullable=True),
        sa.Column("id", sa.CHAR(length=32), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_consents_user_id_users"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_consents")),
    )
    with op.batch_alter_table("consents", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_consents_user_id"), ["user_id"], unique=False)

    op.create_table(
        "sessions",
        sa.Column("user_id", sa.CHAR(length=32), nullable=False),
        sa.Column("token_hash", sa.VARCHAR(length=64), nullable=False),
        sa.Column("created_at", sa.DATETIME(), nullable=False),
        sa.Column("expires_at", sa.DATETIME(), nullable=False),
        sa.Column("id", sa.CHAR(length=32), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_sessions_user_id_users"), ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sessions")),
    )
    with op.batch_alter_table("sessions", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_sessions_user_id"), ["user_id"], unique=False)
        batch_op.create_index(batch_op.f("ix_sessions_token_hash"), ["token_hash"], unique=1)

    with op.batch_alter_table("jobs", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.CHAR(length=32), nullable=False))
        batch_op.create_foreign_key(
            batch_op.f("fk_jobs_user_id_users"), "users", ["user_id"], ["id"], ondelete="CASCADE"
        )
        batch_op.create_index(batch_op.f("ix_jobs_user_id"), ["user_id"], unique=False)

    with op.batch_alter_table("audit_log", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.CHAR(length=32), nullable=True))
        batch_op.create_foreign_key(
            batch_op.f("fk_audit_log_user_id_users"),
            "users",
            ["user_id"],
            ["id"],
            ondelete="SET NULL",
        )
        batch_op.create_index(batch_op.f("ix_audit_log_user_id"), ["user_id"], unique=False)

    # ### end Alembic commands ###
