from services import db


class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Numeric, nullable=False)
    daily_withdrawal_limit = db.Column(db.Numeric, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    account_type = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    person_relation = db.relationship(
        "Person", backref="Account", foreign_keys=person_id, uselist=False
    )

    def __repr__(self) -> str:
        return f"{self.person_relation.name}"

    def __str__(self) -> str:
        return f"{self.person_relation.name}"
