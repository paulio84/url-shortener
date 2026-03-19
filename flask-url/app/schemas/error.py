from marshmallow import Schema, fields


class ErrorDetailSchema(Schema):
    status = fields.Int(dump_only=True)
    message = fields.Str(dump_only=True)


class ErrorSchema(Schema):
    error = fields.Nested(ErrorDetailSchema, dump_only=True)
