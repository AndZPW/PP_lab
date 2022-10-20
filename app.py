from flask import Flask
from flask import make_response
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Tkach2004@localhost:3306/BudgetDb'

db=SQLAlchemy(app)
migrate=Migrate(app,db)
status_code: int = 200


@app.route('/api/v1/hello-world-11')
def index():
    return make_response(f"Hello World 11", status_code)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    firstName = db.Column(db.String(255), nullable=False)
    lastName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Account (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    cv = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(120), nullable=False)
    available_balance=db.Column(db.Integer, nullable=False)
    userId=db.Column(db.Integer, db.ForeignKey("user.id"),nullable=False)

assosiation_table=db.Table(
    "user_to_budget",
    db.Column("user_id",db.Integer,db.ForeignKey("user.id")),
    db.Column("budget_id", db.Integer,db.ForeignKey("budget.record_id"))
)
class Budget (db.Model):
    title = db.Column(db.String(255), nullable=False)
    record_id = db.Column(db.Integer, primary_key=True)
    name_user = db.Column(db.String(120), unique=True, nullable=False)
    income = db.Column(db.Integer, nullable=False)
    outcome = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    available_balance=db.Column(db.Integer, nullable=False)
    user=db.relationship("budget",secondary=assosiation_table)


@app.before_request
def init_database():
    db.drop_all()
    db.create_all()
    db.session.commit()
if __name__ == '__main__':
    app.run()
