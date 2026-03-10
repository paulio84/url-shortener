from marshmallow import Schema, fields


class ShortenRequestSchema(Schema):
    """Validates and deserialises a shorten request"""

    url = fields.Url(
        required=True,
        schemes=["http", "https"],
        error_messages={
            "required": "A 'url' field is required.",
            "invalid": "Must be a valid URL starting with http:// or https://",
        },
    )


class URLResponseSchema(Schema):
    """Serialise a URL model instance for API responses."""

    id = fields.Int(dump_only=True)
    original_url = fields.Str(dump_only=True)
    short_code = fields.Str(dump_only=True)
    short_url = fields.Str(dump_only=True)
    clicks = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)


shorten_request_schema = ShortenRequestSchema()
url_response_schema = URLResponseSchema()
url_response_list_schema = URLResponseSchema(many=True)
