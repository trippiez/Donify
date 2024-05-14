from datetime import datetime
from typing import List

from app.models.base import BaseModel


def investing(
    target: BaseModel,
    entities: List[BaseModel]
):
    result = []
    for obj in entities:
        amount = calculate_allocation(target, entities)
        result.append(amount)
        allocate_investments(target, obj, amount)
        if target.fully_invested:
            break
    return result


def calculate_allocation(target, entity):
    return min(target.full_amount - target.invested_amount,
               entity.full_amount - entity.invested_amount)


def allocate_investments(target, entity, amount):
    for obj in [target, entity]:
        obj.invested_amount += amount
        obj.fully_invested = (
            amount == obj.full_amount
        )
        if obj.fully_invested:
            obj.close_date = datetime.now()