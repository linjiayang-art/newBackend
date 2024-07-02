from webargs import fields

user_args = {
    'userno': fields.Str(required=True),
    'username': fields.Str(required=True),
    'password_hash': fields.Str(required=True),
    'email': fields.Email(required=True)
}