from collections.abc import Iterator
from typing import NamedTuple

from faker import Faker

faker = Faker()


class Phone_Book(NamedTuple):
    contact_name: str
    phone_value: str

    def get_dict(self) -> dict:
        return self._asdict()

    @classmethod
    def get_fieldnames(cls) -> list[str]:
        return list(cls._fields)

    @classmethod
    def from_raw_dict(cls, raw_data: dict) -> "Phone_Book":
        return cls(
            contacted_name=raw_data["contact_name"],
            phone_value=raw_data["phone_value"],
        )


def generate_phone() -> Phone_Book:
    return Phone_Book(
        contact_name=faker.name(),
        phone_value=faker.phone_number(),
    )


def generate_list_of_phones(amount: int = 10) -> Iterator[Phone_Book]:
    for _ in range(1, amount + 1):
        yield generate_phone()


def generate_string_list_of_phones(phonebooks, type_of_list="ol"):
    formatted_list = []
    for phone in phonebooks:
        formatted_phone = f"<li> Name: <b>{phone.contact_name}</b> - <span>phone: {phone.phone_value}</span></li>"
        formatted_list.append(formatted_phone)
    _temp_line = "\n".join(formatted_list)
    return f"<{type_of_list}>{_temp_line}</{type_of_list}>"
