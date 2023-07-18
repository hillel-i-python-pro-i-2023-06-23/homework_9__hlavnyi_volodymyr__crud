import os


def get_string_homework():
    text_its_docker = ""
    if os.environ.get("AM_I_IN_A_DOCKER_CONTAINER", False):
        text_its_docker = "We are running in Docker container!"
    return f"<h3> Homework #9 CRUID and phone book (Volodymyr Hlavnyi) </h2>" f"<br> <h4>{text_its_docker}</h4>"
