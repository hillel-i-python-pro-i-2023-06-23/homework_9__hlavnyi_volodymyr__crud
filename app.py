from flask import Flask, Response, redirect

from webargs import fields
from webargs.flaskparser import use_args

from application.models.db_connection import DBConnection

from application.services.special import get_string_homework
from application.services.create_table import create_table

from application.services.generate_phones import generate_list_of_phones


app = Flask(__name__)


# start/first route
@app.route("/")
@app.route("/start")
@app.route("/start/")
def start():
    return get_string_homework()


@app.route("/phones/create")
@app.route("/phones/create/")
@use_args({"name": fields.Str(reuired=True), "number": fields.Str(required=True)}, location="query")
def phone__create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phones (contact_name, phone_value) VALUES (:name,:number);",
                {"name": args["name"], "number": args["number"]},
            )
    return redirect("/phones/read-all")


@app.route("/phones/read-all")
def phones__read_all():
    with DBConnection() as connection:
        with connection:
            phones = connection.execute("SELECT * FROM phones;").fetchall()

    return "<br>".join([f'{phone["phone_id"]}: {phone["contact_name"]} - {phone["phone_value"]}' for phone in phones])


@app.route("/phones/create-all")
@app.route("/phones/create-all/<int:amount_of_phones>")
def phones__create_all(amount_of_phones: int = 10):
    phones = generate_list_of_phones(amount=amount_of_phones)
    for phone in phones:
        with DBConnection() as connection:
            with connection:
                connection.execute(
                    "INSERT INTO phones (contact_name, phone_value) VALUES (:name,:number);",
                    {"name": phone.contact_name, "number": phone.phone_value},
                )
    return redirect("/phones/read-all")


@app.route("/phones/read/<int:phone_id>")
def phone__read(phone_id: int):
    with DBConnection() as connection:
        phone = connection.execute(
            "SELECT * FROM phones WHERE (phone_id = :phone_id);",
            {
                "phone_id": phone_id,
            },
        ).fetchone()

    return f'{phone["phone_id"]}: {phone["contact_name"]} - {phone["phone_value"]}'


@app.route("/phones/update/<int:phone_id>")
@use_args({"name": fields.Str(), "number": fields.Str()}, location="query")
def phone__update(
    args,
    phone_id: int,
):
    with DBConnection() as connection:
        with connection:
            name = args["name"]
            number = args["number"]
            if name is None and number is None:
                return Response(
                    "Please provide at least one argument",
                    status=400,
                )
            args_for_request = []
            if name is not None:
                args_for_request.append("contact_name=:contact_name")
            if number is not None:
                args_for_request.append("phone_value=:phone_value")
            args_2 = ", ".join(args_for_request)
            connection.execute(
                "UPDATE phones " f"SET {args_2}" " WHERE (phone_id = :phone_id);",
                {
                    "phone_id": phone_id,
                    "contact_name": name,
                    "phone_value": number,
                },
            )
    return redirect("/phones/read-all")


@app.route("/phones/delete/<int:phone_id>")
def phone__delete(phone_id: int):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE FROM phones WHERE (phone_id = :phone_id);",
                {
                    "phone_id": phone_id,
                },
            )
    return redirect("/phones/read-all")


@app.route("/phones/delete-all")
def phones__delete_all():
    with DBConnection() as connection:
        with connection:
            connection.execute("DELETE FROM phones WHERE (1=1);")
    return redirect("/phones/read-all")


create_table()
