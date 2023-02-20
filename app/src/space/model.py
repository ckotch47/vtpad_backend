from tortoise.models import Model
from tortoise import fields


class SpaceModel(Model):
    id = fields.UUIDField(pk=True, index=True)
    name = fields.TextField(null=True)
    sort = fields.IntField()
