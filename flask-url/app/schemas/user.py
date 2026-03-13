from marshmallow import Schema, fields, validate


class RegisterRequestSchema(Schema):
    """Validates and deserialises a register request."""

    email = fields.Email(
        required=True, error_messages={"required": "An email address is required."}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(
            min=8, error="Password must be at least 8 characters."
        ),
        error_messages={"required": "A password is required."},
        load_only=True,
    )


class LoginRequestSchema(Schema):
    """Validates and deserialises a login request."""

    email = fields.Email(
        required=True, error_messages={"required": "An email address is required."}
    )
    password = fields.Str(
        required=True,
        error_messages={"required": "A password is required."},
        load_only=True,
    )


class UserResponseSchema(Schema):
    """Serialises a User model instance for API reponses."""

    id = fields.Int(dump_only=True)
    email = fields.Email(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


register_request_schema = RegisterRequestSchema()
login_request_schema = LoginRequestSchema()
user_response_schema = UserResponseSchema()
