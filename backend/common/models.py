from django.db import models
import uuid

# This model is created as basically a parent class to all the models that would be created later, these models include common fields that would be shared by all the models, so instead of inheriting the models.Model we would basically inherit these abstract classes. These classes are not reflected inside the database
class UUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseModel(UUIDModel, TimestampModel):
    class Meta:
        abstract = True
