"""Changed column name

Revision ID: 236ed811cd03
Revises: 
Create Date: 2024-03-01 23:00:00.933506

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '236ed811cd03'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('comment', sa.Text(), nullable=True))
    op.alter_column('reviews', 'rating',
               existing_type=sa.INTEGER(),
               type_=sa.Float(),
               nullable=False)
    op.drop_column('reviews', 'review')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('review', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('reviews', 'rating',
               existing_type=sa.Float(),
               type_=sa.INTEGER(),
               nullable=True)
    op.drop_column('reviews', 'comment')
    # ### end Alembic commands ###
