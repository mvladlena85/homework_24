from marshmallow import Schema, fields, validate

from config import CMD_VALUES


class RequestSchema(Schema):
    file_name = fields.Str(required=True)
    cmd1 = fields.Str(required=True, validate=validate.OneOf(CMD_VALUES))
    value1 = fields.Str(required=True)
    cmd2 = fields.Str(validate=validate.OneOf(CMD_VALUES))
    value2 = fields.Str()
