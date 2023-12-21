from models.Account import Account
from models.Transaction import Transaction
from models.Person import Person
from datetime import datetime

def check_limit(user_account: Account, amount: float) -> bool:
    current_dt = datetime.now()
    current_day = current_dt.date()

    transaction_list = Transaction.query \
        .filter_by(account_id=user_account.id) \
        .filter(Transaction.date_created >= f'{current_day} 00:00:00') \
        .filter(Transaction.amount < 0) \
        .all()
    withdrawal_list = [float(transaction.amount)
                       for transaction in transaction_list]
    withdrawal_sum = sum(withdrawal_list) * -1
    withdrawal_total = withdrawal_sum + float(amount)

    user_has_limit = withdrawal_total <= user_account.daily_withdrawal_limit

    return user_has_limit


def check_cpf_exists(cpf: str) -> bool:
    person = Person.query.filter_by(cpf=cpf).first()
    person_exists = person is not None
    return person_exists