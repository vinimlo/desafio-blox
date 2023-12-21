from apiflask import APIBlueprint
from lib.schemas import AccountIn, AccountOut, LockIn
from models.Account import Account
from models.Person import Person
from datetime import datetime
from lib.errors import PersonNotFound, AccountNotFound
from services import db

account_bp = APIBlueprint('account', __name__)


@account_bp.post('/account')
@account_bp.input(AccountIn)
@account_bp.output(AccountOut, status_code=201)
def create_account(data):

  new_account = Account()
  new_account.balance = 0.00
  new_account.daily_withdrawal_limit = 1000.00
  new_account.is_active = True
  new_account.account_type = data.get('account_type')
  new_account.date_created = datetime.now()
  new_account.person_id = data.get('person_id')
  db.session.add(new_account)

  db.session.commit()

  return new_account


@account_bp.get('/search_account/<int:person_cpf>')
@account_bp.output(AccountOut, status_code=200)
def search_account(person_cpf: int):
  person = Person.query.filter_by(cpf=person_cpf).first()

  if not person:
    raise PersonNotFound

  account = Account.query.filter_by(person_id=person.id).first()

  if not account:
    raise AccountNotFound

  return account


@account_bp.get('/balance/<int:account_id>')
@account_bp.output(AccountOut(partial=True), status_code=200)
def get_balance(account_id):
  account = Account.query.filter_by(id=account_id).first()

  if not account:
    return {}

  return {'balance': account.balance}


@account_bp.get('/account/<int:account_id>')
@account_bp.output(AccountOut, status_code=200)
def get_account(account_id):
  user_account = Account.query.filter_by(id=account_id).first()

  return user_account

@account_bp.patch('/account/<int:account_id>')
@account_bp.input(LockIn)
@account_bp.output(AccountOut, status_code=200)
def lock_account(account_id, data):
    user_account = Account.query.filter_by(id=account_id).first()
    user_account.is_active = data.get('is_active')
    db.session.commit()

    return user_account