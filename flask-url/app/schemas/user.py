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


class UserResponseSchema(Schema):
    """Serialises a User model instance for API reponses."""

    id = fields.Int(dump_only=True)
    email = fields.Email(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


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


class LoginResponseSchema(Schema):
    """Serialises a response to include a User model and access tokens."""

    access_token = fields.Str(dump_only=True)
    refresh_token = fields.Str(dump_only=True)
    user = fields.Nested(UserResponseSchema, dump_only=True)


class RefreshResponseSchema(Schema):
    """Serialises a refresh token response."""

    access_token = fields.Str(dump_only=True)
