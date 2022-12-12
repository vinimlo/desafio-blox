from apiflask import (APIFlask, Schema, fields, validators,
                      PaginationSchema, pagination_builder, abort, HTTPError)
from flask_cors import CORS
from models import Person, Account, Transaction
from flask_migrate import Migrate, upgrade, downgrade
from datetime import datetime
from services import db


class CPFAlreadyExists(HTTPError):
    status_code = 403
    message = 'CPF already exists.'


class PersonNotFound(HTTPError):
    status_code = 200
    message = 'Person does not exist.'


class AccountNotFound(HTTPError):
    status_code = 200
    message = 'Account does not exist.'


class TransactionQuery(Schema):
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(
        load_default=10, validate=validators.Range(max=30))
    account_id = fields.Integer()


class TransactionIn(Schema):
    amount = fields.Float()
    account_id = fields.Integer()


class AccountIn(Schema):
    person_id = fields.Integer()
    account_type = fields.Integer()


class LockIn(Schema):
    is_active = fields.Boolean()


class PersonIn(Schema):
    name = fields.String()
    cpf = fields.String()
    birthdate = fields.DateTime()


class PersonOut(Schema):
    id = fields.Integer()
    name = fields.String()
    cpf = fields.String()
    birthdate = fields.DateTime()


class AccountOut(Schema):
    id = fields.Integer()
    balance = fields.Float()
    daily_withdrawal_limit = fields.Float()
    is_active = fields.Boolean()
    account_type = fields.Integer()
    date_created = fields.DateTime()
    person_id = fields.Integer()
    person_relation = fields.Nested(PersonOut)


class TransactionOut(Schema):
    id = fields.Integer()
    amount = fields.Float()
    date_created = fields.DateTime()
    account_id = fields.Integer()


class TransactionsOut(Schema):
    transactions = fields.List(fields.Nested(TransactionOut))
    pagination = fields.Nested(PaginationSchema)


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


def create_app():
    app = APIFlask(__name__, title='Desafio Bloxs')
    app.config.from_pyfile('config.py')

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        '{driver}://{user}:{password}@{host}:{port}/{database}'.format(
            driver=app.config['DB_DRIVER'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            host=app.config['DB_HOST'],
            port=app.config['DB_PORT'],
            database=app.config['DB_NAME']
    )

    migrate = Migrate(app, db)
    cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

    with app.app_context():
        db.init_app(app)
        db.create_all()

    @app.cli.command("seed-db")
    def seed_db():
        for num in range(1, 6):
            new_person = Person()
            new_person.name = f'User {num}'
            new_person.cpf = f'1234567891{num}'
            new_person.birthdate = datetime.fromisoformat(
                f'2000-02-0{num}T05:55:00'
            )
            db.session.add(new_person)
            db.session.flush()
        db.session.commit()

    @app.post('/person')
    @app.input(PersonIn)
    @app.output(PersonOut, status_code=201)
    def create_person(data):
        cpf_already_exists = check_cpf_exists(data.get('cpf'))

        if cpf_already_exists:
            raise CPFAlreadyExists

        new_person = Person()
        new_person.name = data.get('name')
        new_person.cpf = data.get('cpf')
        new_person.birthdate = data.get('birthdate')
        db.session.add(new_person)
        db.session.commit()

        return new_person

    @app.post('/account')
    @app.input(AccountIn)
    @app.output(AccountOut, status_code=201)
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

    @app.get('/search_account/<int:person_cpf>')
    @app.output(AccountOut, status_code=200)
    def search_account(person_cpf: int):
        person = Person.query.filter_by(cpf=person_cpf).first()
        if not person:
            raise PersonNotFound

        account = Account.query.filter_by(person_id=person.id).first()

        if not account:
            raise AccountNotFound

        return account

    @app.get('/person/<int:person_cpf>')
    @app.output(PersonOut, status_code=200)
    def get_person(person_cpf: int):
        person = Person.query.filter_by(cpf=person_cpf).first()

        if not person:
            raise PersonNotFound

        return person

    @app.get('/balance/<int:account_id>')
    @app.output(AccountOut(partial=True), status_code=200)
    def get_balance(account_id):
        account = Account.query.filter_by(id=account_id).first()

        return {'balance': account.balance}

    @app.post('/deposit')
    @app.input(TransactionIn)
    @app.output(AccountOut(partial=True), status_code=201)
    def create_deposit(data):
        user_account = Account.query.filter_by(
            id=data.get('account_id')).first()

        if not user_account.is_active:
            abort(403, 'Account locked.')

        amount_to_deposit = abs(data.get('amount'))

        if(amount_to_deposit == 0):
            abort(403, 'Invalid amount')

        new_transaction = Transaction()
        new_transaction.amount = amount_to_deposit
        new_transaction.account_id = data.get('account_id')
        new_transaction.date_created = datetime.now()
        db.session.add(new_transaction)
        db.session.commit()

        user_account = Account.query.filter_by(
            id=data.get('account_id')).first()
        user_account.balance += amount_to_deposit

        db.session.commit()

        return {'balance': user_account.balance}

    @app.post('/withdrawal')
    @app.input(TransactionIn)
    @app.output(AccountOut(partial=True), status_code=201)
    def create_withdrawal(data):
        amount_to_withdrawal = round(abs(data.get('amount')), 2)
        user_account = Account.query.filter_by(
            id=data.get('account_id')).first()

        if not user_account.is_active:
            abort(403, 'Account locked.')

        account_has_limit = check_limit(
            user_account, amount_to_withdrawal)

        if not account_has_limit:
            abort(403, 'Daily limit exceeded!')

        if user_account.balance - amount_to_withdrawal < 0:
            abort(403, 'Not enough funds1!')

        if(amount_to_withdrawal == 0):
            abort(403, 'Invalid amount')

        new_transaction = Transaction()
        new_transaction.amount = -amount_to_withdrawal
        new_transaction.account_id = data.get('account_id')
        new_transaction.date_created = datetime.now()
        db.session.add(new_transaction)
        db.session.commit()

        user_account.balance -= amount_to_withdrawal
        db.session.commit()

        return {'balance': user_account.balance}

    @app.patch('/account/<int:account_id>')
    @app.input(LockIn)
    @app.output(AccountOut, status_code=200)
    def lock_account(account_id, data):
        user_account = Account.query.filter_by(id=account_id).first()
        user_account.is_active = data.get('is_active')
        db.session.commit()

        return user_account

    @app.get('/account/<int:account_id>')
    @app.output(AccountOut, status_code=200)
    def get_account(account_id):
        user_account = Account.query.filter_by(id=account_id).first()

        return user_account

    @app.get('/transactions')
    @app.get('/transactions/<int:account_id>')
    @app.input(TransactionQuery, location='query')
    @app.output(TransactionsOut, status_code=200)
    def get_transactions(account_id, query):
        pagination = Transaction.query.filter_by(account_id=account_id) \
            .paginate(
                page=query.get('page'),
                per_page=query.get('per_page')
        )
        transactions = pagination.items

        return {
            'transactions': transactions,
            'pagination': pagination_builder(pagination)
        }

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
