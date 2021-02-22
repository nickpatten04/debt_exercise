import json
from dataclasses import dataclass, asdict
import datetime
from typing import List
import requests as r

from module.constants import DEBTS_URL
from module.payment_plans import PaymentPlans, PaymentSchedule
from module.table import Table, TableRow


@dataclass
class Debt(TableRow):
    id: int
    amount: float
    has_payment_plan: bool = None
    remaining_amount: float = None
    next_payment_due_date: datetime.datetime = None

    def set_has_payment_plan(self):
        self.has_payment_plan = True if self.id in [plan.debt_id for plan in PaymentPlans.build_from_api()] else False
        return self

    def set_remaining_amount(self):
        self.remaining_amount = sum(
            [
                plan.amount_to_pay
                for plan in PaymentPlans.build_from_api()
                if plan.debt_id == self.id
            ]
        )
        return self

    def set_next_payment_date(self):
        if self.remaining_amount or self.next_payment_due_date:
            start_date, freq = [
                (plan.start_date, plan.installment_frequency)
                for plan in PaymentPlans.build_from_api()
                if plan.debt_id == self.id
            ][0]
            freq_in_days = datetime.timedelta(days=PaymentSchedule.get_value(freq))
            offset_in_days = datetime.timedelta(
                days=(datetime.datetime.now() - start_date).days % PaymentSchedule.get_value(freq)
            )
            self.next_payment_due_date = datetime.datetime.now() - offset_in_days + freq_in_days
        return self

    def enrich(self):
        self.set_has_payment_plan().set_remaining_amount().set_next_payment_date()
        return self


class Debts(Table):
    def __init__(self, rows: List[Debt]):
        super().__init__(rows)

    @classmethod
    def build_from_api(cls):
        debts = json.loads(r.get(DEBTS_URL).text)
        debts = [Debt(**row).enrich() for row in debts]
        return cls(debts)

    @staticmethod
    def _default(o):
        if isinstance(o, (datetime.date, datetime.datetime)):
            return o.isoformat()

    def to_json(self):
        data = [json.dumps(asdict(row), default=self._default) for row in self]
        return data
