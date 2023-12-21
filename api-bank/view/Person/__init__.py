from apiflask import APIBlueprint
from models.Person import Person
from lib.errors import PersonNotFound, CPFAlreadyExists
from lib.schemas import PersonIn, PersonOut
from lib.functions import check_cpf_exists
from services import db

person_bp = APIBlueprint('person', __name__)


@person_bp.post('/person')
@person_bp.input(PersonIn, location='json')
@person_bp.output(PersonOut, status_code=201)
def create_person(json_data):
  cpf_already_exists = check_cpf_exists(json_data.get('cpf'))

  if cpf_already_exists:
      raise CPFAlreadyExists

  new_person = Person()
  new_person.name = json_data.get('name')
  new_person.cpf = json_data.get('cpf')
  new_person.birthdate = json_data.get('birthdate')
  db.session.add(new_person)
  db.session.commit()

  return new_person


@person_bp.get('/person/<int:person_cpf>')
@person_bp.output(PersonOut, status_code=200)
def get_person(person_cpf: int):
  person = Person.query.filter_by(cpf=person_cpf).first()

  if not person:
      raise PersonNotFound

  return person