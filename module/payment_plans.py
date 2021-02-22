import json
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

import requests as r

from module.constants import PAYMENT_PLAN_URL
from module.table import Table, TableRow
from module.utility import try_cast_to_datetime


class PaymentSchedule(Enum):
    DAILY = 1
    WEEKLY = 7
    BI_WEEKLY = 14
    MONTHLY = 30
    BI_MONTHLY = 60
    QUARTERLY = 90
    SEMI_ANNUALLY = 180
    ANNUALLY = 365

    @classmethod
    def get_value(cls, frequency):
        if frequency == "DAILY":
            return PaymentSchedule.DAILY.value
        elif frequency == "WEEKLY":
            return PaymentSchedule.WEEKLY.value
        elif frequency == "BI_WEEKLY":
            return PaymentSchedule.BI_WEEKLY.value
        elif frequency == "MONTHLY":
            return PaymentSchedule.MONTHLY.value
        elif frequency == "BI_MONTHLY":
            return PaymentSchedule.BI_MONTHLY.value
        elif frequency == "QUARTERLY":
            return PaymentSchedule.QUARTERLY.value
        elif frequency == "SEMI_ANNUALLY":
            return PaymentSchedule.SEMI_ANNUALLY.value
        elif frequency == "ANNUALLY":
            return PaymentSchedule.ANNUALLY.value
        else:
            raise NotImplementedError


@dataclass
class PaymentPlan(TableRow):
    amount_to_pay: float
    debt_id: int
    id: int
    installment_amount: float
    installment_frequency: str
    start_date: datetime


class PaymentPlans(Table):
    def __init__(self, rows: List[PaymentPlan]):
        super().__init__(rows)

    @classmethod
    def build_from_api(cls):
        payment_plan = json.loads(r.get(PAYMENT_PLAN_URL).text)
        new_data = []
        for dictionary in payment_plan:
            new_data.append({key: try_cast_to_datetime(value) for key, value in dictionary.items()})
        payment_plans = [PaymentPlan(**data) for data in new_data]
        return payment_plans
