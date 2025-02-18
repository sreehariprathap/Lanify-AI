"""Load init data

Revision ID: e9cacf7e9b71
Revises: 5f7392284e04
Create Date: 2025-02-05 19:00:00.805986

"""
import csv
import os.path

import sqlalchemy as sa
from alembic import op
from sqlalchemy.orm import sessionmaker

# revision identifiers, used by Alembic.
revision = 'e9cacf7e9b71'
down_revision = '5f7392284e04'
branch_labels = None
depends_on = None

Session = sessionmaker()


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    csv_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../data/init.csv'))

    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            students = [dict(row) for row in reader]

        for student in students:
            session.execute(sa.text('INSERT INTO students (name, student_number) VALUES (:name, :student_number)'),
                            student)

        session.commit()

    def downgrade():
        pass
