"""criar trigger alerta

Revision ID: dc0af31597a2
Revises: 004915e81992
Create Date: 2025-04-21 15:04:36.486318

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc0af31597a2'
down_revision: Union[str, None] = '004915e81992'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op


def upgrade():
    op.execute("""
        CREATE OR REPLACE FUNCTION check_alert_trigger()
        RETURNS TRIGGER AS $$
        DECLARE
            alert_row RECORD;
            measure_value FLOAT;
        BEGIN
            measure_value := NEW.value::FLOAT;

            FOR alert_row IN
                SELECT ta.id, ta.value, ta.math_signal
                FROM type_alerts ta
                WHERE ta.parameter_id = NEW.parameter_id AND ta.is_active
            LOOP
                IF (
                    (alert_row.math_signal = '>' AND measure_value > alert_row.value) OR
                    (alert_row.math_signal = '<' AND measure_value < alert_row.value) OR
                    (alert_row.math_signal = '=' AND measure_value = alert_row.value)
                ) THEN
                    INSERT INTO alerts (measure_id, type_alert_id, create_date, is_read)
                    VALUES (NEW.id, alert_row.id, EXTRACT(EPOCH FROM NOW())::INT, FALSE);
                END IF;
            END LOOP;

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    op.execute("""
        DROP TRIGGER IF EXISTS trg_check_alert ON measures;
    """)

    op.execute("""
        CREATE TRIGGER trg_check_alert
        AFTER INSERT ON measures
        FOR EACH ROW
        EXECUTE FUNCTION check_alert_trigger();
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS trg_check_alert ON measures;")
    op.execute("DROP FUNCTION IF EXISTS check_alert_trigger;")

