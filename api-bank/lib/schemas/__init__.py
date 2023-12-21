from apiflask import Schema, fields, validators, PaginationSchema


class PersonIn(Schema):
    name = fields.String()
    cpf = fields.String()
    birthdate = fields.DateTime()


class PersonOut(Schema):
    id = fields.Integer()
    name = fields.String()
    cpf = fields.String()
    birthdate = fields.DateTime()


class AccountIn(Schema):
    person_id = fields.Integer()
    account_type = fields.Integer()


class AccountOut(Schema):
    id = fields.Integer()
    balance = fields.Float()
    daily_withdrawal_limit = fields.Float()
    is_active = fields.Boolean()
    account_type = fields.Integer()
    date_created = fields.DateTime()
    person_id = fields.Integer()
    person_relation = fields.Nested(PersonOut)


class TransactionQuery(Schema):
    page = fields.Integer(load_default=1)
    per_page = fields.Integer(
        load_default=10, validate=validators.Range(max=30))
    account_id = fields.Integer()


class TransactionIn(Schema):
    amount = fields.Float()
    account_id = fields.Integer()


class LockIn(Schema):
    is_active = fields.Boolean()


class TransactionOut(Schema):
    id = fields.Integer()
    amount = fields.Float()
    date_created = fields.DateTime()
    account_id = fields.Integer()


class TransactionsOut(Schema):
    transactions = fields.List(fields.Nested(TransactionOut))
    pagination = fields.Nested(PaginationSchema)
