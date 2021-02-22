import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

import requests as r

from module.constants import PAYMENT_URL
from module.table import Table, TableRow
from module.utility import try_cast_to_datetime


@dataclass
class Payment(TableRow):
    payment_plan_id: int
    amount: float
    date: datetime


class Payments(Table):
    def __init__(self, rows: List[Payment]):
        super().__init__(rows)

    @classmethod
    def build_from_api(cls):
        payment_plan = json.loads(r.get(PAYMENT_URL).text)
        new_data = []
        for dictionary in payment_plan:
            new_data.append({key: try_cast_to_datetime(value) for key, value in dictionary.items()})
        payment_plans = [Payment(**data) for data in new_data]
        return payment_plans
