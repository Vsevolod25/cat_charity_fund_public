from datetime import datetime
from typing import Tuple, Union

from app.models import CharityProject, Donation


def invest_donations(
    *,
    instance: dict[str, Union[str, int, bool, datetime]],
    funds: list[Union[CharityProject, Donation]],
) -> Tuple[
    dict[str, Union[str, int, bool, datetime]],
    list[Union[CharityProject, Donation]]
]:
    """
    Распределение средств после добавления нового проекта или пожертвования.
    """
    investment = instance['full_amount']
    invested = []
    while (investment > 0) and (funds):
        fund = funds[0]
        remaining = fund.full_amount - fund.invested_amount
        if investment >= remaining:
            investment -= remaining
            fund.invested_amount = fund.full_amount
            fund.fully_invested = True
            fund.close_date = datetime.now()
            invested.append(fund)
            funds.pop(0)
        else:
            fund.invested_amount += investment
            invested.append(fund)
            investment = 0
    instance['invested_amount'] = instance['full_amount'] - investment
    if investment == 0:
        instance['fully_invested'] = True
        instance['close_date'] = datetime.now()
    return instance, invested
