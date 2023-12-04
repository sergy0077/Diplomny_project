from tortoise.models import Model
from tortoise import fields


class Token(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="tokens")
    access_token = fields.CharField(max_length=255)
    expires_at = fields.DatetimeField()
