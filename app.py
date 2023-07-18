from flask import Flask  # , Request

# from webargs import fields
# from webargs.flaskparser import use_args

from application.services.special import get_string_homework
from application.services.create_table import create_table

from application.services.generate_users import generate_string_list_of_users, generate_list_of_users


app = Flask(__name__)


# start/first route
@app.route("/")
@app.route("/start")
@app.route("/start/")
def start():
    return get_string_homework()


@app.route("/phones/create")
@app.route("/phones/create/")
@app.route("/phones/create/<int:amount_of_phones>")
def create_phones(amount_of_phones: int = 10):
    phones = generate_list_of_users(amount=amount_of_phones)
    return generate_string_list_of_users(users=phones, type_of_list="ul")


@app.route("/phones/read-all")
def read_all_phones():
    pass


@app.route("/phones/read/<int:phone_id>")
def read_phone(phone_id: int):
    pass


@app.route("/phones/update/<int:phone_id>")
def update_phone(phone_id: int):
    pass


@app.route("/phones/delete/<int:phone_id>")
def delete_phone(phone_id: int):
    pass


@app.route("/generate-users")
@app.route("/generate-users/")
@app.route("/generate-users/<int:amount_of_users>")
def generate_users(amount_of_users: int = 100):
    users = generate_list_of_users(amount=amount_of_users)
    return generate_string_list_of_users(users=users, type_of_list="ol")


create_table()
