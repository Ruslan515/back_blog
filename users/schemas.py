from ninja import Schema


class UserRegisterSchema(Schema):
    username: str
    password: str


class UserLoginSchema(Schema):
    username: str
    password: str


class UserOutSchema(Schema):
    id: int
    username: str
    token: str
