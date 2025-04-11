"""Initialisation propre

Revision ID: 675460a91d38
Revises: 
Create Date: 2025-04-10 22:48:16.266687

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '675460a91d38'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ✅ On ne drop pas de tables inexistantes !
    # op.drop_table('conversations')
    # op.drop_table('messages')

    # ✅ Ajout de la colonne pour la photo de profil
    op.add_column('users', sa.Column('profile_picture_url', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'profile_picture_url')

    op.create_table('messages',
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('conversation_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('sender_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('content', sa.TEXT(), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], name='messages_conversation_id_fkey', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id'], name='messages_sender_id_fkey', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name='messages_pkey')
    )

    op.create_table('conversations',
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=True),
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.CheckConstraint(
            "type::text = ANY (ARRAY['private'::character varying, 'group'::character varying]::text[])",
            name='conversations_type_check'
        ),
        sa.PrimaryKeyConstraint('id', name='conversations_pkey')
    )
