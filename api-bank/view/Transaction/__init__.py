from apiflask import APIBlueprint, abort, pagination_builder
from lib.schemas import AccountOut, TransactionIn, TransactionQuery, TransactionsOut
from lib.functions import check_limit
from models.Account import Account
from models.Transaction import Transaction
from datetime import datetime
from services import db

transaction_bp = APIBlueprint('transaction', __name__)


@transaction_bp.post('/deposit')
@transaction_bp.input(TransactionIn, location='json')
@transaction_bp.output(AccountOut(partial=True), status_code=201)
def create_deposit(json_data):
    user_account = Account.query.filter_by(
        id=json_data.get('account_id')).first()

    if not user_account.is_active:
        abort(403, 'Account locked.')

    amount_to_deposit = abs(json_data.get('amount'))

    if (amount_to_deposit == 0):
        abort(403, 'Invalid amount')

    new_transaction = Transaction()
    new_transaction.amount = amount_to_deposit
    new_transaction.account_id = json_data.get('account_id')
    new_transaction.date_created = datetime.now()
    db.session.add(new_transaction)
    db.session.commit()

    user_account = Account.query.filter_by(
        id=json_data.get('account_id')).first()
    user_account.balance += amount_to_deposit

    db.session.commit()

    return {'balance': user_account.balance}


@transaction_bp.post('/withdrawal')
@transaction_bp.input(TransactionIn, location='json')
@transaction_bp.output(AccountOut(partial=True), status_code=201)
def create_withdrawal(json_data):
    account_id = json_data.get('account_id')

    amount_to_withdrawal = round(abs(json_data.get('amount')), 2)
    user_account = Account.query.filter_by(
        id=account_id).first()

    if not user_account.is_active:
        abort(403, 'Account locked.')

    account_has_limit = check_limit(
        user_account, amount_to_withdrawal)

    if not account_has_limit:
        abort(403, 'Daily limit exceeded!')

    if user_account.balance - amount_to_withdrawal < 0:
        abort(403, 'Not enough funds1!')

    if (amount_to_withdrawal == 0):
        abort(403, 'Invalid amount')

    new_transaction = Transaction()
    new_transaction.amount = -amount_to_withdrawal
    new_transaction.account_id = account_id
    new_transaction.date_created = datetime.now()
    db.session.add(new_transaction)
    db.session.commit()

    user_account.balance -= amount_to_withdrawal
    db.session.commit()

    return {'balance': user_account.balance}


@transaction_bp.get('/transactions')
@transaction_bp.get('/transactions/<int:account_id>')
@transaction_bp.input(TransactionQuery, location='query')
@transaction_bp.output(TransactionsOut, status_code=200)
def get_transactions(account_id, query_data):

    pagination = Transaction.query.filter_by(account_id=account_id) \
        .paginate(
            page=query_data.get('page'),
            per_page=query_data.get('per_page')
    )
    transactions = pagination.items

    return {
        'transactions': transactions,
        'pagination': pagination_builder(pagination)
    }
