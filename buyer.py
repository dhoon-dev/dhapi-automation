#!/usr/bin/env python3

from typing import Dict, List

import typer

from dhapi.domain.user import User
from dhapi.domain.lotto645_ticket import Lotto645Ticket
from dhapi.port.credentials_provider import CredentialsProvider
from dhapi.port.lottery_client import LotteryClient


class _SimplePrinter:
    def print_result_of_assign_virtual_account(self, 전용가상계좌, 결제신청금액):
        _ = (전용가상계좌, 결제신청금액)
        pass

    def print_result_of_show_balance(self, 총예치금, 구매가능금액, 예약구매금액, 출금신청중금액, 구매불가능금액, 이번달누적구매금액):
        _ = (구매가능금액, 예약구매금액, 출금신청중금액, 구매불가능금액, 이번달누적구매금액)
        print(f"{총예치금}")

    def _num_to_money_str(self, num):
        return f"{num:,}"

    def print_result_of_buy_lotto645(self, slots: List[Dict]):
        """
        :param slots: [{"slot": "A", "mode": "자동", "numbers": [1, 2, 3, 4, 5, 6]}, ...]
        :return:
        """
        for slot in slots:
            print(" ".join(f"{num: >2}" for num in slot["numbers"]))

def build_lottery_client(user_profile: User):
    return LotteryClient(user_profile, _SimplePrinter())

app = typer.Typer(
    help="Simple Lottery Buyer",
    context_settings={"help_option_names": ["-h", "--help"]},
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
    add_completion=False,
)

@app.command(help="Show balance")
def show_balance():
    user = CredentialsProvider("default").get_user()

    client = build_lottery_client(user)
    client.show_balance()

@app.command(help="Buy")
def buy():
    user = CredentialsProvider("default").get_user()

    client = build_lottery_client(user)
    client.buy_lotto645(Lotto645Ticket.create_auto_tickets(count=5))

if __name__ == "__main__":
    try:
        app()
    except Exception as e:
        print(e)
