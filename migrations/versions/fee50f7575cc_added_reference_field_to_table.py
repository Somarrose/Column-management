"""added reference field to table

Revision ID: fee50f7575cc
Revises: c74b814f5b49
Create Date: 2024-04-22 12:22:49.474982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fee50f7575cc'
down_revision = 'c74b814f5b49'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('column_info', schema=None) as batch_op:
        batch_op.add_column(sa.Column('reference', sa.String(length=100), nullable=False))
        batch_op.create_unique_constraint(batch_op.f('uq_column_info_reference'), ['reference'])

    with op.batch_alter_table('usage_entry', schema=None) as batch_op:
        batch_op.alter_column('column_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('usage_entry', schema=None) as batch_op:
        batch_op.alter_column('column_id',
               existing_type=sa.String(length=100),
               type_=sa.INTEGER(),
               existing_nullable=False)

    with op.batch_alter_table('column_info', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_column_info_reference'), type_='unique')
        batch_op.drop_column('reference')

    # ### end Alembic commands ###
