"""rename user_id to author_id is users

Revision ID: 3d5ef5a90213
Revises: e4365111e783
Create Date: 2026-11-03 14:11:51.656304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d5ef5a90213'
down_revision: Union[str, Sequence[str], None] = 'e4365111e783'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Удаляем старый внешний ключ и индекс
    op.drop_constraint('posts_user_id_fkey', 'posts', type_='foreignkey')
    op.drop_index('ix_posts_user_id', table_name='posts')
    
    # 2. Безопасно переименовываем колонку (сохраняя данные)
    op.alter_column('posts', 'user_id', new_column_name='author_id')
    
    # 3. Создаем новые индекс и внешний ключ под новое имя
    op.create_index('ix_posts_author_id', 'posts', ['author_id'], unique=False)
    op.create_foreign_key('posts_author_id_fkey', 'posts', 'users', ['author_id'], ['id'], ondelete='CASCADE')

def downgrade() -> None:
    op.drop_constraint('posts_author_id_fkey', 'posts', type_='foreignkey')
    op.drop_index('ix_posts_author_id', table_name='posts')
    op.alter_column('posts', 'author_id', new_column_name='user_id')
    op.create_index('ix_posts_user_id', 'posts', ['user_id'], unique=False)
    op.create_foreign_key('posts_user_id_fkey', 'posts', 'users', ['user_id'], ['id'], ondelete='CASCADE')
