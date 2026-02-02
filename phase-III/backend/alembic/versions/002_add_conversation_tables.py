"""Add conversation, message, and tool_call tables for AI chatbot

Revision ID: 002_add_conversation_tables
Revises: 001_initial
Create Date: 2026-02-02

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '002_add_conversation_tables'
down_revision: Union[str, None] = None  # Set to previous migration ID if exists
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('idx_conversations_user_id', 'conversations', ['user_id'])
    op.create_index('idx_conversations_updated_at', 'conversations', ['updated_at'])

    # Create messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('conversation_id', sa.UUID(), sa.ForeignKey('conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),  # user, assistant, tool
        sa.Column('content', sa.Text(), nullable=False, server_default=''),
        sa.Column('tool_call_id', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('idx_messages_conversation_id', 'messages', ['conversation_id'])
    op.create_index('idx_messages_created_at', 'messages', ['created_at'])

    # Create tool_calls table
    op.create_table(
        'tool_calls',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('message_id', sa.UUID(), sa.ForeignKey('messages.id', ondelete='CASCADE'), nullable=False),
        sa.Column('tool_name', sa.String(100), nullable=False),
        sa.Column('parameters', postgresql.JSONB(), nullable=False, server_default='{}'),
        sa.Column('result', postgresql.JSONB(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),  # pending, success, error
        sa.Column('duration_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index('idx_tool_calls_message_id', 'tool_calls', ['message_id'])
    op.create_index('idx_tool_calls_tool_name', 'tool_calls', ['tool_name'])


def downgrade() -> None:
    # Drop tables in reverse order due to foreign key constraints
    op.drop_index('idx_tool_calls_tool_name', table_name='tool_calls')
    op.drop_index('idx_tool_calls_message_id', table_name='tool_calls')
    op.drop_table('tool_calls')

    op.drop_index('idx_messages_created_at', table_name='messages')
    op.drop_index('idx_messages_conversation_id', table_name='messages')
    op.drop_table('messages')

    op.drop_index('idx_conversations_updated_at', table_name='conversations')
    op.drop_index('idx_conversations_user_id', table_name='conversations')
    op.drop_table('conversations')
