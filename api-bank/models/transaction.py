from services import db


class Transaction(db.Model):
    __tablename__ = "transaction"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    account_relation = db.relationship(
        "Account", backref="Transaction", foreign_keys=account_id
    )

    def __repr__(self) -> str:
        return f"{self.amount}"

    def __str__(self) -> str:
        return f"{self.amount}"
