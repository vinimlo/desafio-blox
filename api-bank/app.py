from apiflask import APIFlask
from flask_cors import CORS
from models.Person import Person
from flask_migrate import Migrate
from datetime import datetime
from services import db
from view.account import account_bp
from view.person import person_bp
from view.transaction import transaction_bp

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
    app.register_blueprint(account_bp)
    app.register_blueprint(person_bp)
    app.register_blueprint(transaction_bp)

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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
