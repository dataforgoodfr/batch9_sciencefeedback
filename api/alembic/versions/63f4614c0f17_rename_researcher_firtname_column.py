"""rename_researcher_firtName_column

Revision ID: 63f4614c0f17
Revises: 2201a3f6d9a0
Create Date: 2021-06-25 14:13:42.213838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '63f4614c0f17'
down_revision = '2201a3f6d9a0'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('researcher', 'firtName', new_column_name='firstName')


def downgrade():
    op.alter_column('researcher', 'firstName', new_column_name='firtName')
