"""Add project type to project

Revision ID: 3968d770dced
Revises: f708791b9270
Create Date: 2025-02-15 10:30:13.163098

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3968d770dced"
down_revision: Union[str, None] = "f708791b9270"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("projects", schema=None) as batch_op:
        batch_op.add_column(sa.Column("project_type", sa.String(), nullable=False, server_default="node"))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("projects", schema=None) as batch_op:
        batch_op.drop_column("project_type")

    # ### end Alembic commands ###
