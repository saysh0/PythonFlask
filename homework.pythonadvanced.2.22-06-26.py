from pydantic import BaseModel, Field, EmailStr, model_validator
import json

json_input = """{
    "name": "John Doe",
    "age": 70,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

json_input1 = """{
    "name": "John Doe",
    "age": 52,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "New York",
        "street": "5th Avenue",
        "house_number": 123
    }
}"""

json_input2 = """{
    "name": "John Doe",
    "age": 167,
    "email": "john.doe@example.cem",
    "is_employed": false,
    "address": {
        "city": "Old York",
        "street": "5th Avenue",
        "house_number": "123"
    }
}"""

class Address(BaseModel):
    city: str = Field(min_length=2)
    street: str = Field(min_length=3)
    house_number: int = Field(gt=0)

class User(BaseModel):
    name: str = Field(min_length=2, pattern=r"^[a-zA-Zа-яА-ЯёЁ ]+$")
    age: int = Field(gt=0, lt=120)
    email: EmailStr
    is_employed: bool
    address: Address

    @model_validator(mode='after')
    def checker_on_employed(self):
        if self.is_employed:
            if self.age < 18 or self.age > 65:
                raise ValueError('Your age or small or big!')
        return self


def checker_json(file: str):
    file_dict = json.loads(file)
    if User(**file_dict):
        return file

try:
    print(checker_json(json_input))
except Exception as e:
    print(e)

try:
    print(checker_json(json_input1))
except Exception as e:
    print(e)

try:
    print(checker_json(json_input2))
except Exception as e:
    print(e)
