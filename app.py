from flask import Flask, request
from flask import make_response
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_restful import reqparse
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import argon2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:10082009@localhost:3307/budgetdb'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
status_code: int = 200
auth = HTTPBasicAuth()


@app.route('/api/v1/hello-world-11')
def index():
    return make_response(f"Hello World 11", status_code)


@app.route('/user/login', methods=['POST'])
@auth.login_required(role='user')
def login():
    return {"message": "you login successful"}, 200


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)

    def add_to(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def user_list(cls):
        def to_json(user):
            return {
                'id': user.id,
                'username': user.username,
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'password': user.password,
                'phone': user.phone
            }

        return {'users': [to_json(user) for user in User.query.all()]}

    @staticmethod
    def generate_hash(password):
        return argon2.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        return argon2.verify(password, hash_)


@auth.verify_password
def verify_password(username, password):
    user = User.find_by_username(username)

    if user and User.verify_hash(password, user.password):
        return username


@auth.get_user_roles
def get_user_roles(user):
    user_entity = User.find_by_username(user)
    return user_entity.role


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    cv = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    available_balance = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def add_to(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()


class Budget(db.Model):
    title = db.Column(db.String(255), nullable=False)
    record_id = db.Column(db.Integer, primary_key=True)
    name_user = db.Column(db.String(120), unique=True, nullable=False)
    income = db.Column(db.Integer, nullable=False)
    outcome = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    available_balance = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def add_to(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_record_id(cls, record_id):
        return cls.query.filter_by(record_id=record_id).first()


@app.route('/user/register', methods=['POST'])
def user():
    pars = reqparse.RequestParser()
    pars.add_argument('id', help='id cannot be blank', required=True)
    pars.add_argument('username', help='name cannot be blank', required=True)
    pars.add_argument('firstName', help='name cannot be blank', required=True)
    pars.add_argument('lastName', help='status cannot be blank', required=True)
    pars.add_argument('email', help='status cannot be blank', required=True)
    pars.add_argument('password', help='userId cannot be blank', required=True)

    data = pars.parse_args()
    try:
        id = int(data['id'])
        username = (data['username'])
        firstName = (data['firstName'])
        lastName = data['lastName']
        email = data['email']
        password = (data['password'])

    except Exception:
        return {'message': 'error'}, 500

    user_1 = User(
        id=id,
        username=username,
        firstName=firstName,
        lastName=lastName,
        email=email,
        password=argon2.hash(password),
        role="user"
    )

    try:
        user_1.add_to()
        return {"message": "everything is good"}, 200
    except Exception:
        return {"message": "error"}, 500


@app.route('/user/<string:username>', methods=['GET'])
@auth.login_required(role=['user', 'admin'])
def getUserByName(username):
    try:
        user_1 = User.find_by_username(username=username)

        return {
                   "id": user_1.id,
                   "username": user_1.username,
                   "firstName": user_1.firstName,
                   "lastName": user_1.lastName,
                   "email": user_1.email,
                   "password": user_1.password,
               }, 200
    except Exception:
        return {'message': 'Error'}, 500


@app.route('/user/<string:username>', methods=['PUT', 'DELETE', 'GET'])
@auth.login_required(role='admin')
def user_by_nick(username):
    if request.method == 'PUT':
        pars = reqparse.RequestParser()
        pars.add_argument('id', help='id cannot be blank', required=True)
        pars.add_argument('username', help='name cannot be blank', required=True)
        pars.add_argument('firstName', help='name cannot be blank', required=True)
        pars.add_argument('lastName', help='status cannot be blank', required=True)
        pars.add_argument('email', help='status cannot be blank', required=True)
        pars.add_argument('password', help='userId cannot be blank', required=True)

        data = pars.parse_args()
        try:
            User.query.filter_by(username=username).update(data)
            db.session.commit()
            return {"message": f"item with {username} is up to date"}
        except Exception:
            return {"message": "Something went wrong"}, 500
        pass

    # elif request.method == 'GET':


    # pass

    elif request.method == 'DELETE':
        if User.query.filter_by(username=username).first() == None:
            return {"message": "Something went wrong"}, 404

        try:
            User.query.filter_by(username=username).delete()
            db.session.commit()
            return {"message": f"user with {username} was deleted"}, 200
        except Exception:
            return {"message": "Something went wrong"}, 500


@app.route('/budget', methods=["POST"])
@auth.login_required(role=['user', 'admin'])
def budget():
    pars = reqparse.RequestParser()
    pars.add_argument('title', help='title cannot be blank', required=True)
    pars.add_argument('record_id', help='record_id cannot be blank', required=True)
    pars.add_argument('name_user', help='name cannot be blank', required=True)
    pars.add_argument('income', help='income cannot be blank', required=True)
    pars.add_argument('outcome', help='outcome cannot be blank', required=True)
    pars.add_argument('date', help='date cannot be blank', required=True)
    pars.add_argument('password', help='password cannot be blank', required=True)
    pars.add_argument('available_balance', help='balance cannot be blank', required=True)
    pars.add_argument('userId', help='userId cannot be blank', required=True)

    data = pars.parse_args()
    try:
        title = (data['title'])
        record_id = int(data['record_id'])
        name_user = (data['name_user'])
        income = int(data['income'])
        outcome = int(data['outcome'])
        date = (data['date'])
        password = (data['password'])
        available_balanse = int(data['available_balance'])
        userId = int(data['userId'])

    except Exception:
        return {'message': 'error'}, 500

    budget_1 = Budget(
        title=title,
        record_id=record_id,
        name_user=name_user,
        income=income,
        outcome=outcome,
        date=date,
        password=password,
        available_balance=available_balanse,
        userId=userId
    )

    try:
        budget_1.add_to()
        return {"message": "everything is good"}, 200
    except Exception:
        return {"message": "error2"}, 500


@app.route('/budget/<int:record_id>', methods=["PUT", "DELETE", "GET"])
@auth.login_required(role=['user', 'admin'])
def budget_by_id(record_id):
    if request.method == "PUT":
        pars = reqparse.RequestParser()
        pars.add_argument('title', help='title cannot be blank', required=True)
        pars.add_argument('record_id', help='record_id cannot be blank', required=True)
        pars.add_argument('name_user', help='name cannot be blank', required=True)
        pars.add_argument('income', help='income cannot be blank', required=True)
        pars.add_argument('outcome', help='outcome cannot be blank', required=True)
        pars.add_argument('date', help='date cannot be blank', required=True)
        pars.add_argument('password', help='password cannot be blank', required=True)
        pars.add_argument('available_balance', help='balance cannot be blank', required=True)
        pars.add_argument('userId', help='userId cannot be blank', required=True)

        data = pars.parse_args()
        try:
            Budget.query.filter_by(record_id=record_id).update(data)
            db.session.commit()
            return {"message": f"item with {record_id} is up to date"}
        except Exception:
            return {"message": "Something went wrong"}, 500
        pass

    elif request.method == "GET":
        try:
            budget_1 = Budget.find_by_record_id(record_id=record_id)
            return {

                       "title": budget_1.title,
                       "record_id": budget_1.record_id,
                       "name_user": budget_1.name_user,
                       "income": budget_1.income,
                       "outcome": budget_1.outcome,
                       "date": budget_1.date,
                       "password": budget_1.password,
                       "available_balance": budget_1.available_balance,
                       "userId": budget_1.userId

                   }, 200
        except Exception:
            return {'message': 'Error'}, 500

    elif request.method == "DELETE":
        if Budget.query.filter_by(record_id=record_id).first() == None:
            return {"message": "Something went wrong"}, 404

        try:
            Budget.query.filter_by(record_id=record_id).delete()
            db.session.commit()
            return {"message": f"user with {record_id} was deleted"}, 200
        except Exception:
            return {"message": "Something went wrong"}, 500


@app.route('/account', methods=['POST'])
@auth.login_required(role=['user', 'admin'])
def account():
    pars = reqparse.RequestParser()
    pars.add_argument('id', help='id cannot be blank', required=True)
    pars.add_argument('number', help='number cannot be blank', required=True)
    pars.add_argument('cv', help='cv cannot be blank', required=True)
    pars.add_argument('password', help='password cannot be blank', required=True)
    pars.add_argument('available_balance', help='available_balance cannot be blank', required=True)
    pars.add_argument('userId', help='userId cannot be blank', required=True)

    data = pars.parse_args()
    try:
        id = int(data['id'])
        number = int(data['number'])
        cv = (data['cv'])
        password = (data['password'])
        available_balanse = int(data['available_balance'])
        userId = int(data['userId'])


    except Exception:
        return {'message': 'error'}, 500

    account_1 = Account(
        id=id,
        number=number,
        cv=cv,
        password=password,
        available_balance=available_balanse,
        userId=userId
    )

    try:
        account_1.add_to()
        return {"message": "everything is good"}, 200
    except Exception:
        return {"message": "error"}, 500


@app.route('/account/<int:id>', methods=["PUT", "DELETE", "GET"])
@auth.login_required(role=['user', 'admin'])
def account_by_id(id):
    if request.method == "PUT":
        pars = reqparse.RequestParser()
        pars.add_argument('id', help='id cannot be blank', required=True)
        pars.add_argument('number', help='number cannot be blank', required=True)
        pars.add_argument('cv', help='cv cannot be blank', required=True)
        pars.add_argument('password', help='password cannot be blank', required=True)
        pars.add_argument('available_balance', help='available_balance cannot be blank', required=True)
        pars.add_argument('userId', help='userId cannot be blank', required=True)

        data = pars.parse_args()
        try:
            Account.query.filter_by(id=id).update(data)
            db.session.commit()
            return {"message": f"item with {id} is up to date"}
        except Exception:
            return {"message": "Something went wrong"}, 500
        pass

    elif request.method == "GET":
        try:
            account_1 = Account.find_by_id(id=id)
            return {
                       "id": account_1.id,
                       "number": account_1.number,
                       "cv": account_1.cv,
                       "password": account_1.password,
                       "available_balance": account_1.available_balance,
                       "userId": account_1.userId

                   }, 200
        except Exception:
            return {'message': 'Error'}, 500

    elif request.method == "DELETE":
        if Account.query.filter_by(id=id).first() == None:
            return {"message": "Something went wrong"}, 404

        try:
            Account.query.filter_by(id=id).delete()
            db.session.commit()
            return {"message": f"user with {id} was deleted"}, 200
        except Exception:
            return {"message": "Something went wrong"}, 500


# @app.before_request
def init_database():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    app.run()

