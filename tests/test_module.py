import json

from module.debts import Debts
from module.payment_plans import PaymentPlans
from module.payments import Payments


def test_table_load():
    modules = [Debts, PaymentPlans, Payments]
    tables = []
    for i, module in enumerate(modules):
        tables.append(module.build_from_api())
    for table in tables:
        assert len(table) > 0


def test_debt_table_enrich():
    debts = Debts.build_from_api()
    num_has_payment_plan = 0
    num_remaining_amount = 0
    num_next_payment_due_date = 0
    for row in debts:
        if row.has_payment_plan:
            num_has_payment_plan+=1
        if row.remaining_amount:
            num_remaining_amount+=1
        if row.next_payment_due_date:
            num_next_payment_due_date+=1
    assert num_has_payment_plan > 0 and num_remaining_amount > 0 and num_next_payment_due_date > 0


def test_json_output():
    debts = Debts.build_from_api().to_json()
    for row in debts:
        assert json.loads(row)


