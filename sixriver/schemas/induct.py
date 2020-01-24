from datetime import date
from marshmallow import Schema, fields, pprint, post_dump, post_load

from .. import models

from .common import SixRiverSchema
from .deserializer import register_schema


@register_schema
class InductSchema(SixRiverSchema):

    __schema_name__ = "induct"

    started_at = fields.DateTime(load_from="startedAt")
    completed_at = fields.DateTime(load_from="completedAt")
    user_id = fields.Str(data_key='userID', load_from="userID", required=True)
    device_id = fields.Str(data_key='deviceID', load_from="deviceID", required=True)

    @post_load
    def make_induct(self, data, **kwargs):
        return models.Induct(**data)
